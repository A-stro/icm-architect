#!/usr/bin/env python3
"""Check a concept map: links resolve, note types sit in the schema, every quoted line appears
word for word in its raw source, and nothing on the keep-out list shows up anywhere.

Copy this file to _tools/ in the map and run from anywhere:  python -I _tools/check-concept-map.py
Standard library only. Exits 1 on any problem; warnings do not fail the run but should be read.

A quote is  "verbatim line" (key position)  where
  key       names a file in sources/raw/ (its name without the extension, or a short name
            declared in _meta/sources.txt as  key = filename)
  position  a timestamp or range for transcripts (12:30, 1:02:15, 12:30-13:05), or a page or
            page range for documents (page 2, p2, pp 4-5)
Transcripts are timed when their lines start with **[12:30]** or [12:30]. A document is paged when
it has lines that read  Page 1, Page 2 ... ; any other source is matched anywhere and its position
is not checked. A cut inside a quote is written ... and each piece is checked in order.
A timed quote is accepted within one paragraph of its cited position, since a line can straddle two.

Options
  --show-cuts         list every quote that uses a cut, with the words the cut drops
  --write-indexes     (re)write each shelf's _index.md from its notes' title and description
  --tokens PLAN       approximate size of the entry file + that plan + its first three concepts
"""
import bisect
import re
import sys
import urllib.parse
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "sources" / "raw"
SKIP_DIRS = {"raw", "_meta", "_tools", "_templates", ".git"}
NOT_NOTES = {"index.md", "_index.md", "log.md", "claude.md", "agents.md", "context.md", "routing.md"}
TIME = r"\d+(?::\d+)+"
LINK = re.compile(r"\[[^\]]*\]\((<[^>]+>|[^)\s]+)\)")
QUOTE = re.compile(r'"([^"\n]+?)"\s*\(([A-Za-z0-9_.-]+)(?:\s+([^)]*))?\)')
ANY_QUOTE = re.compile(r'"([^"\n]+)"')
POSITION = re.compile(rf"({TIME})(?:\s*[–-]\s*({TIME}))?")
PAGE_POSITION = re.compile(r"(?:\bpp?\.?|\bpages?)\s*(\d+)(?:\s*[–-]\s*(\d+))?", re.I)
PAGE_LINE = re.compile(r"^\s*\[?page\s+(\d+)\]?\s*$", re.I)
CITATION_LIKE = re.compile(rf"{TIME}|\bpp?\.?\s*\d+|\bpages?\b|§", re.I)
WORDS_HEADING = re.compile(r"#{1,6}\s*in\s+(their|his|her|the speaker'?s?)\s+words", re.I)
NEGATION = re.compile(r"\b(never|not|no|none|nothing|nobody|without|cannot|neither|nor|hardly|"
                      r"cant|dont|doesnt|didnt|isnt|arent|wasnt|werent|wont|wouldnt|shouldnt|couldnt)\b")

problems, warnings, cuts, stubs = [], [], [], []


def norm(s):
    s = s.lower().replace("’", "'").replace("'", "")
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", s)).strip()


def secs(t):
    n = 0
    for part in t.split(":"):
        n = n * 60 + int(part)
    return n


def straighten(text):
    return text.replace("“", '"').replace("”", '"')


def match_in_order(pieces, haystack):
    """Return (missing_piece, gaps): the first piece not found in order, and the text between pieces."""
    pos, gaps = 0, []
    for k, piece in enumerate(pieces):
        i = haystack.find(piece, pos)
        if i < 0:
            return piece, gaps
        if k:
            gaps.append(haystack[pos:i])
        pos = i + len(piece)
    return None, gaps


def load_sources():
    files = {p.stem: p for p in sorted(RAW.glob("*")) if p.is_file()} if RAW.exists() else {}
    aliases = ROOT / "_meta" / "sources.txt"
    if aliases.exists():
        for line in aliases.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.lstrip().startswith("#"):
                key, name = (x.strip() for x in line.split("=", 1))
                if (RAW / name).is_file():
                    files[key] = RAW / name
                else:
                    problems.append(f"_meta/sources.txt: {key} -> {name} is not in sources/raw/")
    sources = {}
    for key, path in files.items():
        text = path.read_text(encoding="utf-8", errors="replace")
        paras = []
        for line in text.splitlines():
            m = re.match(rf"\s*(?:\*\*)?\[({TIME})\](?:\*\*)?\s*(.*)", line)
            if m:
                paras.append((secs(m.group(1)), norm(m.group(2))))
        if paras:
            sources[key] = ("timed", paras)
            continue
        pages, current = {}, None
        for line in text.splitlines():
            m = PAGE_LINE.match(line)
            if m:
                current = int(m.group(1))
                pages[current] = []
            elif current is not None:
                pages[current].append(line)
        if pages:
            sources[key] = ("paged", {n: norm(" ".join(lines)) for n, lines in pages.items()})
        else:
            sources[key] = ("plain", norm(text))
    return sources


