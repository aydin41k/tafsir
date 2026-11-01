#!/usr/bin/env python3
"""
Typeset the Badr chapter as a printable book, in either edition.

Design replicates the Everyman's Library / Folio Society tradition:
Jan Tschichold's golden canon of page construction, in which the text
block is set high and toward the gutter with margins in the proportion
2:3:4:6 (inner:top:outer:bottom). Text face EB Garamond, a revival of
Claude Garamond's sixteenth-century romans, with real small caps and
old-style figures. Amiri covers the Arabic glyphs.

Usage
  typeset.py [en|tr]        default en

Outputs
  dist/the-water-at-badr-A5.pdf         one book page per PDF page
  dist/the-water-at-badr-booklet-A4.pdf 2-up imposed, folded signatures
  dist/bedir-suyu-A5.pdf                the same, Turkish edition
  dist/bedir-suyu-kitapcik-A4.pdf
"""

import html
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

BOOK = Path(__file__).resolve().parent.parent
FONTS = BOOK / "build" / "fonts"
DIST = BOOK / "dist"


# ------------------------------------------------------------------ editions

@dataclass(frozen=True)
class Edition:
    code: str
    src: str
    lang: str
    title: str
    subtitle: str
    imprint: str
    contents: str
    notes: str
    notes_marker: str
    page_abbr: str           # leads the endnote back-reference: "p. " / "s. "
    back_matter: frozenset   # divisions that open on a fresh recto
    running: dict            # section title -> the form printed and run as head
    roster: frozenset        # sections set as a roster of entries
    gloss: frozenset         # sections set as a glossary
    figure_after: str        # section the valley plate follows
    labels: dict             # the plate's lettering
    colophon_head: str
    colophon: tuple
    stem: str                # output file stem
    booklet: str             # the word between stem and -A4
    hyphens: str = "auto"    # 'manual' where pyphen has no dictionary
    apostrophe_after: str = ""   # extra chars a suffix apostrophe may follow

    @property
    def path(self) -> Path:
        return BOOK / self.src

    @property
    def hyphenate(self):
        return hyphenate_html if self.hyphens == "manual" else None


EN = Edition(
    code="en",
    src="badr-chapter.md",
    lang="en-GB",
    title="The Water at Badr",
    subtitle="The Battle of Badr, 17 Ramadan 2 AH",
    imprint="Printed for private reading",
    contents="Contents",
    notes="Notes",
    notes_marker="\n## Notes\n",
    page_abbr="p. ",
    back_matter=frozenset({
        "A Note on the Sources",
        "What the Sources Disagree About",
        "The Principal Figures",
        "The Fallen",
        "Chronology",
        "A Note on Numbers and Distances",
        "Glossary",
        "Further Reading",
        "Notes",
    }),
    running={
        "What the Sources Disagree About": "What the Sources Disagree About",
        "A Note on Numbers and Distances": "Numbers and Distances",
    },
    roster=frozenset({"The Principal Figures", "Further Reading"}),
    gloss=frozenset({"Glossary"}),
    figure_after="The Valley of Yalyal",
    labels=dict(
        aria="Schematic plan of the valley at Badr",
        dark_rock="DARK ROCK",
        broken="broken rocky ground",
        broken_x=256, broken_w=148,
        aqanqal="AL-&#8216;AQANQAL",
        aqanqal_y=176, aqanqal_h=76,
        mecca="to Mecca", mecca_w=56,
        medina="to Medina", medina_w=60,
        quraysh="Quraysh",
        muslims="Muslims",
        wadi="Wadi Yalyal",
        dune="dune belt",
        scale="about one mile",
        north="N",
        legend=(
            '<span class="k">1</span>&#8202;the wells, seven or eight of\n'
            'them &#183; <span class="k">2</span>&#8202;the <em>hawd</em>, '
            'the cistern dug and\nfilled on al-Hubab&#8217;s advice &#183; '
            '<span class="k">3</span>&#8202;the\n'
            '<em>&#8216;arish</em>, the shelter of palm branches &#183;\n'
            '<span class="k">4</span>&#8202;wells broken in and filled with '
            'sand'
        ),
        caption=(
            "The floor at Badr, looking down. A schematic drawn from the\n"
            "descriptions in Ibn Ishaq and al-Waqidi, not a survey: the "
            "distances are the\nones the sources give and the shapes are "
            "indicative only. The Muslims held\nthe firm nearer bank with "
            "the wells, the cistern and the shelter behind them.\n"
            "Quraysh walked their column over the wall of sand at "
            "al-&#8216;Aqanqal and\nspent the night in the hollows of the "
            "farther bank, three-quarters of a mile\nfrom a drink, with the "
            "whole Muslim army between them and the water."
        ),
    ),
    colophon_head="A note on this edition",
    colophon=(
        "The text is a single chapter, set here as a book. It commits in the\n"
        "    prose and argues in the notes: a reader who skips every note will meet\n"
        "    an unbroken story, and one who reads them will find the disputes set\n"
        "    out. The seven narrative sections come first; the apparatus &#8212; the\n"
        "    weighing of the sources, the contested points, the rosters, the\n"
        "    casualty lists, the chronology and the glossary &#8212; follows, and then\n"
        "    the notes.",
        "Dates are given in the Hijri calendar first, with the Julian\n"
        "    equivalent in parentheses. Distances are in miles. A dagger\n"
        "    (&#8224;) in the lists marks an attribution the sources dispute.",
        "The page is set to Jan Tschichold&#8217;s golden canon, in which the\n"
        "    text block is placed high on the leaf and toward the gutter, with the\n"
        "    margins in the proportion 2:3:4:6 &#8212; inner, top, outer, bottom &#8212;\n"
        "    so that the two pages of an opening read as one field. The type is\n"
        "    EB Garamond, a revival of the romans cut by Claude Garamond in\n"
        "    sixteenth-century Paris, with old-style figures and drawn small\n"
        "    capitals; the Arabic glyphs are Amiri.",
    ),
    stem="the-water-at-badr",
    booklet="booklet",
)


