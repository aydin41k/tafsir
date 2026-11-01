#!/usr/bin/env python3
"""furkan-gunu.md dosyasından Word belgesi üretir: furkan-gunu.docx

Dışa bağımlılığı yoktur: .docx bir zip içinde OOXML olduğu için yalnız zipfile
kullanılır. Bu makinede pandoc, libreoffice ve python-docx yok; olsalar da
aradaki çevirici kendi biçim kararlarını getirir. Burada tertip elle kuruldu.

Sayfa A5, yani kitabın okuma baskısıyla aynı kesim. A4'e çevirmek için aşağıdaki
PAGE ölçülerini değiştirmek kâfidir.

Kullanım: python3 docx.py
"""
import os, re, sys, zipfile
from xml.sax.saxutils import escape

os.chdir(os.path.dirname(os.path.abspath(__file__)))

SRC = 'furkan-gunu.md'
OUT = 'furkan-gunu.docx'

TITLE = 'Furkān Günü'
SUBTITLE = 'Bedir Savaşı, 17 Ramazan 2 (hicrî)'
IMPRINT = 'Husûsî okuma için hazırlanmıştır'
DATE = '2026-08-08T00:00:00Z'

FONT = 'Cambria'        # Word ile birlikte gelir, Türkçe harfleri tamdır
ARFONT = 'Amiri'        # ﷺ için; kurulu değilse Word kendi yerine koyar
SIZE = 21               # yarım punto: 10,5 punto
LINE = 264              # satır aralığı, otomatik ölçekli

# A5 = 148 x 210 mm. 1 mm = 56,6929 twip.
PAGE_W, PAGE_H = 8391, 11906
MARGIN = 964            # 17 mm yan
MARGIN_T, MARGIN_B = 1020, 1134

if not os.path.exists(SRC):
    sys.exit(f'{SRC} yok; önce build.py çalıştırılmalı')

# --- markdown'ı böl -----------------------------------------------------------
book_title, chapters, cur = None, [], None
for line in open(SRC).read().split('\n'):
    if line.startswith('# '):
        book_title = line[2:].strip()
    elif line.startswith('## '):
        cur = (line[3:].strip(), [])
        chapters.append(cur)
    elif line.strip():
        if cur is None:
            sys.exit('bölüm başlığından önce metin var; dosya bozuk')
        cur[1].append(line.strip())
if not chapters:
    sys.exit('bölüm bulunamadı')

# --- tipografi ---------------------------------------------------------------
def curl_double(t):
    """Düz " işaretini dönüşümlü olarak “ ve ” yapar. Metinde tırnaklar
    dengeli olduğu için (check.py yokluyor) bu güvenlidir."""
    out, opening = [], True
    for ch in t:
        if ch == '"':
            out.append('“' if opening else '”')
            opening = not opening
        else:
            out.append(ch)
    return ''.join(out)

def curl_single(t):
    """Kesme işaretini, ayn'ı ve iç alıntıyı birbirinden ayırır.

    Bir işarete üç iş yüklenmiştir ve üçü ayrı görünmelidir:
      iki harf arasındaki kesme (Medine'nin, Sa'd, Ümmü'l-Fazl)  ->  ’
      kelime sonundaki ayn (Mihca', Ebû Râfi')                   ->  ’
      iç alıntı ('sen ve Rabbin gidip savaşın')                  ->  ‘ … ’

    Ayrımı dönüşümle yapmak yanlıştır: kelime sonundaki ayn sırayı kaydırır ve
    kendisinden sonraki ilk kesmeyi açılış tırnağı yapar. Doğru ölçü şudur: bir
    işaret ancak boşluktan sonra gelip harfle devam ediyorsa alıntı açar, ve
    ancak açık bir alıntı varken kapatır. Geri kalanların hepsi kesme yahut
    ayn'dır ve hepsi ’ ile yazılır.
    """
    t = re.sub(r"(?<=\w)'(?=\w)", '’', t)
    out, pending = [], False
    for i, ch in enumerate(t):
        if ch != "'":
            out.append(ch)
            continue
        prev = t[i - 1] if i else ' '
        nxt = t[i + 1] if i + 1 < len(t) else ' '
        if not pending and prev.isspace() and nxt.isalpha():
            out.append('‘')
            pending = True
        else:
            out.append('’')
            pending = False
    return ''.join(out)