def check_quote(text, key, position, sources):
    """Return (error or None, warning or None, cut gaps)."""
    pieces = [norm(p) for p in re.split(r"\.\.\.|…", text) if norm(p)]
    if len(pieces) > 1 and any(len(p.split()) < 2 for p in pieces):
        return "a piece of a cut quote is too short to verify", None, []
    kind, data = sources[key]
    if kind == "plain":
        missing, gaps = match_in_order(pieces, data)
        return (f"not found in the source: {missing[:60]}" if missing else None), None, gaps
    if kind == "paged":
        m = PAGE_POSITION.search(position or "")
        if not m:
            return "the citation has no page", None, []
        first, last = int(m.group(1)), int(m.group(2) or m.group(1))
        absent = [n for n in range(first, last + 1) if n not in data]
        if absent:
            return f"page {absent[0]} is not in the source", None, []
        missing, gaps = match_in_order(pieces, " ".join(data[n] for n in range(first, last + 1)))
        return (f"not found on the cited page: {missing[:60]}" if missing else None), None, gaps
    m = POSITION.search(position or "")
    if not m:
        return "the citation has no timestamp", None, []
    start, end = secs(m.group(1)), secs(m.group(2) or m.group(1))
    times = [t for t, _ in data]
    lo, hi = bisect.bisect_right(times, start) - 1, bisect.bisect_right(times, end) - 1
    wide = " ".join(p for _, p in data[max(0, lo - 1): hi + 2])
    missing, gaps = match_in_order(pieces, wide)
    if missing:
        return f"not found near that position: {missing[:60]}", None, gaps
    tight = " ".join(p for _, p in data[max(0, lo): hi + 1])
    if match_in_order(pieces, tight)[0]:
        return None, "found in a neighboring paragraph, not the cited one", gaps
    return None, None, gaps


def front_matter(text):
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[3:end], text[end + 4:]
    return "", text


def field(front, name):
    m = re.search(rf"^{name}:\s*(.+)$", front, re.M)
    if not m:
        return ""
    v = m.group(1).strip()
    return v[1:-1] if len(v) > 1 and v[0] == v[-1] and v[0] in "\"'" else v


def read_list(path):
    if not path.exists():
        return []
    lines = (x.strip() for x in path.read_text(encoding="utf-8").splitlines())
    return [x for x in lines if x and not x.startswith("#")]


def keep_out_patterns():
    return [re.compile(r"(?<!\w)" + re.escape(p) + r"(?!\w)", re.I) for p in read_list(ROOT / "_meta" / "keep-out.txt")]


def check_words_sections(rel, body, sources):
    """Every bullet under 'In their words' must be a cited quote."""
    inside = False
    for line in straighten(body).splitlines():
        if line.lstrip().startswith("#"):
            inside = bool(WORDS_HEADING.match(line.strip()))
            continue
        if inside and re.match(r"\s*[-*]\s", line):
            if not any(m.group(2) in sources for m in QUOTE.finditer(line)):
                problems.append(f"{rel}: a bullet under 'In their words' has no cited quote: {line.strip()[:60]}")


def write_or_check_indexes(notes, write):
    shelves = {}
    for f, front in notes:
        if f.parent != ROOT:
            shelves.setdefault(f.parent, []).append((f, front))
    for shelf, items in sorted(shelves.items()):
        lines = ["<!-- generated by _tools/check-concept-map.py; do not edit -->", f"# {shelf.name.capitalize()}", ""]
        for f, front in sorted(items, key=lambda x: x[0].name):
            lines.append(f"* [{field(front, 'title') or f.stem}]({f.name}) - {field(front, 'description')}")
        text = "\n".join(lines) + "\n"
        target = shelf / "_index.md"
        if write:
            target.write_text(text, encoding="utf-8", newline="\n")
            print(f"wrote {target.relative_to(ROOT).as_posix()}")
        elif target.exists() and target.read_text(encoding="utf-8").strip() != text.strip():
            problems.append(f"{target.relative_to(ROOT).as_posix()}: stale, run with --write-indexes")


