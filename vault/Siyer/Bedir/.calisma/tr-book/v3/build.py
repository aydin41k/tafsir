#!/usr/bin/env python3
"""Yedi bölümü tek kitap hâline getirir: furkan-gunu.md

DİKKAT: aydin4ik onay verene kadar çalıştırılmaz. Şimdilik yalnız MD yazılıyor.
"""
import os, sys, re

os.chdir(os.path.dirname(os.path.abspath(__file__)))
SECS = ['s1', 's2', 's3', 's4', 's5', 's6', 's7', 's8']
OUT = 'furkan-gunu.md'

missing = [s for s in SECS if not os.path.exists(s + '.md')]
if missing:
    sys.exit(f'eksik bölüm: {missing}')

parts = []
for s in SECS:
    t = open(s + '.md').read().strip()
    parts.append(t)

book = '\n\n'.join(parts) + '\n'
open(OUT, 'w').write(book)

lines = book.split('\n')
body = [l for l in lines if l.strip() and not l.startswith('#')]
words = len(' '.join(body).split())
print(f'{OUT} yazıldı')
print(f'  bölüm      : {len([l for l in lines if l.startswith("## ")])}')
print(f'  kitap adı  : {[l for l in lines if l.startswith("# ")]}')
print(f'  kelime     : {words}')
print(f'  sayfa (~315 kelime/A5) : {words/315:.1f}')
print(f'  uzun çizgi : {book.count("—") + book.count("–")}')
print(f'  dipnot     : {book.count("[^")}')
print(f'  ﷺ         : {book.count("ﷺ")} (bölüm başına 1, yani 7 olmalı)')
print('\n  başlık sırası:')
for l in lines:
    if l.startswith('#'):
        print(f'    {l}')