def runs(t):
    """Paragrafı run'lara böler: *italik* ve ﷺ ayrı run olur."""
    t = curl_single(curl_double(t))
    parts, pos = [], 0
    for m in re.finditer(r'\*([^*\n]+)\*', t):
        if m.start() > pos:
            parts.append((t[pos:m.start()], False))
        parts.append((m.group(1), True))
        pos = m.end()
    if pos < len(t):
        parts.append((t[pos:], False))

    xml = []
    for txt, italic in parts:
        # ﷺ kendi run'ında dursun ki yazı tipi ona verilebilsin
        for piece in re.split(r'(ﷺ)', txt):
            if not piece:
                continue
            rpr = []
            if piece == 'ﷺ':
                rpr.append(f'<w:rFonts w:ascii="{ARFONT}" w:hAnsi="{ARFONT}" '
                           f'w:cs="{ARFONT}"/>')
            if italic:
                rpr.append('<w:i/>')
            rprx = f'<w:rPr>{"".join(rpr)}</w:rPr>' if rpr else ''
            xml.append(f'<w:r>{rprx}<w:t xml:space="preserve">'
                       f'{escape(piece)}</w:t></w:r>')
    return ''.join(xml)

def para(style, text=None, raw=None):
    inner = raw if raw is not None else (runs(text) if text else '')
    return f'<w:p><w:pPr><w:pStyle w:val="{style}"/></w:pPr>{inner}</w:p>'

# --- gövde -------------------------------------------------------------------
body = [
    para('KitapAdi', book_title or TITLE),
    para('AltBaslik', SUBTITLE),
    para('Kunye', IMPRINT),
    para('Baslik1', 'İçindekiler'),
]
body += [para('Icindekiler', t) for t, _ in chapters]
for title, paras in chapters:
    body.append(para('Baslik1', title))
    for i, p in enumerate(paras):
        body.append(para('GovdeIlk' if i == 0 else 'Govde', p))

sect = f"""<w:sectPr>
  <w:footerReference w:type="default" r:id="rIdFtr"/>
  <w:footerReference w:type="first" r:id="rIdFtrF"/>
  <w:titlePg/>
  <w:pgSz w:w="{PAGE_W}" w:h="{PAGE_H}"/>
  <w:pgMar w:top="{MARGIN_T}" w:right="{MARGIN}" w:bottom="{MARGIN_B}"
           w:left="{MARGIN}" w:header="567" w:footer="567" w:gutter="0"/>
</w:sectPr>"""

NS = ('xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
      'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"')

document = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document {NS}>
<w:body>
{chr(10).join(body)}
{sect}
</w:body>
</w:document>"""

# --- üsluplar ----------------------------------------------------------------
def style(sid, name, ppr, rpr, based='Normal'):
    return f"""  <w:style w:type="paragraph" w:styleId="{sid}">
    <w:name w:val="{name}"/><w:basedOn w:val="{based}"/>
    <w:pPr>{ppr}</w:pPr><w:rPr>{rpr}</w:rPr>
  </w:style>"""

styles = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles {NS}>
  <w:docDefaults>
    <w:rPrDefault><w:rPr>
      <w:rFonts w:ascii="{FONT}" w:hAnsi="{FONT}" w:cs="{FONT}"/>
      <w:sz w:val="{SIZE}"/><w:szCs w:val="{SIZE}"/>
      <w:lang w:val="tr-TR"/>
    </w:rPr></w:rPrDefault>
    <w:pPrDefault><w:pPr>
      <w:spacing w:after="0" w:line="{LINE}" w:lineRule="auto"/>
      <w:jc w:val="both"/>
    </w:pPr></w:pPrDefault>
  </w:docDefaults>
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
    <w:name w:val="Normal"/>
  </w:style>
{style('KitapAdi', 'Kitap Adi',
       '<w:jc w:val="center"/><w:spacing w:before="2600" w:after="200" w:line="240" w:lineRule="auto"/>',
       '<w:sz w:val="40"/><w:szCs w:val="40"/>')}
{style('AltBaslik', 'Alt Baslik',
       '<w:jc w:val="center"/><w:spacing w:after="120"/>',
       '<w:i/><w:sz w:val="22"/>')}
{style('Kunye', 'Kunye',
       '<w:jc w:val="center"/><w:spacing w:before="2000"/>',
       '<w:sz w:val="18"/>')}
{style('Baslik1', 'heading 1',
       '<w:pageBreakBefore/><w:keepNext/><w:jc w:val="center"/>'
       '<w:spacing w:before="480" w:after="400" w:line="240" w:lineRule="auto"/>'
       '<w:outlineLvl w:val="0"/>',
       '<w:sz w:val="28"/><w:szCs w:val="28"/>')}
{style('Icindekiler', 'Icindekiler',
       '<w:jc w:val="center"/><w:spacing w:after="160"/>', '')}
{style('GovdeIlk', 'Govde Ilk', '<w:ind w:firstLine="0"/>', '')}
{style('Govde', 'Govde', '<w:ind w:firstLine="240"/>', '')}
  <w:style w:type="paragraph" w:styleId="Altbilgi">
    <w:name w:val="footer"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:jc w:val="center"/></w:pPr>
    <w:rPr><w:sz w:val="18"/></w:rPr>
  </w:style>
</w:styles>"""

