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
SECS = [s for s in ('s1','s2','s3','s4','s5','s6','s7') if os.path.exists(s + '.md')]

# Sahibi brieflerde belli olan ayrıntılar: (ad, desen, sahip bölüm)
OWNED = [
 ('altı zırh / sekiz kılıç',   r'sekiz kılıç|altı zırh',                's2'),
 ('bedrî mertebesi',           r'bedrî|bedriyy',                        's7'),
 ('mübâreze',                  r'mübâreze',                             's4'),
 ('Utbe\'nin barış teşebbüsü', r'Utbe.{0,40}(barış|sulh)|barış teşebbüs', 's4'),
 ('Âtike\'nin rüyası',         r'Âtike|rüya',                           's2'),
 ('Hubâb\'ın kuyu tavsiyesi',  r'Hubâb',                                's3'),
 ('yağmur ve Enfâl 8:11',      r'8:11|yağmur',                          's4'),
 ('humus / beşte bir',         r'humus|beşte bir',                      's7'),
 ('furkān günü',               r'furkān',                               's7'),
 ('on dört mezar',             r'on dört mez|on dört ölü',              's7'),
 ('üç yüz on üç',              r'üç yüz on üç',                         's2'),
 ('Damdam',                    r'Damdam',                               's2'),
 ('kervanın kıymeti',          r'elli bin dinar|bin deve',              's1'),
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
for pat in (r'Ebû Süfyân b\. Harb', r'Ebû Süfyân b\. Hâris', r'Amr b\. Hadramî',
            r'Âmir b\. Hadramî', r'Muâz b\. Amr b\. Cemûh', r'Muavviz b\. Afrâ',
            r'Avf b\. Afrâ'):
    n = len(re.findall(pat, allt))
    print(f'  {pat.replace(chr(92), "")}: {n}')
