#!/usr/bin/env python3
"""
lf_update.py — Aggiorna l'indice di Literatura Foiro
Uso: python lf_update.py

Legge lf_indekso.csv, sostituisce il blocco DATA nell'HTML e salva index.html.
"""

import csv, json, re

CSV_FILE  = "lf_indekso.csv"
HTML_IN   = "index.html"        # file originale (template)
HTML_OUT  = "index.html"        # sovrascrive; cambia nome se vuoi backup

# 1. Leggi il CSV
records = []
with open(CSV_FILE, encoding="utf-8-sig", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        records.append(dict(row))

# 2. Serializza in JSON compatto (come nell'originale)
new_json = json.dumps(records, ensure_ascii=False, separators=(",", ":"))

# 3. Sostituisci il blocco DATA nel file HTML
with open(HTML_IN, encoding="utf-8") as f:
    html = f.read()

new_html = re.sub(
    r'const DATA = \[[\s\S]*?\];',
    f'const DATA = {new_json};',
    html,
    count=1
)

with open(HTML_OUT, "w", encoding="utf-8") as f:
    f.write(new_html)

print(f"✓ {len(records)} record scritti in {HTML_OUT}")
