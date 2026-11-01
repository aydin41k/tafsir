#!/usr/bin/env python3
"""furkan-gunu.md dosyasından Kindle için EPUB üretir: furkan-gunu.epub

Neden EPUB: Amazon MOBI'yi bıraktı. Send-to-Kindle bugün EPUB kabul ediyor ve
cihazda kendi biçimine kendisi çeviriyor. KPF/AZW3 istenirse Kindle Previewer
yahut calibre gerekir; ikisi de bu makinede yok, EPUB ise tam ve standarttır.

Dışa bağımlılığı yoktur: EPUB bir zip olduğu için yalnız zipfile kullanılır.

Kullanım: python3 kindle.py
"""
import os, re, sys, zipfile, html

os.chdir(os.path.dirname(os.path.abspath(__file__)))

SRC = 'furkan-gunu.md'
OUT = 'furkan-gunu.epub'

TITLE = 'Furkān Günü'
SUBTITLE = 'Bedir Savaşı, 17 Ramazan 2 (hicrî)'
IMPRINT = 'Husûsî okuma için hazırlanmıştır'
LANG = 'tr'
# Sabit kimlik: her derlemede aynı kalsın, yoksa cihaz kitabı yenisi sayar.
UID = 'urn:uuid:8f2c1a54-6b3d-4e77-9a10-furkan-gunu-v2'

if not os.path.exists(SRC):
    sys.exit(f'{SRC} yok; önce build.py çalıştırılmalı')

raw = open(SRC).read()

# --- markdown'ı böl: kitap adı (#) ve bölümler (##) ---------------------------
book_title = None
chapters = []          # (başlık, [paragraf, ...])
cur = None
for line in raw.split('\n'):
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

# --- markdown içi vurgu: yalnız *italik* kullanılıyor ------------------------
def inline(t):
    t = html.escape(t, quote=False)
    # kitapta tek biçim var: *furkān günü*
    t = re.sub(r'(?<!\*)\*([^*\n]+)\*(?!\*)', r'<em>\1</em>', t)
    return t

# Türkçe tırnak: düz " işareti dönüşümlü olarak “ ve ” olur. Söz açılışı ve
# kapanışı dönüşümlüdür; metinde tırnaklar dengeli olduğu için bu güvenlidir.
def curl(t):
    out, open_q = [], True
    for ch in t:
        if ch == '"':
            out.append('“' if open_q else '”')
            open_q = not open_q
        else:
            out.append(ch)
    return ''.join(out)

CSS = """@charset "utf-8";
/* Kindle kendi tipografisini uygular; burada yalnız yapı tarif edilir.
   Yazı tipi ve punto zorlanmaz, okuyucunun tercihi bozulmasın. */
body { margin: 0; padding: 0; text-align: justify; }
h1.book { text-align: center; font-size: 1.6em; font-weight: normal;
          margin: 3em 0 0.2em; line-height: 1.3; }
p.sub { text-align: center; font-style: italic; margin: 0.4em 0 0; }
p.imprint { text-align: center; font-size: 0.85em; margin: 3em 0 0; }
hr.rule { width: 30%; margin: 1.2em auto; border: 0; border-top: 1px solid; }
h2 { font-size: 1.25em; font-weight: normal; text-align: center;
     margin: 0 0 1.2em; page-break-before: always; line-height: 1.3; }
/* İlk paragraf girintisiz, sonrakiler girintili: klasik nesir tertibi. */
p { margin: 0; text-indent: 1.2em; }
p.first { text-indent: 0; }
nav ol { list-style: none; padding-left: 0; }
nav li { margin: 0.5em 0; }
"""

def chapter_xhtml(title, paras):
    body = []
    for i, p in enumerate(paras):
        cls = ' class="first"' if i == 0 else ''
        body.append(f'  <p{cls}>{inline(curl(p))}</p>')
    return f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="{LANG}" lang="{LANG}">
<head>
  <meta charset="utf-8"/>
  <title>{html.escape(title)}</title>
  <link rel="stylesheet" type="text/css" href="style.css"/>
</head>
<body>
  <h2>{html.escape(title)}</h2>
{chr(10).join(body)}
</body>
</html>
"""

titlepage = f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="{LANG}" lang="{LANG}">
<head>
  <meta charset="utf-8"/>
  <title>{html.escape(TITLE)}</title>
  <link rel="stylesheet" type="text/css" href="style.css"/>
</head>
<body>
  <h1 class="book">{html.escape(book_title or TITLE)}</h1>
  <hr class="rule"/>
  <p class="sub">{html.escape(SUBTITLE)}</p>
  <p class="imprint">{html.escape(IMPRINT)}</p>
</body>
</html>
"""