TR = Edition(
    code="tr",
    src="badr-chapter.tr.md",
    lang="tr-TR",
    title="Bedir Suyu",
    subtitle="Bedir Savaşı, 17 Ramazan 2 (hicrî)",
    imprint="Husûsî okuma için basılmıştır",
    contents="İçindekiler",
    notes="Notlar",
    notes_marker="\n## Notlar\n",
    page_abbr="s. ",
    back_matter=frozenset({
        "Kaynaklar Üzerine Bir Not",
        "Kaynakların İhtilâf Ettiği Hususlar",
        "Başlıca Şahıslar",
        "Düşenler",
        "Kronoloji",
        "Sayılar ve Mesafeler Üzerine Bir Not",
        "Sözlük",
        "İleri Okuma",
        "Notlar",
    }),
    running={
        "Sayılar ve Mesafeler Üzerine Bir Not": "Sayılar ve Mesafeler",
    },
    roster=frozenset({"Başlıca Şahıslar", "İleri Okuma"}),
    gloss=frozenset({"Sözlük"}),
    figure_after="Yelyel Vadisi",
    labels=dict(
        aria="Bedir vadisinin şematik planı",
        dark_rock="KOYU KAYA",
        broken="engebeli kayalık arazi",
        broken_x=244, broken_w=172,
        aqanqal="AKANKAL",
        aqanqal_y=188, aqanqal_h=52,
        mecca="Mekke&#8217;ye", mecca_w=60,
        medina="Medine&#8217;ye", medina_w=64,
        quraysh="Kureyş",
        muslims="Müslümanlar",
        wadi="Yelyel Vadisi",
        dune="kumul kuşağı",
        scale="yaklaşık bir buçuk kilometre",
        north="K",
        legend=(
            '<span class="k">1</span>&#8202;kuyular, yedi sekiz tane\n'
            '&#183; <span class="k">2</span>&#8202;<em>havuz</em>, '
            'Hubâb&#8217;ın tavsiyesiyle\nkazılıp doldurulan sarnıç &#183; '
            '<span class="k">3</span>&#8202;\n'
            '<em>arîş</em>, hurma dallarından gölgelik &#183;\n'
            '<span class="k">4</span>&#8202;çökertilip kumla doldurulan '
            'kuyular'
        ),
        caption=(
            "Bedir&#8217;deki taban, yukarıdan. İbn İshak ve Vâkıdî&#8217;deki\n"
            "tasvirlerden çizilmiş bir şema, bir ölçüm değil: mesafeler "
            "kaynakların\nverdiği mesafeler, şekiller ise yalnızca "
            "yaklaşıktır. Müslümanlar kuyuları,\nhavuzu ve gölgeliği "
            "arkalarına alarak sağlam beri yakayı tuttular.\n"
            "Kureyş kolonunu Akankal&#8217;daki kum duvarının üstünden "
            "yürüttü ve\ngeceyi uzak yakanın çukurlarında, bir yudumdan bir "
            "küsur kilometre\nuzakta, aralarında ve su arasında bütün "
            "müslüman ordusu bulunarak geçirdi."
        ),
    ),
    colophon_head="Bu neşir hakkında bir not",
    colophon=(
        "Metin tek bir bölümdür, burada bir kitap olarak dizilmiştir.\n"
        "    Nesirde karar verir, notlarda tartışır: her notu atlayan okur "
        "kesintisiz\n    bir hikâyeyle karşılaşır, notları okuyan ise "
        "ihtilâfları serilmiş hâlde\n    bulur. Yedi anlatı bölümü önce "
        "gelir; tertibat &#8212; kaynakların tartılması,\n    ihtilâflı "
        "noktalar, şahıs listeleri, maktul listeleri, kronoloji ve sözlük\n"
        "    &#8212; onu izler, en sonda da notlar gelir.",
        "Tarihler önce hicrî takvimle, Jülyen karşılığı parantez içinde\n"
        "    verilmiştir. Mesafeler kilometreyledir. Listelerdeki bir hançer\n"
        "    (&#8224;) kaynakların ihtilâf ettiği bir nispeti gösterir.",
        "Sayfa Jan Tschichold&#8217;un altın kanonuna göre kurulmuştur: metin\n"
        "    bloğu yaprağın üst kısmına ve cilt payına doğru yerleştirilir, "
        "kenar\n    boşlukları 2:3:4:6 oranındadır &#8212; iç, üst, dış, alt "
        "&#8212; böylece bir\n    açılımın iki sayfası tek bir alan olarak "
        "okunur. Yazı karakteri, Claude\n    Garamond&#8217;un on altıncı "
        "yüzyıl Paris&#8217;inde kestiği romenlerinin bir\n    ihyası olan "
        "EB Garamond&#8217;dur; eski usul rakamlarla ve çizilmiş küçük\n"
        "    kapitellerle. Arapça glifler Amiri&#8217;dir.",
    ),
    stem="bedir-suyu",
    booklet="kitapcik",
    hyphens="manual",
    # A suffix apostrophe in Turkish often follows a closing emphasis marker:
    # *Tabakāt*'ı, **Safrâ**'da. It is a right quote, not an opening one.
    apostrophe_after="*",
)

EDITIONS = {e.code: e for e in (EN, TR)}


# ------------------------------------------------------------- hyphenation

# pyphen ships no Turkish dictionary, so hyphens:auto is silently a no-op for
# the Turkish edition and its justified measure opens rivers. Turkish
# syllabification is regular enough to do by rule, so we mark the breaks in
# the text with soft hyphens and let CSS hyphens:manual use them.

VOWELS = set("aeıioöuüâêîôûāēīōū" "AEIİOÖUÜÂÊÎÔÛĀĒĪŌŪ")
_WORD = re.compile(r"[^\W\d_]{7,}", re.U)
_MARKUP = re.compile(r"<[^>]*>|&[#0-9A-Za-z]+;")
SHY = "­"

