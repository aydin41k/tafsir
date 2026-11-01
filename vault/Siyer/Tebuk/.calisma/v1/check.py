#!/usr/bin/env python3
"""Bölüm doğrulayıcı. Kullanım: python3 check.py s2 [s3 ...]  |  python3 check.py all"""
import re, sys, glob, os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

SPEC = {
 's1': dict(title='Kuzeyden Gelen Haber', lo=1250, hi=1550,
   first="Sekizinci yılın sonunda Arabistan'ın hâli birkaç ay içinde değişmişti.",
   last="Ordunun yolunu kaynaklar anlatır; öteki yolu ise Ka'b'dan başka anlatan yoktur."),
 's2': dict(title='Darlık Ordusu', lo=1100, hi=1400,
   first="Tebük'e çağrı, Medine'nin alışık olmadığı bir açıklıkla yapıldı.",
   last='nihayet insanlar işi iyice ciddiye aldılar."'),
 's3': dict(title='Kuzeye Giden Yol', lo=1000, hi=1300,
   first="Ordu Medine'nin Şam tarafında, Seniyyetü'l-Vedâ denen tepede toplandı.",
   last="(Müslim'in rivayetinde: 'kendime bir örnek göremiyordum').\""),
 's4': dict(title='Tebük', lo=1300, hi=1550,
   first="Tebük'te bir pınar vardı ve ordu vardığında pınardan bir ayakkabı bağı inceliğinde su akıyordu.",
   last='hurmayı sadaka olarak veren oydu."'),
 's5': dict(title='Akabe Gecesi', lo=1150, hi=1400,
   first='Dönüş yolunda, Tebük ile Medine arasında, Arapların akabe dediği dar ve sarp bir geçit vardı.',
   last='sonra insanlar için otururdu."'),
 's6': dict(title='Elli Gece', lo=1000, hi=1400,
   first="Hz. Muhammed ﷺ Tebük'ten Ramazan 9'da (Aralık 630) döndü.",
   last="tevbemdendir.'\""),
 's7': dict(title='Darlık Saatinden Sonra', lo=1050, hi=1300,
   first="Abdullah b. Übey, Tebük'ten iki ay kadar sonra öldü.",
   last='helâk olmamamdan daha büyük hiçbir nimet vermedi."'),
 's8': dict(title='Kaynaklar', lo=900, hi=1600,
   first="Hamd, bize bu sayfaları yazmayı ve okumayı, Resûlullah'ın ve ashâbının o darlık saatini öğrenmeyi nasip eden Allah'adır.",
   last='diyerek şükretmektir.'),
}