files = [('titlepage.xhtml', titlepage)]
for i, (title, paras) in enumerate(chapters, 1):
    files.append((f'ch{i:02d}.xhtml', chapter_xhtml(title, paras)))

# --- EPUB 3 gezinme (nav) ve EPUB 2 uyumu için NCX --------------------------
nav_items = '\n'.join(
    f'      <li><a href="ch{i:02d}.xhtml">{html.escape(t)}</a></li>'
    for i, (t, _) in enumerate(chapters, 1))
nav = f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops"
      xml:lang="{LANG}" lang="{LANG}">
<head><meta charset="utf-8"/><title>İçindekiler</title>
  <link rel="stylesheet" type="text/css" href="style.css"/></head>
<body>
  <nav epub:type="toc" id="toc">
    <h2>İçindekiler</h2>
    <ol>
{nav_items}
    </ol>
  </nav>
  <nav epub:type="landmarks" hidden="hidden">
    <ol><li><a epub:type="bodymatter" href="ch01.xhtml">Metin</a></li></ol>
  </nav>
</body>
</html>
"""

ncx_points = '\n'.join(
    f'    <navPoint id="n{i}" playOrder="{i}">\n'
    f'      <navLabel><text>{html.escape(t)}</text></navLabel>\n'
    f'      <content src="ch{i:02d}.xhtml"/>\n'
    f'    </navPoint>'
    for i, (t, _) in enumerate(chapters, 1))
ncx = f"""<?xml version="1.0" encoding="utf-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
  <head><meta name="dtb:uid" content="{UID}"/></head>
  <docTitle><text>{html.escape(TITLE)}</text></docTitle>
  <navMap>
{ncx_points}
  </navMap>
</ncx>
"""

manifest = '\n'.join(
    f'    <item id="{n.split(".")[0]}" href="{n}" media-type="application/xhtml+xml"/>'
    for n, _ in files)
spine = '\n'.join(f'    <itemref idref="{n.split(".")[0]}"/>' for n, _ in files)
opf = f"""<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="uid"
         xml:lang="{LANG}">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="uid">{UID}</dc:identifier>
    <dc:title id="t">{html.escape(TITLE)}</dc:title>
    <meta refines="#t" property="title-type">main</meta>
    <dc:title id="st">{html.escape(SUBTITLE)}</dc:title>
    <meta refines="#st" property="title-type">subtitle</meta>
    <dc:language>{LANG}</dc:language>
    <meta property="dcterms:modified">2026-08-08T00:00:00Z</meta>
    <meta property="ibooks:specified-fonts">false</meta>
  </metadata>
  <manifest>
    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
    <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>
    <item id="css" href="style.css" media-type="text/css"/>
{manifest}
  </manifest>
  <spine toc="ncx">
{spine}
  </spine>
</package>
"""

container = """<?xml version="1.0" encoding="utf-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>
"""

with zipfile.ZipFile(OUT, 'w') as z:
    # mimetype ilk giren ve sıkıştırılmamış olmak zorundadır: EPUB şartı.
    z.writestr(zipfile.ZipInfo('mimetype'), 'application/epub+zip',
               compress_type=zipfile.ZIP_STORED)
    z.writestr('META-INF/container.xml', container, zipfile.ZIP_DEFLATED)
    z.writestr('OEBPS/content.opf', opf, zipfile.ZIP_DEFLATED)
    z.writestr('OEBPS/nav.xhtml', nav, zipfile.ZIP_DEFLATED)
    z.writestr('OEBPS/toc.ncx', ncx, zipfile.ZIP_DEFLATED)
    z.writestr('OEBPS/style.css', CSS, zipfile.ZIP_DEFLATED)
    for name, txt in files:
        z.writestr('OEBPS/' + name, txt, zipfile.ZIP_DEFLATED)

words = sum(len(' '.join(p).split()) for _, p in chapters)
print(f'{OUT} yazıldı ({os.path.getsize(OUT)/1024:.0f} KB)')
print(f'  kitap adı : {book_title}')
print(f'  bölüm     : {len(chapters)}')
print(f'  kelime    : {words}')
print(f'  dosya     : {len(files)} xhtml + nav + ncx + css')
for i, (t, p) in enumerate(chapters, 1):
    print(f'    ch{i:02d}  {t}  ({len(p)} paragraf)')