# English words — the titles, authors and publishers cited in Further Reading
# and the notes — would be broken on Turkish syllables (Mag-hazi, His-tory).
# There is no orthographic tell to catch them by, so they are listed: every
# word of seven letters or more in the Turkish text that is not Turkish. A
# missed break costs nothing; a wrong one is visible. Words of six letters or
# fewer (Oxford, Darwin, Waqidi) are never broken anyway.
FOREIGN_WORDS = frozenset("""
    Believers Boycott Community Earliest Foundation Gassick Guillaume Harvard
    History Islamic Maghazi Marsden McDonald Montgomery Muhammad Narratives
    Origins Patricia Princeton Routledge Society Sources Supplies
""".split())


def syllables(word: str):
    """Split a Turkish word into syllables.

    Cut between each pair of adjacent vowels: with no consonant between them
    the break falls between the vowels (sa-at); with one, before it
    (Ra-ma-zan); with two or more, before the last (Ab-dül, e-lekt-rik).
    """
    v = [i for i, c in enumerate(word) if c in VOWELS]
    if len(v) < 2:
        return [word]
    out, prev = [], 0
    for a, b in zip(v, v[1:]):
        cut = b if b - a == 1 else b - 1
        out.append(word[prev:cut])
        prev = cut
    out.append(word[prev:])
    return out


def hyphenate_word(word: str, left=3, right=3) -> str:
    """Insert soft hyphens, keeping left/right stubs at least three letters."""
    if word in FOREIGN_WORDS:
        return word
    parts = syllables(word)
    if len(parts) < 2:
        return word
    out = parts[0]
    for part in parts[1:]:
        if len(out) >= left and len(word) - len(out) >= right:
            out += SHY
        out += part
    return out


def hyphenate_text(text: str) -> str:
    return _WORD.sub(lambda m: hyphenate_word(m.group(0)), text)


def hyphenate_html(fragment: str) -> str:
    """Soft-hyphenate the text of an HTML fragment, never its markup."""
    out, pos = [], 0
    for m in _MARKUP.finditer(fragment):
        out.append(hyphenate_text(fragment[pos:m.start()]))
        out.append(m.group(0))
        pos = m.end()
    out.append(hyphenate_text(fragment[pos:]))
    return "".join(out)


# ---------------------------------------------------------------- punctuation

def smarten(text: str, ed: Edition) -> str:
    """Curly quotes, with care for 'ayn and hamza.

    The source uses a straight apostrophe for three different things:
    the possessive or Turkish suffix, and the Arabic 'ayn and hamza.
    Word-initial occurrences are 'ayn ('Utba, al-'Abbas) and take a left
    quote, which is the scholarly convention; everything else is a right
    quote, which serves both the possessive and medial or final 'ayn/hamza
    (Ka'ba, al-Safra'). Verified against the chapter's transliteration list.
    """
    # Double quotes: opening after start-of-line, whitespace, or an opening
    # bracket or dash; closing everywhere else.
    text = re.sub(r'(?<![^\s([{—–-])"', "“", text)
    text = text.replace('"', "”")
    # Single quotes / apostrophes.
    text = re.sub(rf"(?<=[0-9A-Za-zÀ-ɏ{ed.apostrophe_after}])'", "’", text)
    text = text.replace("'", "‘")
    # Ellipsis and ranges.
    text = text.replace("...", "…")
    return text


def inline(text: str, hy=None) -> str:
    """Markdown inline markup -> HTML. Escapes first; source has no raw HTML."""
    text = html.escape(text, quote=False)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text, flags=re.S)
    text = re.sub(r"(?<!\*)\*(?!\s)(.+?)(?<!\s)\*(?!\*)", r"<em>\1</em>", text, flags=re.S)
    if hy:
        text = hy(text)
    return text


def strip_tags(text: str) -> str:
    return re.sub(r"<[^>]+>", "", text)


def slug(title: str) -> str:
    """A section id that survives Turkish orthography."""
    # İ.lower() is i + U+0307 in Python; drop the combining dot first.
    folded = title.lower().replace("̇", "").translate(str.maketrans({
        "ı": "i", "ş": "s", "ğ": "g", "ç": "c", "ö": "o", "ü": "u",
        "â": "a", "ê": "e", "î": "i", "ô": "o", "û": "u",
        "ā": "a", "ē": "e", "ī": "i", "ō": "o", "ū": "u",
        "’": "", "‘": "",
    }))
    return "s" + re.sub(r"[^a-z0-9]+", "-", folded).strip("-")


# ------------------------------------------------------------------- parsing

def split_notes(md: str, marker: str):
    i = md.index(marker)
    body, notes_md = md[:i], md[i + len(marker):]
    notes = {}
    for m in re.finditer(r"^\[\^(\d+)\]:[ \t]*(.*)$", notes_md, re.M):
        notes[int(m.group(1))] = m.group(2).strip()
    return body, notes


def blocks(section_md: str):
    """Split a section body into (kind, payload) blocks."""
    out = []
    lines = section_md.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line.strip() == "---":
            out.append(("hr", None))
            i += 1
            continue
        m = re.match(r"^(#{3,4})\s+(.*)$", line)
        if m:
            out.append(("h" + str(len(m.group(1))), m.group(2).strip()))
            i += 1
            continue
        if line.lstrip().startswith("|"):
            rows = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                rows.append(lines[i].strip())
                i += 1
            out.append(("table", rows))
            continue
        para = [line]
        i += 1
        while i < len(lines) and lines[i].strip() and not lines[i].lstrip().startswith("|") \
                and lines[i].strip() != "---" and not re.match(r"^#{3,4}\s", lines[i]):
            para.append(lines[i])
            i += 1
        out.append(("p", " ".join(x.strip() for x in para)))
    # A rule that opens or closes a section is a source-file separator, not an
    # ornament: it would print as a lone asterisk on an otherwise empty page.
    while out and out[0][0] == "hr":
        out.pop(0)
    while out and out[-1][0] == "hr":
        out.pop()
    return out


def parse_table(rows):
    cells = [[c.strip() for c in r.strip("|").split("|")] for r in rows]
    header = cells[0]
    body = [r for r in cells[1:] if not all(set(c) <= set("-: ") for c in r)]
    return header, body


# ------------------------------------------------------------------ rendering

