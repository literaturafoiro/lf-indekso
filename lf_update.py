#!/usr/bin/env python3
"""
lf_update.py — Aggiorna l'indice di Literatura Foiro
Uso: python3 lf_update.py

Legge lf_indekso.csv, sostituisce il blocco DATA nell'HTML e salva index.html.
"""

import csv, json, re, io

CSV_FILE  = "lf_indekso.csv"
HTML_IN   = "index.html"
HTML_OUT  = "index.html"

# 1. Leggi il CSV (separatore punto e virgola, salta eventuale prima riga "lf_indekso")
with open(CSV_FILE, encoding="utf-8", newline="") as f:
    raw = f.read()

lines = raw.splitlines()
# Salta la prima riga se non è l'intestazione dei campi
start = 1 if lines[0].strip() == "lf_indekso" else 0
reader = csv.DictReader(io.StringIO("\n".join(lines[start:])), delimiter=";")
records = [dict(row) for row in reader]

# 2. Serializza in JSON compatto
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