MODERN = r'moral|lojistik|istihbarat|strateji|propaganda|finanse|organize|koordinasyon|motivasyon|pozisyon|operasyon|kapasite|travma|depresyon|psikoloj|\bego\b|boykot|Bizans'
WRONG = r'(?<!şehit )\b(aldı ve|o da|Mu.te.de|Yemâme.de) düş(tü|en)\b|tevbemin tamamı|geride bırakılan üç|elli birinci|hiçbir deftere sığ|Zû Evân.da indi|âyet\w*.{0,30}Zû Evân'
CLICHE = r'tarih onu hatırla|gerisi tarihtir|oyunun kurallar|az sonra ne olacağını|zaman durmuştu|kalbi yerinden'
# İmlâ tuzakları: (yanlış, doğru)
SPELL = [(r"\bKab\b|\bKâ'b\b|\bKa'ab\b", "Ka'b"), (r'\bMalik\b', 'Mâlik'), (r'\bHilal\b', 'Hilâl'),
         (r'\bMurare\b|\bMürare\b', 'Mürâre'), (r'\bZerr\b', 'Zer'), (r'\bKatade\b', 'Katâde'),
         (r'\bSelul\b|\bSelûl\b', '(eklenmez)'), (r'\bHuzeyfe b\. Yeman\b', 'Yemân'), (r'\bAmmar\b', 'Ammâr'),
         (r'\bTebuk\b|\bTebûk\b', 'Tebük'), (r'\bSeniyyet[üu]l-Veda\b', "Seniyyetü'l-Vedâ"),
         (r'\bEbû Bekr\b', 'Ebû Bekir'), (r'\bMuaz\b', 'Muâz'), (r'\bVakıdî\b|\bVâkidî\b', 'Vâkıdî'),
         (r'\bİshâk\b', 'İshak'), (r'\bİbn Sad\b', "İbn Sa'd"), (r'\bTaberi\b', 'Taberî'), (r'\bBuhari\b', 'Buhârî'),
         (r'\bKesir\b', 'Kesîr'), (r'\bSemud\b', 'Semûd'), (r'\bGassan\b', 'Gassân'),
         (r'\bMesud\b', "Mes'ûd"), (r'\bHalid\b', 'Hâlid'), (r'\bÜkeydir\b', 'Ükeyder')]

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
    if words > sp['hi']: bad(f'kelime {words} (tavan {sp["hi"]})')
    elif words < sp['lo']: print(f'  not   kelime {words}: bandın altında ({sp["lo"]}-{sp["hi"]}); doldurma, malzeme bittiyse yeterli')
    else: good(f'kelime {words} (bant {sp["lo"]}-{sp["hi"]})')
    # başlık
    heads = [l for l in lines if l.startswith('#')]
    exp = ['# Darlık Saati - Tebük Seferi', f'## {sp["title"]}'] if sec == 's1' else [f'## {sp["title"]}']
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
    for pat, name in ((MODERN,'modern kelime'), (CLICHE,'klişe'), (WRONG,'doğrulamada düşen ibare')):
        src = ' '.join(t.split('"')[0::2]) if pat is WRONG else t
        hits = sorted(set(m.group(0) for m in re.finditer(pat, src, re.I)))
        (good if not hits else bad)(f'{name}: {hits or "yok"}')
    # imlâ
    for pat, right in SPELL:
        hits = sorted(set(m.group(0) for m in re.finditer(pat, t)))
        if hits: bad(f'imlâ: {hits} -> {right}')
    # büyük sahâbe ve Ehl-i beyt: anlatıcının cümlesinde çıplak ad yok (tırnak içi hariç)
    outside = ' '.join(t.split('"')[0::2])
    HONOR = r"(?<!b\. )(?<!Ebû )(?<!Hz\. )(?<!İbn )\b(Ebû Bekir(?! el-Verrâk)|Ömer|Osman|Ali|Ca'fer|Hamza|Abbas|Fâtıma|Ümmü Seleme|Hasan|Hüseyin)\b(?! b\.)"
    bare = sorted(set(m.group(0) for m in re.finditer(HONOR, outside)))
    (good if not bare else bad)(f'Hz.siz büyük sahâbe adı (tırnak dışı): {bare or "yok"}')
    # ﷺ bir kez
    g = t.count('ﷺ')
    (good if g == 1 else bad)(f'ﷺ sayısı {g} (tam 1 olmalı)')
    # tırnaklı söz (v2: hedef değil, ayna)
    # DİKKAT: r'"[^"]*"' deseni kullanılmaz. Tırnaklar dönüşümlüdür; o desen
    # kapanan tırnakla bir sonraki açılan tırnağın arasındaki ANLATIYI da
    # yakalar ve sayıyı iki katına çıkarır. Doğrusu tırnaktan bölüp tek
    # sıradaki parçaları almaktır.
    parts = t.split('"')
    if len(parts) % 2 == 0:
        bad(f'tırnak sayısı tek ({t.count(chr(34))}); bir söz kapanmamış')
    quotes = [q for q in parts[1::2] if len(q) >= 12]
    print(f'  not   tırnaklı söz sayısı {len(quotes)}')
    # paragraf uzunluğu
    longp = [(i, len(p.split())) for i, p in enumerate(body, 1) if len(p.split()) > 170]
    shortp = [(i, len(p.split())) for i, p in enumerate(body, 1) if len(p.split()) < 85]
    if longp: print(f'  not   170+ kelimelik paragraf: {longp}')
    if shortp: print(f'  not   85- kelimelik paragraf (ağırlık cümlesi olabilir): {shortp}')
    print(f'  {"GEÇTİ" if ok else "GEÇMEDİ"}  ({len(body)} paragraf)')
    return ok

args = sys.argv[1:] or ['all']
secs = sorted(SPEC, key=lambda s: int(s[1:])) if args == ['all'] else args
secs = [s for s in secs if os.path.exists(s + '.md')] if args == ['all'] else secs
allok = all([check(s) for s in secs])
tot = sum(len(' '.join(l for l in open(s+'.md').read().split('\n') if l.strip() and not l.startswith('#')).split()) for s in secs if os.path.exists(s+'.md'))
print(f'\nTOPLAM {tot} kelime / {len(secs)} bölüm')
sys.exit(0 if allok else 1)