class Renderer:
    def __init__(self, notes, hy=None):
        self.notes = notes
        self.hy = hy
        self.ref_seen = {}      # note number -> anchor id of its reference
        self.counter = 0

    def refs(self, text: str) -> str:
        """Replace [^N] with a superscript link to the endnote."""
        def sub(m):
            n = int(m.group(1))
            self.counter += 1
            rid = f"r{n}"
            self.ref_seen.setdefault(n, rid)
            return (f'<sup class="nref"><a id="{rid}" href="#n{n}">'
                    f'{n}</a></sup>')
        return re.sub(r"\[\^(\d+)\]", sub, text)

    def para(self, text: str, cls=None) -> str:
        c = f' class="{cls}"' if cls else ""
        return f"<p{c}>{self.refs(inline(text, self.hy))}</p>"

    def opener(self, text: str) -> str:
        """First paragraph of a section: drop capital, opening in small caps."""
        body = self.refs(inline(text, self.hy))
        # Take the first few words for the small-caps lead-in, but never
        # break inside a tag.
        plain = strip_tags(body)
        words = plain.split()
        lead_n = 4 if len(words) > 12 else 2
        lead_words = words[:lead_n]
        # Rebuild by walking the marked-up string and counting plain words.
        target = " ".join(lead_words)
        cut = 0
        seen = ""
        in_tag = False
        for idx, ch in enumerate(body):
            if ch == "<":
                in_tag = True
            elif ch == ">":
                in_tag = False
            elif not in_tag:
                seen += ch
            if seen.strip() == target:
                cut = idx + 1
                break
        if not cut:
            cut = len(lead_words[0]) if lead_words else 0
        lead, rest = body[:cut], body[cut:]
        first, lead = lead[0], lead[1:]
        return (f'<p class="opener"><span class="dropcap">{first}</span>'
                f'<span class="lead">{lead}</span>{rest}</p>')

    def entries(self, header, rows) -> str:
        """A table whose last column is prose reads better as entry blocks."""
        out = ['<div class="entries">']
        for row in rows:
            labels = [c for c in row[:-1] if c and c not in {"—", "-"}]
            head = " · ".join(labels)
            out.append('<div class="entry">')
            if head:
                out.append(f'<p class="ehead">{self.refs(inline(head))}</p>')
            out.append(f'<p class="ebody">{self.refs(inline(row[-1], self.hy))}</p>')
            out.append("</div>")
        out.append("</div>")
        return "\n".join(out)

    def table(self, rows) -> str:
        header, body = parse_table(rows)
        widest = max((len(r[-1]) for r in body), default=0)
        if len(header) <= 4 and widest > 90:
            return self.entries(header, body)
        cells = "".join(f"<th>{inline(c)}</th>" for c in header)
        out = [f'<table><thead><tr>{cells}</tr></thead><tbody>']
        for row in body:
            tds = "".join(f"<td>{self.refs(inline(c, self.hy))}</td>" for c in row)
            out.append(f"<tr>{tds}</tr>")
        out.append("</tbody></table>")
        return "\n".join(out)


# --------------------------------------------------------------------- figure