# Sayfa numarası: PAGE alanı. İlk sayfada (başlık sayfası) numara yok.
footer = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:ftr {NS}>
  <w:p><w:pPr><w:pStyle w:val="Altbilgi"/></w:pPr>
    <w:r><w:fldChar w:fldCharType="begin"/></w:r>
    <w:r><w:instrText xml:space="preserve"> PAGE </w:instrText></w:r>
    <w:r><w:fldChar w:fldCharType="separate"/></w:r>
    <w:r><w:t>1</w:t></w:r>
    <w:r><w:fldChar w:fldCharType="end"/></w:r>
  </w:p>
</w:ftr>"""

footer_first = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:ftr {NS}><w:p><w:pPr><w:pStyle w:val="Altbilgi"/></w:pPr></w:p></w:ftr>"""

settings = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:settings {NS}>
  <w:zoom w:percent="100"/>
  <w:autoHyphenation w:val="true"/>
  <w:hyphenationZone w:val="284"/>
  <w:themeFontLang w:val="tr-TR"/>
</w:settings>"""

content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
  <Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>
  <Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/>
  <Override PartName="/word/footer2.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>"""

rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>"""

doc_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/>
  <Relationship Id="rIdFtr" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Target="footer1.xml"/>
  <Relationship Id="rIdFtrF" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Target="footer2.xml"/>
</Relationships>"""

core = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
  xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>{escape(TITLE)}</dc:title>
  <dc:subject>{escape(SUBTITLE)}</dc:subject>
  <dc:language>tr-TR</dc:language>
  <cp:revision>2</cp:revision>
  <dcterms:created xsi:type="dcterms:W3CDTF">{DATE}</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">{DATE}</dcterms:modified>
</cp:coreProperties>"""

words = sum(len(' '.join(p).split()) for _, p in chapters)
app = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"
  xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
  <Application>tr-book/v2/docx.py</Application>
  <Words>{words}</Words>
  <Paragraphs>{sum(len(p) for _, p in chapters)}</Paragraphs>
</Properties>"""

parts = [
    ('[Content_Types].xml', content_types),
    ('_rels/.rels', rels),
    ('docProps/core.xml', core),
    ('docProps/app.xml', app),
    ('word/document.xml', document),
    ('word/_rels/document.xml.rels', doc_rels),
    ('word/styles.xml', styles),
    ('word/settings.xml', settings),
    ('word/footer1.xml', footer),
    ('word/footer2.xml', footer_first),
]

with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as z:
    for name, txt in parts:
        z.writestr(name, txt)

print(f'{OUT} yazıldı ({os.path.getsize(OUT)/1024:.0f} KB)')
print(f'  kitap adı : {book_title}')
print(f'  bölüm     : {len(chapters)}')
print(f'  kelime    : {words}')
print(f'  sayfa     : A5 ({PAGE_W/56.6929:.0f} x {PAGE_H/56.6929:.0f} mm), '
      f'yazı {FONT} {SIZE/2:g} punto')
for i, (t, p) in enumerate(chapters, 1):
    print(f'    {i}. {t}  ({len(p)} paragraf)')