def tokens(plan_arg):
    plan = (ROOT / plan_arg) if (ROOT / plan_arg).exists() else Path(plan_arg)
    parts = [ROOT / "CLAUDE.md", plan]
    linked = re.findall(r"\]\(([^)\s]*concepts/[^)\s#]+\.md)\)", plan.read_text(encoding="utf-8"))
    parts += [(plan.parent / link).resolve() for link in dict.fromkeys(linked)][:3]
    total = 0
    for p in parts:
        n = len(p.read_text(encoding="utf-8")) // 4 if p.exists() else 0
        total += n
        print(f"  ~{n:5d} tokens  {p.name}")
    print(f"  ~{total:5d} tokens in all (stay under 8,000; the 2,000 floor is a guide for a full-size step, not a target)")


def main():
    args = sys.argv[1:]
    if "--tokens" in args:
        tokens(args[args.index("--tokens") + 1])
        return
    sources = load_sources()
    schema = ROOT / "_meta" / "schema.md"
    types = None
    if schema.exists():
        m = re.search(r"^types:\s*(.+)$", schema.read_text(encoding="utf-8"), re.M | re.I)
        if m:
            types = {t.strip().lower() for t in m.group(1).split(",") if t.strip()}
    keep_out = keep_out_patterns()

    files = sorted(f for f in ROOT.rglob("*.md") if not SKIP_DIRS & set(f.relative_to(ROOT).parts))
    counts, links, quotes, notes = {}, 0, 0, []
    for f in files:
        rel = f.relative_to(ROOT).as_posix()
        text = f.read_text(encoding="utf-8")
        front, body = front_matter(text)
        is_note = f.name.lower() not in NOT_NOTES

        for pattern in keep_out:  # every file, frontmatter included
            if pattern.search(text):
                problems.append(f"{rel}: contains a phrase from _meta/keep-out.txt")
                break

        for m in LINK.finditer(body):
            target = m.group(1)[1:-1] if m.group(1).startswith("<") else m.group(1)
            if re.match(r"^[a-z]+:", target) or target.startswith("#"):
                continue
            links += 1
            if not (f.parent / urllib.parse.unquote(target.split("#")[0])).resolve().exists():
                problems.append(f"{rel}: broken link -> {target}")

        if not is_note:
            continue
        notes.append((f, front))
        if re.search(r"^status:\s*stub\b", front, re.M):
            stubs.append(rel)
        t = re.search(r"^type:\s*(\S+)", front, re.M)
        note_type = t.group(1).lower() if t else None
        counts[note_type or "(none)"] = counts.get(note_type or "(none)", 0) + 1
        if note_type is None:
            problems.append(f"{rel}: no type in the frontmatter")
        elif types is not None and note_type not in types:
            problems.append(f"{rel}: type '{note_type}' is not in _meta/schema.md")

        text_q = straighten(body)
        check_words_sections(rel, body, sources)
        cited = set()
        for m in QUOTE.finditer(text_q):
            quote, key, position = m.group(1), m.group(2), m.group(3)
            cited.add(m.start())
            if key not in sources:
                if CITATION_LIKE.search(position or ""):
                    problems.append(f"{rel}: unknown source key '{key}' for: {quote[:50]}")
                continue
            quotes += 1
            error, warn, gaps = check_quote(quote, key, position, sources)
            where = f"{rel} ({key} {position or ''})".replace(" )", ")")
            if error:
                problems.append(f"{where}: {error}")
            if warn:
                warnings.append(f"{where}: {warn}")
            if "..." in quote or "…" in quote:
                cuts.append((where, quote, gaps))
                dropped = [g for g in gaps if NEGATION.search(g)]
                if dropped and not error:
                    problems.append(f"{where}: a cut drops a negation: ...{dropped[0][:60]}...")
        for m in ANY_QUOTE.finditer(text_q):
            if m.start() not in cited and len(m.group(1).split()) >= 8:
                warnings.append(f"{rel}: quoted words with no citation: {m.group(1)[:60]}")

    if stubs:
        warnings.append(f"{len(stubs)} stub note(s) remain: " + ", ".join(stubs[:6]) + (" ..." if len(stubs) > 6 else ""))
    write_or_check_indexes(notes, "--write-indexes" in args)
    print(f"{sum(counts.values())} notes, {links} links, {quotes} quotes checked, {len(cuts)} with cuts")
    for name, n in sorted(counts.items()):
        print(f"  {name}: {n}")
    if "--show-cuts" in args:
        for where, quote, gaps in cuts:
            print(f"  cut in {where}: \"{quote[:80]}\" drops: " + " | ".join(g[:50] for g in gaps))
    if warnings:
        print(f"{len(warnings)} warning(s), read them:")
        for w in warnings:
            print("  " + w)
    if problems:
        print(f"{len(problems)} problem(s):")
        for p in problems:
            print("  " + p)
        sys.exit(1)
    print("ok: every link resolves, every quote matches its source")


if __name__ == "__main__":
    main()