FIGURE = """
<figure class="plate">
<svg viewBox="0 0 640 462" xmlns="http://www.w3.org/2000/svg"
     role="img" aria-label="{aria}">
  <defs>
    <pattern id="sand" width="7" height="7" patternUnits="userSpaceOnUse"
             patternTransform="rotate(35)">
      <line x1="0" y1="0" x2="0" y2="7" stroke="#000" stroke-width=".45"
            opacity=".33"/>
    </pattern>
    <pattern id="rock" width="6" height="6" patternUnits="userSpaceOnUse"
             patternTransform="rotate(-40)">
      <line x1="0" y1="0" x2="0" y2="6" stroke="#000" stroke-width=".5"
            opacity=".42"/>
    </pattern>
  </defs>

  <!-- valley floor -->
  <path d="M96 84 C240 62 430 66 556 92 C572 150 574 268 552 342
           C420 366 232 364 108 340 C86 262 82 154 96 84 Z"
        fill="#fbf8f2" stroke="none"/>

  <!-- dark rock, north and east -->
  <path d="M96 84 C240 62 430 66 556 92 L566 56 C420 26 232 24 88 50 Z"
        fill="url(#rock)" stroke="#000" stroke-width=".7"/>
  <path d="M556 92 C572 150 574 268 552 342 L596 350 C616 264 614 148 598 60 Z"
        fill="url(#rock)" stroke="#000" stroke-width=".7"/>
  <!-- broken ground, south -->
  <path d="M108 340 C232 364 420 366 552 342 L558 380 C420 402 230 400 100 378 Z"
        fill="url(#rock)" stroke="#000" stroke-width=".7" opacity=".8"/>

  <!-- al-'Aqanqal: the wall of sand on the west -->
  <path d="M96 84 C60 150 56 268 108 340 L58 356 C14 268 18 148 52 66 Z"
        fill="url(#sand)" stroke="#000" stroke-width=".8"/>
  <path d="M108 340 C74 262 74 156 96 84" fill="none" stroke="#000"
        stroke-width="1.6"/>
  <!-- slip-face ticks, pointing down into the valley -->
  <g stroke="#000" stroke-width=".7">
    <path d="M98 110 l15 5M92 140 l16 4M88 170 l16 3M86 200 l16 2
             M86 230 l16 1M88 260 l16 0M92 290 l16 -2M99 316 l15 -3"/>
  </g>

  <!-- dune belt and hollows: the farther bank -->
  <g stroke="#000" stroke-width=".6" fill="none" opacity=".7">
    <path d="M122 150 c13 -7 29 -6 40 2"/>
    <path d="M118 196 c14 -7 30 -6 42 2"/>
    <path d="M118 242 c14 -7 30 -6 42 2"/>
    <path d="M122 288 c13 -7 29 -6 40 2"/>
  </g>

  <!-- braided channels of the wadi, running away west-north-west -->
  <g stroke="#000" stroke-width=".55" fill="none" opacity=".45">
    <path d="M520 158 C420 178 300 192 178 174"/>
    <path d="M522 180 C422 202 300 214 176 198"/>
    <path d="M518 202 C418 226 302 234 180 218"/>
  </g>

  <!-- the wells, north-eastern edge -->
  <g fill="#fff" stroke="#000" stroke-width="1">
    <circle cx="452" cy="120" r="4.2"/><circle cx="474" cy="136" r="4.2"/>
    <circle cx="492" cy="154" r="4.2"/><circle cx="506" cy="176" r="4.2"/>
    <circle cx="516" cy="200" r="4.2"/><circle cx="522" cy="226" r="4.2"/>
    <circle cx="524" cy="252" r="4.2"/>
  </g>
  <!-- wells broken in and filled with sand, on the Mecca approach -->
  <g stroke="#000" stroke-width="1">
    <circle cx="300" cy="300" r="4.2" fill="url(#sand)"/>
    <circle cx="336" cy="308" r="4.2" fill="url(#sand)"/>
    <path d="M296 296 l8 8M304 296 l-8 8" stroke-width=".7"/>
    <path d="M332 304 l8 8M340 304 l-8 8" stroke-width=".7"/>
  </g>

  <!-- the Muslim line, on the firm nearer bank -->
  <path d="M424 148 C438 190 438 236 424 278" stroke="#000"
        stroke-width="2.8" fill="none"/>
  <!-- the cistern, behind the line -->
  <ellipse cx="466" cy="214" rx="11" ry="7" fill="#e8ecf1" stroke="#000"
           stroke-width=".9"/>
  <!-- the 'arish, on its low rise -->
  <g stroke="#000" stroke-width="1">
    <path d="M486 290 l9 -12 9 12 Z" fill="#fff"/>
    <path d="M478 294 q17 -7 34 0" stroke-width=".6" fill="none"
          opacity=".55"/>
  </g>

  <!-- the Qurayshi line, in the dune hollows -->
  <path d="M186 112 C170 176 170 250 186 316" stroke="#000"
        stroke-width="2.8" fill="none" stroke-dasharray="9 5"/>

  <!-- roads -->
  <g stroke="#000" stroke-width=".9" fill="none" stroke-dasharray="2.5 3.5">
    <path d="M600 96 C566 104 548 112 528 124"/>
    <path d="M52 352 C96 344 122 330 150 312"/>
  </g>
  <path d="M597 93 l-13 4 5 -9 Z" fill="#000"/>
  <path d="M52 352 l13 -4 -5 9 Z" fill="#000"/>

  <!-- keys -->
  <g stroke="#000" stroke-width=".7" fill="none">
    <path d="M444 108 l6 6"/><path d="M480 208 l-8 4"/>
    <path d="M513 285 l-8 -1"/><path d="M312 320 l-8 -12"/>
    <path d="M324 320 l10 -6"/>
  </g>
  <g>
    <circle cx="438" cy="102" r="7.6" fill="#fff" stroke="#000"
            stroke-width=".8"/>
    <text x="438" y="105.4" text-anchor="middle" font-family="Garamond"
          font-size="8.6">1</text>
    <circle cx="487" cy="205" r="7.6" fill="#fff" stroke="#000"
            stroke-width=".8"/>
    <text x="487" y="208.4" text-anchor="middle" font-family="Garamond"
          font-size="8.6">2</text>
    <circle cx="520" cy="286" r="7.6" fill="#fff" stroke="#000"
            stroke-width=".8"/>
    <text x="520" y="289.4" text-anchor="middle" font-family="Garamond"
          font-size="8.6">3</text>
    <circle cx="318" cy="328" r="7.6" fill="#fff" stroke="#000"
            stroke-width=".8"/>
    <text x="318" y="331.4" text-anchor="middle" font-family="Garamond"
          font-size="8.6">4</text>
  </g>

  <!-- region labels, knocked out of the hatching so they read cleanly -->
  <rect x="278" y="35" width="94" height="16" fill="#fff"/>
  <text x="325" y="47" text-anchor="middle" font-family="Garamond"
        font-size="8" letter-spacing="1.5">{dark_rock}</text>
  <rect x="{broken_x}" y="381" width="{broken_w}" height="16" fill="#fff"/>
  <text x="330" y="393" text-anchor="middle" font-family="Garamond"
        font-size="8">{broken}</text>
  <rect x="24" y="{aqanqal_y}" width="16" height="{aqanqal_h}" fill="#fff"/>
  <text x="32" y="214" text-anchor="middle" font-family="Garamond"
        font-size="8" letter-spacing="2"
        transform="rotate(-90 32 214)">{aqanqal}</text>
  <rect x="76" y="358" width="{mecca_w}" height="16" fill="#fff"/>
  <text x="80" y="370" font-family="Garamond" font-size="8">{mecca}</text>
  <rect x="558" y="60" width="{medina_w}" height="16" fill="#fff"/>
  <text x="562" y="72" font-family="Garamond" font-size="8">{medina}</text>

  <!-- the two lines, named where they stood -->
  <text x="212" y="120" font-family="Garamond" font-size="8.6">{quraysh}</text>
  <path d="M210 124 l-22 8" stroke="#000" stroke-width=".7" fill="none"/>
  <text x="408" y="120" text-anchor="end" font-family="Garamond"
        font-size="8.6">{muslims}</text>
  <path d="M412 124 l14 20" stroke="#000" stroke-width=".7" fill="none"/>
  <text x="300" y="258" text-anchor="middle" font-family="Garamond"
        font-size="8" font-style="italic">{wadi}</text>
  <text x="146" y="330" font-family="Garamond" font-size="7.6"
        font-style="italic">{dune}</text>
  <path d="M144 327 l-14 -22" stroke="#000" stroke-width=".7" fill="none"/>

  <!-- scale and compass, clear of the map -->
  <g transform="translate(96 424)">
    <path d="M0 0 h140" stroke="#000" stroke-width="1"/>
    <path d="M0 -4 v8M70 -3 v6M140 -4 v8" stroke="#000" stroke-width="1"/>
    <text x="70" y="16" text-anchor="middle" font-family="Garamond"
          font-size="8">{scale}</text>
  </g>
  <g transform="translate(596 430)">
    <path d="M0 0 v-24" stroke="#000" stroke-width=".9"/>
    <path d="M0 -27 l-4.5 9 9 0 Z" fill="#000"/>
    <text x="0" y="11" text-anchor="middle" font-family="Garamond"
          font-size="8">{north}</text>
  </g>
</svg>
<p class="legend">{legend}</p>
<figcaption>{caption}</figcaption>
</figure>
"""


