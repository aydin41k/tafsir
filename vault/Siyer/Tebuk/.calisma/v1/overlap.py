#!/usr/bin/env python3
"""Bölümler arası tekrar yoklayıcı.

Koşut yazımın bedeli tekrardır: iki bölüm aynı ayrıntıyı ayrı ayrı anlatır.
Bu betik iki şeyi yoklar:

  1. Bölümler arasında paylaşılan uzun kelime dizileri (7 kelime ve üstü).
     Aynı vak'ayı iki kere anlatmak çoğu zaman aynı kelimeleri de getirir.
  2. Adı belli ayrıntıların hangi bölümlerde geçtiği. Her birinin sahibi
     brieflerde bellidir; birden fazla bölümde çıkması bakılacak demektir.

Kullanım: python3 overlap.py
"""
import re, os, glob, itertools

os.chdir(os.path.dirname(os.path.abspath(__file__)))

N = 7          # kaç kelimelik dizi tekrar sayılsın
SECS = [s for s in ('s1','s2','s3','s4','s5','s6','s7','s8') if os.path.exists(s + '.md')]

# Sahibi brieflerde belli olan ayrıntılar: (ad, desen, sahip bölüm)
OWNED = [
 ('Ka\'b\'ın açılış sözü / Akabe gecesi', r'Akabe gecesi',                    's1'),
 ('Mu\'te',                     r'Mu\'te',                                     's1'),
 ('Nebatî haberi',              r'Nebatî',                                      's1'),
 ('iki binek devesi',           r'iki binek|iki deve',                          's2'),
 ('Osman\'ın bin dinarı',       r'bin dinar',                                   's2'),
 ('Ebû Akîl / sâ\' (9:79)',     r'Ebû Akîl',                                    's8'),
 ('bekkâûn',                    r'bekkâûn|ağlayarak dön',                       's2'),
 ('Cedd b. Kays',               r'Cedd',                                        's2'),
 ('sıcakta çıkmayın (9:81)',    r'sıcakta çıkmay',                              's2'),
 ('Süveylim',                   r'Süveylim',                                    's2'),
 ('Abdullah b. Übey\'in dönüşü', r'Übey.{0,60}(dön|geri)',                     's3'),
 ('Hârûn sözü',                 r'Hârûn',                                       's3'),
 ('Hicr kuyuları',              r'Hicr|Semûd',                                  's3'),
 ('kaybolan deve',              r'Lusayt|ağaca takıl',                          's3'),
 ('Ebû Zer yalnız',             r'Ebû Zer',                                     's3'),
 ('Tebük pınarı',               r'pınar',                                       's4'),
 ('Ükeyder',                    r'Ükeyder',                                     's4'),
 ('Zülbicâdeyn',                r'Zülbicâdeyn',                                 's4'),
 ('Ebû Hayseme',                r'Ebû Hayseme',                                 's4'),
 ('Ka\'b sorulur / iki bürde',  r'iki bürde|Ka\'b ne yaptı',                    's4'),
 ('Akabe geçidi',               r'geçit|Huzeyfe',                               's5'),
 ('alaycılar (9:65)',           r'eğleniyor|lafa dal',                          's3'),
 ('rüzgâr gecesi',              r'Tay',                                         's4'),
 ('Mescid-i Dırâr',             r'Dırâr|Zû Evân',                               's5'),
 ('Medine\'de kalıp beraber olanlar', r'hiçbir vadi geçmediniz|özürleri alıkoy', 's5'),
 ('öfkeli adamın tebessümü',    r'tebessüm',                                    's6'),
 ('seksen küsur yemin',         r'seksen küsur',                                    's6'),
 ('Ebû Katâde\'nin duvarı',     r'Ebû Katâde|duvar',                            's6'),
 ('Gassân mektubu',             r'Gassân|tandır',                               's6'),
 ('Sel\' dağı müjdesi',         r'Sel\'',                                       's6'),
 ('darlık saati (9:117)',       r'darlık saat|sâatü\'l-usre',                   's8'),
 ('hullifû / ertelenen',        r'ertelen',                                     's8'),
 ('Tevvâb / rahmet kapanışı',   r'Tevvâb|tevbeyi çok kabul',                    's8'),
 ('Ka\'b\'ın doğruluk nimeti',  r'bile bile|daha büyük ol',                     's7'),
 ('Abdullah b. Übey\'in cenazesi', r'gömleğ|seksen dördüncü',                  's7'),
 ('Rebeze',                     r'Rebeze',                                      's7'),
 ('el-Fâdıha',                  r'Fâdıha',                                      's8'),
 ('yüz yirminci âyet',          r'yüz yirminci',                                's8'),
]

def body(sec):
    t = open(sec + '.md').read()
    return '\n'.join(l for l in t.split('\n') if l.strip() and not l.startswith('#'))

