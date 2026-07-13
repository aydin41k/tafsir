#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path


ONES = {
    1: "bir",
    2: "iki",
    3: "üç",
    4: "dört",
    5: "beş",
    6: "altı",
    7: "yedi",
    8: "sekiz",
    9: "dokuz",
}
TENS = {
    10: "on",
    20: "yirmi",
    30: "otuz",
    40: "kırk",
    50: "elli",
    60: "altmış",
    70: "yetmiş",
    80: "seksen",
    90: "doksan",
}
ORDINAL_LAST_WORD = {
    "bir": "birinci",
    "iki": "ikinci",
    "üç": "üçüncü",
    "dört": "dördüncü",
    "beş": "beşinci",
    "altı": "altıncı",
    "yedi": "yedinci",
    "sekiz": "sekizinci",
    "dokuz": "dokuzuncu",
    "on": "onuncu",
    "yirmi": "yirminci",
    "otuz": "otuzuncu",
    "kırk": "kırkıncı",
    "elli": "ellinci",
    "altmış": "altmışıncı",
    "yetmiş": "yetmişinci",
    "seksen": "sekseninci",
    "doksan": "doksanıncı",
    "yüz": "yüzüncü",
}

SENTENCE_PREFIX = r"(?P<prefix>(?:^|(?<!\d)[.!?][”\"']?\s+)[“\"']?)"
NUMBER_SERIES = (
    r"\d{1,3}(?:(?:\s*[-–,]\s*|\s+ve\s+|\.\s+(?:ve\s+)?)\d{1,3})*\.?"
)
SENTENCE_INITIAL_AYAH = re.compile(
    SENTENCE_PREFIX
    + rf"(?P<numbers>{NUMBER_SERIES})\s*"
    r"(?P<ayah>[AaÂâ]yet\w*)",
    re.MULTILINE,
)
SENTENCE_INITIAL_CARDINAL = re.compile(
    SENTENCE_PREFIX
    + r"(?P<number>\d{1,6}(?:\.\d{3})*)"
    r"(?P<suffix>[’'][A-Za-zÇĞİÖŞÜçğıöşü]+)?(?=\s|[,;:](?=\s))",
    re.MULTILINE,
)
SENTENCE_INITIAL_NAMED_ORDINAL = re.compile(
    SENTENCE_PREFIX
    + rf"(?P<numbers>{NUMBER_SERIES})\s*"
    r"(?P<noun>(?:[Yy]üzyıl|[Aa]s(?:ı)?r|[Ss]öz|[Dd]eva)\w*)",
    re.MULTILINE,
)


def turkish_number_under_thousand(number: int) -> str:
    if not 1 <= number <= 999:
        raise ValueError(f"Unsupported Turkish ordinal number: {number}")
    words: list[str] = []
    hundreds, remainder = divmod(number, 100)
    if hundreds:
        if hundreds > 1:
            words.append(ONES[hundreds])
        words.append("yüz")
    tens, ones = divmod(remainder, 10)
    if tens:
        words.append(TENS[tens * 10])
    if ones:
        words.append(ONES[ones])
    return " ".join(words)


def turkish_number(number: int) -> str:
    if not 1 <= number <= 999_999:
        raise ValueError(f"Unsupported Turkish number: {number}")
    thousands, remainder = divmod(number, 1000)
    words: list[str] = []
    if thousands:
        if thousands > 1:
            words.append(turkish_number_under_thousand(thousands))
        words.append("bin")
    if remainder:
        words.append(turkish_number_under_thousand(remainder))
    return " ".join(words)


def turkish_ordinal(number: int) -> str:
    words = turkish_number(number).split()
    words[-1] = ORDINAL_LAST_WORD[words[-1]]
    return " ".join(words)


def normalize_sentence_initial_ayah_ordinals(text: str) -> str:
    def written_ordinals(raw_numbers: str) -> str:
        numbers = [int(value) for value in re.findall(r"\d+", raw_numbers)]
        ordinals = [turkish_ordinal(number) for number in numbers]
        if len(ordinals) == 1:
            return ordinals[0]
        if len(ordinals) == 2:
            return f"{ordinals[0]} ve {ordinals[1]}"
        return f"{', '.join(ordinals[:-1])} ve {ordinals[-1]}"

    def replace_ayah(match: re.Match[str]) -> str:
        written = written_ordinals(match.group("numbers"))
        ayah = match.group("ayah")
        ayah = ayah[0].lower() + ayah[1:]
        return f"{match.group('prefix')}{written.capitalize()} {ayah}"

    def replace_named_ordinal(match: re.Match[str]) -> str:
        written = written_ordinals(match.group("numbers")).capitalize()
        return f"{match.group('prefix')}{written} {match.group('noun')}"

    def replace_cardinal(match: re.Match[str]) -> str:
        number = int(match.group("number").replace(".", ""))
        written = turkish_number(number)
        suffix = (match.group("suffix") or "").lstrip("’'")
        if suffix:
            head, separator, last = written.rpartition(" ")
            written = f"{head}{separator}{last}{suffix}"
        return f"{match.group('prefix')}{written.capitalize()}"

    text = SENTENCE_INITIAL_AYAH.sub(replace_ayah, text)
    text = SENTENCE_INITIAL_NAMED_ORDINAL.sub(replace_named_ordinal, text)
    return SENTENCE_INITIAL_CARDINAL.sub(replace_cardinal, text)


def markdown_files(paths: list[str]) -> list[Path]:
    files: list[Path] = []
    for raw_path in paths:
        path = Path(raw_path)
        if path.is_dir():
            files.extend(sorted(path.rglob("*.md")))
        elif path.suffix == ".md":
            files.append(path)
    return files


def main() -> int:
    parser = argparse.ArgumentParser(description="Enforce deterministic Turkish editorial style rules.")
    parser.add_argument("paths", nargs="+", help="Markdown files or directories to inspect")
    parser.add_argument("--check", action="store_true", help="Report files requiring changes without writing")
    args = parser.parse_args()

    changed: list[Path] = []
    for path in markdown_files(args.paths):
        original = path.read_text(encoding="utf-8")
        normalized = normalize_sentence_initial_ayah_ordinals(original)
        if normalized == original:
            continue
        changed.append(path)
        if not args.check:
            path.write_text(normalized, encoding="utf-8")

    if args.check and changed:
        for path in changed:
            print(path)
        return 1
    print(f"editorial_style: {len(changed)} file(s) {'would change' if args.check else 'changed'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