def figure(ed: Edition) -> str:
    labels = dict(ed.labels)
    if ed.hyphenate:
        labels["caption"] = ed.hyphenate(labels["caption"])
    return FIGURE.format(**labels)


# ----------------------------------------------------------------------- CSS

def css(ed: Edition) -> str:
    faces = []
    for name, weight, style in [
        ("EBGaramond-Regular", 400, "normal"),
        ("EBGaramond-Italic", 400, "italic"),
        ("EBGaramond-Medium", 500, "normal"),
        ("EBGaramond-MediumItalic", 500, "italic"),
        ("EBGaramond-SemiBold", 600, "normal"),
        ("EBGaramond-SemiBoldItalic", 600, "italic"),
        ("EBGaramond-Bold", 700, "normal"),
        ("EBGaramond-BoldItalic", 700, "italic"),
    ]:
        faces.append(
            "@font-face{font-family:Garamond;"
            f"src:url('file://{FONTS}/{name}.ttf');"
            f"font-weight:{weight};font-style:{style};font-display:block}}"
        )
    faces.append(
        "@font-face{font-family:Arabic;"
        f"src:url('file://{FONTS}/Amiri-Regular.ttf')}}"
    )

    # Tschichold's golden canon, margins 2:3:4:6 (inner:top:outer:bottom).
    U = 6.6  # mm
    inner, top, outer, bottom = 2 * U, 3 * U, 4 * U, 6 * U
    hyphens = ed.hyphens

    return "\n".join(faces) + f"""
@page {{
  size: 148mm 210mm;
  margin: {top}mm {outer}mm {bottom}mm {inner}mm;
  @bottom-center {{
    content: counter(page);
    font: 400 9.5pt Garamond; color: #111;
    font-feature-settings: "onum";
    margin-top: 8mm;
  }}
}}
@page :left {{
  margin-left: {outer}mm; margin-right: {inner}mm;
  @top-left {{
    content: string(booktitle);
    font: 400 8.2pt Garamond; color: #333;
    font-variant-caps: small-caps; letter-spacing: .07em;
    margin-bottom: 7mm;
  }}
}}
@page :right {{
  @top-right {{
    content: string(section);
    font: 400 8.2pt Garamond; color: #333;
    font-variant-caps: small-caps; letter-spacing: .07em;
    margin-bottom: 7mm;
  }}
}}
@page front {{ @top-left {{content: none}} @top-right {{content: none}}
  @bottom-center {{content: counter(page, lower-roman)}} }}
/* Half-title, title and title verso are counted but never numbered, as in
   any printed book: the folio first shows itself on the contents page. */
@page display {{
  @top-left {{content: none}} @top-right {{content: none}}
  @bottom-center {{content: none}}
}}
@page plate {{ @top-left {{content:none}} @top-right {{content:none}} }}
/* A section's opening page carries no running head: the title is already
   there, set below it. */
@page opening {{ @top-left {{content:none}} @top-right {{content:none}} }}
/* The page counter restarts at the first narrative section. Scoped to that
   one heading's page, since a named page rule applies to every page of
   its type and would otherwise reset the count on every leaf. */
@page bodystart {{
  counter-reset: page 1;
  @top-left {{content: none}} @top-right {{content: none}}
}}
/* Blank versos forced by recto starts carry no furniture at all. Each
   named page needs its own :blank, a named page outranking the bare
   pseudo-class. */
@page :blank, front:blank, display:blank, plate:blank, bodystart:blank {{
  @top-left {{content: none}} @top-right {{content: none}}
  @bottom-center {{content: none}}
}}

html {{
  font: 400 10.4pt/1.44 Garamond, Arabic, serif;
  color: #111;
  font-feature-settings: "onum", "kern", "liga";
  text-rendering: geometricPrecision;
}}
body {{ margin: 0 }}

p {{
  margin: 0; text-align: justify; text-indent: 1.15em;
  hyphens: {hyphens}; hyphenate-limit-chars: 7 3 3;
  orphans: 2; widows: 2;
}}
em {{ font-style: italic }}
strong {{ font-weight: 600 }}
.nobr {{ white-space: nowrap }}

/* ---- front matter ---- */
.front {{ page: front }}
.leaf {{ break-before: right }}
/* The colophon takes the title verso, as it does in a printed book. */
.verso {{ break-before: page }}
/* Half-title, title and title verso are unnumbered; the contents keeps its
   roman folio. */
.halftitle, .titlepage, .colophon {{ page: display }}
.halftitle {{ padding-top: 34mm; text-align: center }}
.halftitle .t {{
  font-variant-caps: small-caps; letter-spacing: .3em; font-size: 13pt;
}}
.titlepage {{ padding-top: 22mm; text-align: center }}
.titlepage h1 {{
  font-weight: 400; font-size: 25pt; line-height: 1.16; margin: 0;
  font-variant-caps: small-caps; letter-spacing: .085em;
  string-set: booktitle content(text);
}}
.titlepage .sub {{
  margin-top: 7mm; font-size: 10.5pt; font-style: italic; color: #333;
  text-indent: 0; text-align: center;
}}
.rule {{
  width: 34mm; height: 0; margin: 9mm auto;
  border-top: .6pt solid #333;
}}
.rule.sm {{ width: 20mm; margin: 6mm auto }}
.titlepage .imprint {{
  margin-top: 30mm; font-size: 9pt; color: #444; text-indent: 0;
  text-align: center; font-variant-caps: small-caps; letter-spacing: .12em;
}}
.colophon {{ font-size: 9.2pt; color: #333 }}
.colophon p {{ text-indent: 0; margin-bottom: .7em; text-align: left }}
.colophon h2 {{
  font-size: 9.2pt; font-weight: 400; font-variant-caps: small-caps;
  letter-spacing: .12em; margin: 0 0 1.4em 0; text-align: left;
}}

/* ---- contents ---- */
.contents {{ break-before: right }}
.contents h2 {{
  font-weight: 400; font-size: 11pt; font-variant-caps: small-caps;
  letter-spacing: .2em; text-align: center; margin: 0 0 12mm 0;
}}
.toc {{ list-style: none; margin: 0; padding: 0 }}
.toc li {{ margin-bottom: .52em; font-size: 10.2pt }}
.toc li.grp {{ margin-top: 1.5em }}
.toc a {{ color: #111; text-decoration: none }}
.toc a::after {{
  content: leader(". ") target-counter(attr(href), page);
  font-feature-settings: "onum";
}}
.toc .sc {{ font-variant-caps: small-caps; letter-spacing: .05em }}

/* ---- sections ---- */
section {{ break-before: page }}
section.recto {{ break-before: right }}
section.first {{ break-before: right }}
/* Only the opening heading's own page restarts the arabic numbering. */
section.first > h2.sec {{ page: bodystart }}
section:not(.first) > h2.sec {{ page: opening }}
h2.sec {{
  string-set: section content(text);
  font-weight: 400; font-size: 12.5pt;
  font-variant-caps: small-caps; letter-spacing: .16em;
  text-align: center; text-indent: 0;
  margin: 0 0 11mm 0; padding-top: 16mm;
  break-after: avoid;
}}
h3 {{
  font-weight: 400; font-size: 10.4pt; font-style: italic;
  text-align: left; text-indent: 0;
  margin: 1.6em 0 .5em; break-after: avoid;
}}
h4 {{
  font-weight: 400; font-size: 9.4pt; text-indent: 0;
  font-variant-caps: small-caps; letter-spacing: .1em;
  margin: 1.4em 0 .45em; break-after: avoid;
}}
.opener {{ text-indent: 0; overflow: hidden }}
.dropcap {{
  float: left; font-size: 3.42em; line-height: .84;
  margin: .02em .07em -.06em 0; font-weight: 400;
}}
.lead {{ font-variant-caps: small-caps; letter-spacing: .045em }}
hr {{
  border: 0; margin: 1.5em auto; width: 100%;
  text-align: center;
  break-before: avoid; break-after: avoid;
}}
hr::after {{
  content: "\\2733"; font-size: 7.5pt; color: #555;
}}

/* ---- note references ---- */
.nref {{ font-size: .62em; line-height: 0; vertical-align: super }}
.nref a {{ color: #111; text-decoration: none;
  font-feature-settings: "lnum" }}

/* ---- entry lists (rosters, casualty lists, chronology) ---- */
.entries {{ margin: .8em 0 }}
.entry {{ margin-bottom: .62em; break-inside: avoid }}
.ehead {{
  text-indent: 0; text-align: left; margin: 0;
  font-size: 9.5pt; font-variant-caps: small-caps; letter-spacing: .055em;
  color: #000;
}}
.ehead strong {{ font-weight: 600 }}
.ebody {{
  text-indent: 0; margin: 0 0 0 5mm; font-size: 9.9pt;
  text-align: justify;
}}
.roster p {{ text-indent: 0; margin-bottom: .62em; font-size: 9.9pt }}
.roster strong:first-child {{
  font-variant-caps: small-caps; letter-spacing: .05em; font-weight: 600;
}}
.gloss p {{ text-indent: 0; margin-bottom: .62em; font-size: 9.9pt }}

table {{
  width: 100%; border-collapse: collapse; margin: .9em 0;
  font-size: 9.2pt;
}}
th {{
  text-align: left; font-weight: 400; font-size: 8.4pt;
  font-variant-caps: small-caps; letter-spacing: .08em;
  border-bottom: .5pt solid #444; padding: 0 .5em .3em 0;
}}
td {{ padding: .3em .5em .3em 0; vertical-align: top;
  border-bottom: .3pt solid #ddd }}

/* ---- figure ---- */
.plate {{ page: plate; break-before: page; margin: 0; padding-top: 22mm }}
.plate svg {{ width: 100%; height: auto }}
.plate svg text {{ fill: #000; font-feature-settings: "lnum" }}
.legend {{
  text-indent: 0; margin: 4.5mm 0 0; font-size: 8.2pt; line-height: 1.45;
  text-align: center; color: #222;
}}
.legend .k {{
  font-feature-settings: "lnum"; font-size: 7.6pt;
  border: .4pt solid #444; border-radius: 50%;
  padding: .06em .34em .1em; margin-right: .1em;
}}
.legend em {{ font-style: italic }}
figcaption {{
  margin-top: 4.5mm; font-size: 8.6pt; line-height: 1.4; color: #333;
  text-align: justify; hyphens: {hyphens};
}}

/* ---- endnotes ---- */
.notes {{ break-before: right; font-size: 9pt; line-height: 1.4 }}
.notes h2.sec {{ font-size: 12.5pt }}
.notes h3 {{
  font-size: 8.6pt; font-style: normal; font-variant-caps: small-caps;
  letter-spacing: .12em; color: #333; margin: 1.5em 0 .6em;
}}
.note {{
  text-indent: 0; margin-bottom: .5em; padding-left: 6.5mm;
  text-align: justify;
}}
.note .num {{
  display: inline-block; width: 6.5mm; margin-left: -6.5mm;
  font-feature-settings: "lnum";
}}
.note .back {{ color: #555; white-space: nowrap }}
.note .back a {{ color: #555; text-decoration: none }}
.note .back a::after {{
  content: target-counter(attr(href), page);
  font-feature-settings: "onum";
}}
"""