def norm(s):
    s = s.lower()
    s = re.sub(r'[^\wçğıöşüâîû\s]', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()

texts = {s: body(s) for s in SECS}
grams = {}
for s in SECS:
    w = norm(texts[s]).split()
    grams[s] = {' '.join(w[i:i+N]) for i in range(len(w) - N + 1)}

print(f'=== paylaşılan {N}+ kelimelik diziler ===')
found = 0
for a, b in itertools.combinations(SECS, 2):
    shared = grams[a] & grams[b]
    # alt dizileri at: uzun bir eşleşme kendi içindeki kısaları da üretir
    shared = {g for g in shared if not any(g != h and g in h for h in shared)}
    if shared:
        found += len(shared)
        print(f'\n{a} <-> {b}  ({len(shared)})')
        for g in sorted(shared):
            print(f'    {g}')
if not found:
    print('  yok')

print('\n=== sahibi belli ayrıntılar ===')
print('  Ölçü cümledir, kelime değil: bir motifin sahibi olmayan bir bölümde bir')
print('  cümlede anılması geri çağırmadır ve caizdir; iki ve daha fazla cümlede')
print('  anılması o ayrıntının ikinci defa anlatıldığına delâlet eder.\n')
def sentences(t):
    return [c for c in re.split(r'(?<=[.!?:;])\s+', t) if c.strip()]
for name, pat, owner in OWNED:
    hits = {s: sum(1 for c in sentences(texts[s]) if re.search(pat, c, re.I)) for s in SECS}
    hits = {s: n for s, n in hits.items() if n}
    heavy = [s for s, n in hits.items() if s != owner and n >= 2]
    flag = 'BAK ' if heavy else 'ok  '
    where = ', '.join(f'{s}:{n} cümle' for s, n in sorted(hits.items()))
    print(f'  {flag}{name} (sahip {owner}): {where or "hiç geçmiyor"}')

print('\n=== tırnaklı söz: aynı söz iki bölümde mi? ===')
print('  v2\'nin getirdiği yeni tehlike budur. Bir konuşma bir bölümde söz olarak')
print('  yazılmışsa, öteki bölümde ancak anılabilir; ikinci defa tırnağa alınamaz.\n')
QN = 5   # söz içinde kaç kelimelik dizi eşleşme sayılsın

# DİKKAT: r'"([^"]*)"' deseni yanlıştır. Tırnaklar dönüşümlü olduğu için o desen
# kapanan tırnakla bir sonraki açılan tırnağın arasındaki anlatıyı da söz sanar.
# Tırnaktan bölüp tek sıradaki parçaları almak lâzımdır.
def quoted(t):
    parts = t.split('"')
    return [q for q in parts[1::2] if len(q) >= 12]

quotes = {s: quoted(texts[s]) for s in SECS}
qgrams = {}
for s in SECS:
    g = set()
    for q in quotes[s]:
        w = norm(q).split()
        g |= {' '.join(w[i:i+QN]) for i in range(len(w) - QN + 1)}
    qgrams[s] = g
qfound = 0
for a, b in itertools.combinations(SECS, 2):
    shared = qgrams[a] & qgrams[b]
    shared = {g for g in shared if not any(g != h and g in h for h in shared)}
    if shared:
        qfound += len(shared)
        print(f'  BAK {a} <-> {b}: {sorted(shared)}')
if not qfound:
    print('  ok  hiçbir söz iki bölümde tırnağa alınmamış')

print('\n=== söz sayımı ve tırnak sıhhati ===')
tot_q = 0
for s in SECS:
    t = texts[s]
    paras = [p for p in t.split('\n') if p.strip()]
    tek = [i for i, p in enumerate(paras, 1) if p.count('"') % 2]
    yogun = [(i, p.count('"') // 2) for i, p in enumerate(paras, 1) if p.count('"') // 2 > 4]
    # dolaylı kalmış konuşma fiilleri: kaynak sözü korumadıysa yerindedir
    dolayli = len(re.findall(r'\b(söyledi|bildirdi|dile getirdi|ifade etti|belirtti)\b', t))
    tot_q += len(quotes[s])
    uyari = []
    if tek: uyari.append(f'tek tırnak kalmış paragraf {tek}')
    if yogun: uyari.append(f'4\'ten çok sözlü paragraf {yogun}')
    print(f'  {"BAK " if uyari else "ok  "}{s}: {len(quotes[s])} söz, {dolayli} dolaylı fiil'
          + (('  <- ' + '; '.join(uyari)) if uyari else ''))
dedikî = len(re.findall(r'dedi ki:', '\n'.join(texts[s] for s in SECS)))
print(f'\n  kitapta toplam {tot_q} tırnaklı söz ({tot_q / len(SECS):.1f} bölüm başına)')
print(f'  "dedi ki:" {dedikî} kere (brief sade "dedi:"yi tercih ediyor)')

print('\n=== ﷺ ve ad imlâsı, bütün kitapta ===')
allt = '\n'.join(texts[s] for s in SECS)
print(f'  ﷺ toplam {allt.count("ﷺ")} (bölüm sayısı {len(SECS)} olmalı)')
for pat in (r"Ka'b b\. Mâlik", r'Mürâre b\. Rebî', r'Hilâl b\. Ümeyye', r'Abdullah b\. Übey',
            r'Ebû Hayseme', r'Ebû Zer', r'Ebû Katâde'):
    n = len(re.findall(pat, allt))
    print(f'  {pat.replace(chr(92), "")}: {n}')
