#!/usr/bin/env python3
"""
lf_update.py — Aggiorna l'indice di Literatura Foiro
Uso: python3 lf_update.py
"""

import csv, io, json, re, sys

CSV_FILE = "lf_indekso.csv"
HTML_FILE = "index.html"

# ── 1. Leggi il CSV ──────────────────────────────────────────────────────────
with open(CSV_FILE, encoding="utf-8", newline="") as f:
    raw = f.read()

lines = raw.splitlines()

# Salta la prima riga se è "lf_indekso" (aggiunta da Numbers come nome tabella)
start = 1 if lines[0].strip() == "lf_indekso" else 0

# Rileva automaticamente il separatore (punto e virgola o virgola)
header = lines[start]
delimiter = ";" if header.count(";") > header.count(",") else ","
print(f"Separatore rilevato: '{delimiter}'")

reader = csv.DictReader(io.StringIO("\n".join(lines[start:])), delimiter=delimiter)

def clean(s):
    s = s.replace("\\n", " ").replace("\\t", " ")
    return "".join(c if ord(c) >= 32 else " " for c in s).strip()

records = [{k: clean(v) for k, v in row.items()} for row in reader]
print(f"Record letti: {len(records)}")

# Verifica che i campi siano corretti
expected = {'jaro','titolo','aŭtoro(j)','tipologio'}
actual = set(records[0].keys()) if records else set()
if not expected.issubset(actual):
    print(f"ERRORE: campi CSV non validi.")
    print(f"  Attesi: {expected}")
    print(f"  Trovati: {actual}")
    sys.exit(1)

# ── 2. Serializza in JSON ────────────────────────────────────────────────────
new_json = json.dumps(records, ensure_ascii=False, separators=(",", ":"))

# ── 3. Sostituisci DATA nell'HTML ────────────────────────────────────────────
with open(HTML_FILE, encoding="utf-8") as f:
    html = f.read()

MARKER = "const DATA = ["
if MARKER not in html:
    print("ERRORE: 'const DATA = [' non trovato nell'HTML.")
    sys.exit(1)

start_idx = html.index(MARKER) + len(MARKER) - 1  # points to '['
# Find matching closing '];'
end_idx = html.index("];", start_idx) + 2

new_html = html[:start_idx - len(MARKER) + 1 - (len(MARKER)-1)] 
# Simpler: replace everything between markers
new_html = html[:html.index(MARKER)] + f"const DATA = {new_json};" + html[end_idx:]

# ── 4. Verifica ──────────────────────────────────────────────────────────────
check = re.search(r'const DATA = (\[[\s\S]*?\]);', new_html)
if not check:
    print("ERRORE: verifica fallita, DATA non trovato nell'HTML generato.")
    sys.exit(1)
try:
    verify = json.loads(check.group(1))
    print(f"Verifica OK: {len(verify)} record nell'HTML.")
except Exception as e:
    print(f"ERRORE JSON: {e}")
    sys.exit(1)

# ── 5. Salva ─────────────────────────────────────────────────────────────────
with open(HTML_FILE, "w", encoding="utf-8") as f:
    f.write(new_html)

print(f"✓ {HTML_FILE} aggiornato con {len(records)} record.")