# ----------------------------------------------------------------- assembly

def build_html(ed: Edition) -> str:
    md = ed.path.read_text(encoding="utf-8")
    md = smarten(md, ed)
    body_md, notes = split_notes(md, ed.notes_marker)

    # Drop the H1; split on H2.
    body_md = re.sub(r"^#\s+.*$", "", body_md, count=1, flags=re.M)
    parts = re.split(r"^##\s+(.*)$", body_md, flags=re.M)
    sections = [(parts[i].strip(), parts[i + 1]) for i in range(1, len(parts), 2)]

    r = Renderer(notes, ed.hyphenate)
    narrative, back = [], []
    toc_narr, toc_back = [], []

    for idx, (title, content) in enumerate(sections):
        is_back = title in ed.back_matter
        sid = slug(title)
        cls = ["recto"] if is_back else []
        if idx == 0:
            cls = ["first"]
        head = ed.running.get(title, title)
        out = [f'<section id="{sid}" class="{" ".join(cls)}">',
               f'<h2 class="sec">{inline(head)}</h2>']

        bs = blocks(content)
        first_para = True
        wrap = None
        if title in ed.roster:
            wrap = "roster"
        elif title in ed.gloss:
            wrap = "gloss"
        if wrap:
            out.append(f'<div class="{wrap}">')
        for kind, payload in bs:
            if kind == "p":
                if first_para and not is_back and not wrap:
                    out.append(r.opener(payload))
                    first_para = False
                else:
                    out.append(r.para(payload))
            elif kind == "table":
                out.append(r.table(payload))
            elif kind == "hr":
                out.append("<hr>")
            elif kind == "h3":
                out.append(f"<h3>{inline(payload)}</h3>")
            elif kind == "h4":
                out.append(f"<h4>{inline(payload)}</h4>")
        if wrap:
            out.append("</div>")
        out.append("</section>")

        # The schematic belongs with the section that describes the ground.
        if title == ed.figure_after:
            out.append(figure(ed))

        (back if is_back else narrative).append("\n".join(out))
        entry = (f'<li><a href="#{sid}">{inline(head)}</a></li>')
        (toc_back if is_back else toc_narr).append(entry)

    # Endnotes, grouped under the section each note falls in.
    note_sections = []
    for n in sorted(notes):
        note_sections.append(n)
    notes_html = ['<section id="notes" class="notes">',
                  f'<h2 class="sec">{ed.notes}</h2>']
    for n in note_sections:
        rid = r.ref_seen.get(n)
        backlink = (f' <span class="back">(<a href="#{rid}">{ed.page_abbr}</a>)</span>'
                    if rid else "")
        notes_html.append(
            f'<p class="note" id="n{n}"><span class="num">{n}</span>'
            f'{inline(notes[n], ed.hyphenate)}{backlink}</p>'
        )
    notes_html.append("</section>")
    toc_back.append(f'<li><a href="#notes">{ed.notes}</a></li>')

    toc = ('<ul class="toc">' + "".join(toc_narr) +
           '<li class="grp"></li>' + "".join(toc_back) + "</ul>")

    colophon = "\n".join(f"    <p>{p}</p>" for p in ed.colophon)

    front = f"""
<div class="front">
  <div class="leaf halftitle"><p class="t">{ed.title}</p></div>
  <div class="leaf titlepage">
    <h1>{ed.title}</h1>
    <div class="rule"></div>
    <p class="sub">{ed.subtitle}</p>
    <p class="imprint">{ed.imprint}</p>
  </div>
  <div class="verso colophon">
    <h2>{ed.colophon_head}</h2>
{colophon}
  </div>
  <div class="leaf contents">
    <h2>{ed.contents}</h2>
    {toc}
  </div>
</div>
"""

    return f"""<!DOCTYPE html>
<html lang="{ed.lang}"><head><meta charset="utf-8">
<title>{ed.title}</title><style>{css(ed)}</style></head>
<body>
{front}
{''.join(narrative)}
{''.join(back)}
{''.join(notes_html)}
</body></html>
"""


