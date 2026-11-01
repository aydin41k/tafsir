#!/usr/bin/env python3
"""Bölüm doğrulayıcı. Kullanım: python3 check.py s2 [s3 ...]  |  python3 check.py all"""
import re, sys, glob, os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

SPEC = {
 's1': dict(title='Yesrib\'in Yemi', lo=1300, hi=1500,
   first='Ebû Süfyân b. Harb, Bedir suyunun başına çömeldi ve parmaklarının arasında bir deve tersini ufaladı.',
   last='O ikindi Medine\'de emir dolaştırıldı ve bu, bir savaşa hazırlanma emri değildi.'),
 's2': dict(title='Üç Yüz On Üç', lo=1450, hi=1650,
   first='Damdam b. Amr el-Gıfârî, kulaklarını yardığı ve burnunu kanattığı bir devenin üstünde, semerinde ayağa dikilmiş ve gömleğini ters çevirmiş hâlde Mekke vadisine girdi.',
   last='Artık yolda iki kol vardı ve her biri hâlâ ötekinden başka bir şey arıyordu.'),
 's3': dict(title='Yelyel Vadisi', lo=1650, hi=1850,
   first='Bedir ovası, Suriye\'den gelen kervan yolunun denizden içeriye kıvrıldığı yerde, Medine\'nin yüz otuz kilometre kadar güneybatısında uzanıyordu.',
   last='Ramazan\'ın on altısında güneş battığında müslümanların arkasında su, Kureyş\'in arkasında bir kum tepesi vardı.'),
 's4': dict(title='Yağmur Gecesi', lo=1450, hi=1650,
   first='O gece yağmur yağdı.',
   last='Sonra saflar kapandı ve ondan sonra kimse bütününü göremedi.'),
 's5': dict(title='Boyunların Üstüne', lo=1650, hi=1850,
   first='Müslümanlar yerinden kımıldamadı.',
   last='Baş vadinin öte yakasına taşındı ve Hz. Peygamber\'in ayağına konuldu; o da bunun bu ümmetin Firavun\'u olduğunu söyledi.'),
 's6': dict(title='Kuyu ve Esirler', lo=1650, hi=1850,
   first='O çukur, vadi tabanında göçmüş ve suyu çekilmiş eski bir kuyuydu.',
   last='Mekke\'de hiçbir kadının işitilebileceği bir yerde ağlamasına izin verilmiyordu.'),
 's7': dict(title='Bedir\'in Kırdığı', lo=1200, hi=1400,
   first='Ebû Süfyân kervanı Mekke\'ye getirdi ve sattı.',
   last='Arabistan\'da sonradan gelen her şey, karanlıkta bir kuyunun başında iki su bölüğünün karşılaşmasıyla başlayan bir çarpışmadan geldi.'),
}

MODERN = r'moral|lojistik|istihbarat|strateji|propaganda|finanse|organize|koordinasyon|motivasyon|pozisyon|operasyon|kapasite'
CLICHE = r'tarih onu hatırla|gerisi tarihtir|oyunun kurallar|az sonra ne olacağını'
# İmlâ tuzakları: (yanlış, doğru)
SPELL = [(r'\bSüfyan\b','Süfyân'), (r'\bVakıdî\b|\bVâkidî\b','Vâkıdî'), (r'\bİshâk\b','İshak'),
         (r'\bEbû Bekr\b','Ebû Bekir'), (r'\bSad b\.','Sa\'d b.'), (r'\bMusab\b','Mus\'ab'),
         (r'\bKureyş̧','Kureyş'), (r'\bYatrib\b|\bYesrîb\b','Yesrib'), (r'\bMuaz\b','Muâz'),
         (r'\bMedîne\b','Medine'), (r'\bMekka\b|\bMekke\b(?=[a-zâîû])','Mekke'), (r'\bİbn Sad\b','İbn Sa\'d'),
         (r'\bTaberi\b','Taberî'), (r'\bBuhari\b','Buhârî'), (r'\bKesir\b','Kesîr')]

def check(sec):
    sp = SPEC[sec]; f = sec + '.md'
    if not os.path.exists(f):
        print(f'{sec}: DOSYA YOK'); return False
    t = open(f).read()
    lines = t.split('\n')
    body = [l for l in lines if l.strip() and not l.startswith('#')]
    words = len(' '.join(body).split())
    ok = True
    def bad(m):
        nonlocal ok; ok = False; print(f'  HATA  {m}')
    def good(m): print(f'  ok    {m}')

    print(f'\n=== {sec} ===')
    # kelime
    (good if sp['lo'] <= words <= sp['hi'] else bad)(f'kelime {words} (hedef {sp["lo"]}-{sp["hi"]})')
    # başlık
    heads = [l for l in lines if l.startswith('#')]
    exp = ['# Furkān Günü - Bedir Savaşı', f'## {sp["title"]}'] if sec == 's1' else [f'## {sp["title"]}']
    (good if heads == exp else bad)(f'başlıklar {heads}')
    # sabit cümleler
    (good if body[0].startswith(sp['first']) else bad)('sabit ilk cümle')
    (good if body[-1].rstrip().endswith(sp['last']) else bad)('sabit son cümle')
    # çizgi
    n = t.count('—') + t.count('–')
    (good if n == 0 else bad)(f'uzun/orta çizgi sayısı {n}')
    # apparatus
    (good if '[^' not in t else bad)('dipnot işareti yok')
    (good if not [l for l in lines if l.startswith('|')] else bad)('tablo yok')
    (good if not [l for l in lines if re.match(r'^\s*([-*+] |[0-9]+\. )', l)] else bad)('madde imi yok')
    (good if not [l for l in lines if l.startswith('###')] else bad)('alt başlık yok')
    # kelime yasakları
    for pat, name in ((MODERN,'modern kelime'), (CLICHE,'klişe')):
        hits = sorted(set(m.group(0) for m in re.finditer(pat, t, re.I)))
        (good if not hits else bad)(f'{name}: {hits or "yok"}')
    # imlâ
    for pat, right in SPELL:
        hits = sorted(set(m.group(0) for m in re.finditer(pat, t)))
        if hits: bad(f'imlâ: {hits} -> {right}')
    # ﷺ bir kez
    g = t.count('ﷺ')
    (good if g == 1 else bad)(f'ﷺ sayısı {g} (tam 1 olmalı)')
    # paragraf uzunluğu
    longp = [(i, len(p.split())) for i, p in enumerate(body, 1) if len(p.split()) > 170]
    shortp = [(i, len(p.split())) for i, p in enumerate(body, 1) if len(p.split()) < 85]
    if longp: print(f'  not   170+ kelimelik paragraf: {longp}')
    if shortp: print(f'  not   85- kelimelik paragraf (ağırlık cümlesi olabilir): {shortp}')
    print(f'  {"GEÇTİ" if ok else "GEÇMEDİ"}  ({len(body)} paragraf)')
    return ok

args = sys.argv[1:] or ['all']
secs = sorted(SPEC) if args == ['all'] else args
secs = [s for s in secs if os.path.exists(s + '.md')] if args == ['all'] else secs
allok = all([check(s) for s in secs])
tot = sum(len(' '.join(l for l in open(s+'.md').read().split('\n') if l.strip() and not l.startswith('#')).split()) for s in secs if os.path.exists(s+'.md'))
print(f'\nTOPLAM {tot} kelime / {len(secs)} bölüm')
sys.exit(0 if allok else 1)