# ---------------------------------------------------------------- imposition

def impose(src_pdf: Path, out_pdf: Path, sheets_per_sig=8):
    """2-up saddle-stitch imposition on A4 landscape, in signatures."""
    from pypdf import PdfWriter, PdfReader, Transformation
    from pypdf.generic import RectangleObject

    reader = PdfReader(str(src_pdf))
    n = len(reader.pages)
    per_sig = sheets_per_sig * 4
    # Pad to a multiple of 4.
    total = ((n + 3) // 4) * 4

    A4_W, A4_H = 841.89, 595.276          # A4 landscape, points
    A5_W, A5_H = 419.528, 595.276

    writer = PdfWriter()
    order = []
    for start in range(0, total, per_sig):
        end = min(start + per_sig, total)
        lo, hi = start, end - 1
        while lo < hi:
            order.append((hi, lo))       # front of sheet: last | first
            order.append((lo + 1, hi - 1))  # back of sheet
            lo, hi = lo + 2, hi - 2

    def page(i):
        return reader.pages[i] if i < n else None

    for left_i, right_i in order:
        sheet = writer.add_blank_page(width=A4_W, height=A4_H)
        for slot, idx in ((0, left_i), (1, right_i)):
            p = page(idx)
            if p is None:
                continue
            box = p.mediabox
            sx = A5_W / float(box.width)
            sy = A5_H / float(box.height)
            s = min(sx, sy)
            dx = slot * A5_W + (A5_W - float(box.width) * s) / 2
            dy = (A5_H - float(box.height) * s) / 2
            t = Transformation().scale(s, s).translate(dx, dy)
            sheet.merge_transformed_page(p, t)
    writer.write(str(out_pdf))
    return total, len(order)


# --------------------------------------------------------------------- main

def main(code="en"):
    ed = EDITIONS[code]
    DIST.mkdir(exist_ok=True)
    name = "book.html" if ed.code == "en" else f"book.{ed.code}.html"
    html_path = BOOK / "build" / name
    html_path.write_text(build_html(ed), encoding="utf-8")

    from weasyprint import HTML
    a5 = DIST / f"{ed.stem}-A5.pdf"
    HTML(str(html_path)).write_pdf(str(a5))
    print(f"wrote {a5}")

    from pypdf import PdfReader
    n = len(PdfReader(str(a5)).pages)
    print(f"  {n} pages")

    booklet = DIST / f"{ed.stem}-{ed.booklet}-A4.pdf"
    total, sheets = impose(a5, booklet)
    print(f"wrote {booklet}\n  {total} book pages on {sheets} A4 sides")


if __name__ == "__main__":
    code = sys.argv[1] if len(sys.argv) > 1 else "en"
    if code not in EDITIONS:
        sys.exit(f"unknown edition {code!r}; expected one of {sorted(EDITIONS)}")
    main(code)
