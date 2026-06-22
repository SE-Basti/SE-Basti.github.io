#!/usr/bin/env python3
"""
build.py — Systems Engineering Website Builder
Liest geraete.json und generiert:
  - geraete.html (vollständige SEO-Seite mit allen Geräten)
  - Aktualisiert den <datalist> in index.html, einsenden.html, konfigurator-bezogene Seiten

Aufruf:
  python3 build.py

Wird automatisch von GitHub Actions ausgeführt wenn geraete.json geändert wird.
"""

import json, re, os
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent

# ── Daten laden ──────────────────────────────────────────────────────────────
with open(ROOT / 'geraete.json', encoding='utf-8') as f:
    geraete = json.load(f)

KAT_LABELS = {
    'kalibratoren': 'Multiprodukt-Kalibratoren',
    'multimeter':   'Multimeter & Stromzangen',
    'frequenz':     'Frequenzzähler & Funktionsgeneratoren',
    'milliohm':     'Milliohm- & Isolationsmessgeräte',
    'lcr':          'LCR-Meter & Impedanzmessgeräte',
    'temperatur':   'Temperaturmessgeräte',
    'sicherheit':   'Sicherheitsprüfgeräte',
    'oszilloskop':  'Oszilloskope',
}

hersteller_count = len(set(g['hersteller'] for g in geraete))
heute = date.today().strftime('%Y-%m-%d')

# ── Datalist HTML (für Autocomplete) ─────────────────────────────────────────
def build_datalist():
    opts = '\n'.join(
        f'  <option value="{g["hersteller"]} {g["modell"]}">'
        for g in geraete
    )
    return f'<datalist id="geraete-list">\n{opts}\n</datalist>'

DATALIST = build_datalist()

# ── Datalist in HTML-Dateien aktualisieren ────────────────────────────────────
DATALIST_FILES = ['index.html', 'einsenden.html']

for fname in DATALIST_FILES:
    fpath = ROOT / fname
    if not fpath.exists():
        print(f"  ⚠ {fname} nicht gefunden, übersprungen")
        continue
    with open(fpath, encoding='utf-8') as f:
        html = f.read()

    # Bestehende Datalist ersetzen oder vor </body> einfügen
    if '<datalist id="geraete-list">' in html:
        html = re.sub(
            r'<datalist id="geraete-list">.*?</datalist>',
            DATALIST,
            html, flags=re.DOTALL
        )
        print(f"  ✓ {fname}: datalist aktualisiert")
    elif '</body>' in html:
        html = html.replace('</body>', DATALIST + '\n</body>')
        print(f"  ✓ {fname}: datalist eingefügt")

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(html)

# ── geraete.html generieren ───────────────────────────────────────────────────
from collections import defaultdict

by_kat = defaultdict(list)
for g in geraete:
    by_kat[g['kat']].append(g)

# Tabellen nach Kategorie
kat_blocks = ''
for kat, label in KAT_LABELS.items():
    if kat not in by_kat:
        continue
    rows = ''.join(
        f'<tr>'
        f'<td class="td">{g["hersteller"]}</td>'
        f'<td class="td mono blue">{g["modell"]}</td>'
        f'<td class="td muted small">{g["bezeichnung"]}</td>'
        f'<td class="td center"><a href="/einsenden.html" class="kal-link">Kalibrieren →</a></td>'
        f'</tr>'
        for g in by_kat[kat]
    )
    kat_blocks += f'''<section class="kat-block" id="kat-{kat}">
  <h2 class="kat-title"><span class="kat-badge">{label}</span></h2>
  <div class="tbl-wrap">
    <table class="gtbl">
      <thead><tr>
        <th>Hersteller</th><th>Modell</th><th>Bezeichnung</th><th>Aktion</th>
      </tr></thead>
      <tbody>{rows}</tbody>
    </table>
  </div>
</section>\n'''

kat_nav = ' · '.join(
    f'<a href="#kat-{k}">{l}</a>'
    for k, l in KAT_LABELS.items() if k in by_kat
)

# CSS inline (kompakt, ohne Logo-base64)
CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Inter,system-ui,sans-serif;background:#EEF2F8;color:#08152E;line-height:1.6;-webkit-font-smoothing:antialiased}
.wrap{max-width:1100px;margin:0 auto;padding:0 24px}
a{color:#0B53F0;text-decoration:none}
a:hover{text-decoration:underline}
header{background:rgba(8,21,46,.93);backdrop-filter:blur(10px);position:sticky;top:0;z-index:50;padding:0}
.nav{display:flex;align-items:center;justify-content:space-between;height:68px;gap:16px}
.brand{color:#fff;display:flex;align-items:center;gap:10px;text-decoration:none;font-family:Archivo,sans-serif;font-weight:800}
.nav-links{display:flex;gap:24px}
.nav-links a{color:#C4CFDB;font-size:.9rem}
.nav-links a:hover{color:#fff;text-decoration:none}
.hero{background:#08152E;color:#fff;padding:48px 0 52px}
.hero h1{font-family:Archivo,sans-serif;font-weight:800;font-size:clamp(1.8rem,4vw,2.8rem);line-height:1.1;letter-spacing:-.02em;margin-bottom:12px}
.hero .hl{color:#3B7BFF}
.hero p{color:#B7C3D0;font-size:1rem;max-width:54ch;margin-bottom:20px}
.crumb{font-size:.78rem;color:#8FA0B8;margin-bottom:16px}
.crumb a{color:#3B7BFF}
.btn{display:inline-flex;align-items:center;gap:8px;padding:10px 20px;border-radius:6px;font-family:Archivo,sans-serif;font-weight:600;font-size:.9rem;text-decoration:none}
.btn-p{background:#0B53F0;color:#fff}.btn-p:hover{background:#0A3FBE;text-decoration:none}
.btn-g{border:1px solid rgba(255,255,255,.2);color:#fff}.btn-g:hover{border-color:#3B7BFF;color:#3B7BFF;text-decoration:none}
.sticky-nav{background:#fff;border-bottom:1px solid #e0e0e0;padding:12px 0;position:sticky;top:68px;z-index:10;font-size:.86rem}
.sticky-nav a{color:#0B53F0;margin-right:2px}.sticky-nav a:hover{text-decoration:underline}
.search-wrap{padding:28px 0 8px}
.search-wrap input{width:100%;max-width:420px;background:#fff;border:1.5px solid #d0d7df;border-radius:8px;padding:11px 14px;font-size:.95rem;color:#08152E}
.search-wrap input:focus{outline:2px solid #0B53F0;outline-offset:-1px}
.kat-block{margin:32px 0}
.kat-title{margin-bottom:14px}
.kat-badge{font-family:'IBM Plex Mono',monospace;font-size:.72rem;background:rgba(11,83,240,.1);color:#0B53F0;padding:4px 12px;border-radius:4px;letter-spacing:.08em;text-transform:uppercase}
.tbl-wrap{overflow-x:auto;border:1px solid #dde3ea;border-radius:9px}
.gtbl{width:100%;border-collapse:collapse;min-width:480px}
.gtbl th{padding:10px 14px;text-align:left;font-family:'IBM Plex Mono',monospace;font-size:.68rem;letter-spacing:.12em;text-transform:uppercase;color:#55657B;background:#EEF2F8;border-bottom:2px solid #dde3ea}
.td{padding:10px 14px;border-bottom:1px solid #EEF2F8;font-size:.9rem}
.td.mono{font-family:'IBM Plex Mono',monospace;color:#0B53F0}
.td.blue{color:#0B53F0}
.td.muted{color:#55657B}
.td.small{font-size:.86rem}
.td.center{text-align:center}
.gtbl tbody tr:hover td{background:#F7F9FC}
.kal-link{font-family:Archivo,sans-serif;font-size:.82rem;font-weight:600;color:#0B53F0;white-space:nowrap}
.not-found{background:#fff;border-radius:9px;padding:22px 24px;margin-top:8px;margin-bottom:40px}
.not-found h3{font-family:Archivo,sans-serif;font-weight:600;margin-bottom:8px}
.not-found p{color:#55657B;font-size:.93rem;margin-bottom:14px}
footer{background:#08152E;color:#8FA0B8;padding:48px 0 32px;margin-top:48px;border-top:1px solid rgba(255,255,255,.1)}
footer h4{color:#fff;font-size:.92rem;margin-bottom:12px;font-family:Archivo,sans-serif}
footer a{display:block;color:#8FA0B8;font-size:.88rem;padding:4px 0}
footer a:hover{color:#3B7BFF;text-decoration:none}
.fgrid{display:grid;grid-template-columns:2fr 1fr 1fr;gap:28px;margin-bottom:32px}
.copyright{border-top:1px solid rgba(255,255,255,.1);padding-top:20px;font-family:'IBM Plex Mono',monospace;font-size:.74rem;display:flex;justify-content:space-between;flex-wrap:wrap;gap:10px}
@media(max-width:700px){.fgrid{grid-template-columns:1fr}.nav-links{display:none}}
"""

geraete_html = f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Kalibrierfähige Messgeräte | {len(geraete)} Modelle | Systems Engineering</title>
<meta name="description" content="Vollständige Liste aller {len(geraete)} Messgeräte die wir DAkkS-akkreditiert kalibrieren: Multimeter, Kalibratoren, Oszilloskope, Sicherheitsprüfgeräte und Temperaturmessgeräte von Fluke, Keysight, Tektronix, Megger und weiteren.">
<meta name="keywords" content="Multimeter kalibrieren DAkkS, Fluke 87V Kalibrierung, Keysight Kalibrierung, Oszilloskop kalibrieren, Sicherheitsprüfgerät Kalibrierung, Installationstester kalibrieren, Temperaturmessgerät kalibrieren Stolberg NRW">
<link rel="canonical" href="https://www.west-kal.de/geraete.html">
<!-- Letzte Aktualisierung: {heute} | {len(geraete)} Geräte | generiert von build.py -->
<meta property="og:title" content="Kalibrierfähige Messgeräte | Systems Engineering">
<meta property="og:description" content="{len(geraete)} Messgerätemodelle DAkkS-akkreditiert kalibrierbar – von Fluke, Keysight, Tektronix und mehr.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@700;800&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@400;600&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<header>
  <div class="wrap nav">
    <a class="brand" href="/">SE Kalibrierlaboratorium</a>
    <nav class="nav-links">
      <a href="/">Startseite</a>
      <a href="/leistungen.html">Leistungen</a>
      <a href="/geraete.html">Geräteliste</a>
      <a href="/akkreditierung.html">Akkreditierung</a>
      <a href="/#kontakt">Kontakt</a>
    </nav>
  </div>
</header>

<section class="hero">
  <div class="wrap">
    <div class="crumb"><a href="/">Startseite</a> › <a href="/leistungen.html">Leistungen</a> › Geräteliste</div>
    <h1>Kalibrierfähige Messgeräte —<br><span class="hl">{len(geraete)} Modelle</span> von {hersteller_count} Herstellern</h1>
    <p>Alle Gerätetypen die wir DAkkS-akkreditiert kalibrieren. Ihr Gerät nicht dabei? Anfragen — wir prüfen es kurzfristig.</p>
    <div style="display:flex;gap:12px;flex-wrap:wrap">
      <a href="/einsenden.html" class="btn btn-p">Gerät einschicken →</a>
      <a href="/#kontakt" class="btn btn-g">Anfrage stellen</a>
    </div>
  </div>
</section>

<div class="sticky-nav">
  <div class="wrap">{kat_nav}</div>
</div>

<div class="search-wrap">
  <div class="wrap">
    <input type="text" id="gs" placeholder="Suchen … z. B. Fluke 87V oder Tektronix"
      oninput="filterG(this.value)">
  </div>
</div>

<div class="wrap">
  {kat_blocks}
  <div class="not-found">
    <h3>Ihr Gerät nicht in der Liste?</h3>
    <p>Die Liste zeigt unsere häufigsten Kalibrieraufträge — wir kalibrieren deutlich mehr. Sprechen Sie uns an, wir prüfen kurzfristig ob eine Kalibrierung möglich ist und mit welcher Messunsicherheit.</p>
    <a href="/#kontakt" class="btn btn-p" style="font-size:.88rem;padding:9px 18px">Gerät anfragen →</a>
  </div>
</div>

<footer>
  <div class="wrap">
    <div class="fgrid">
      <div><strong style="color:#fff;font-family:Archivo,sans-serif">Systems Engineering Kalibrierlaboratorium GmbH &amp; Co. KG</strong><p style="margin-top:8px;font-size:.86rem">Leimberg 9 · 52222 Stolberg / Rheinland<br>Tel. +49 2402 900180</p></div>
      <nav><h4>Navigation</h4><a href="/leistungen.html">Leistungen</a><a href="/geraete.html">Geräteliste</a><a href="/akkreditierung.html">Akkreditierung</a><a href="/ueber-uns.html">Über uns</a></nav>
      <nav><h4>Rechtliches</h4><a href="/impressum.html">Impressum</a><a href="/datenschutz.html">Datenschutz</a></nav>
    </div>
    <div class="copyright">
      <span>© {date.today().year} Systems Engineering Kalibrierlaboratorium GmbH &amp; Co. KG</span>
      <span>DAkkS D-K-19425 · ISO/IEC 17025 · Generiert {heute}</span>
    </div>
  </div>
</footer>

<script>
function filterG(q) {{
  var blocks = document.querySelectorAll('.kat-block');
  q = q.toLowerCase().trim();
  if (!q) {{ blocks.forEach(function(b) {{ b.style.display=''; }}); return; }}
  blocks.forEach(function(block) {{
    var rows = block.querySelectorAll('tbody tr');
    var any = false;
    rows.forEach(function(r) {{
      var show = r.textContent.toLowerCase().includes(q);
      r.style.display = show ? '' : 'none';
      if (show) any = true;
    }});
    block.style.display = any ? '' : 'none';
  }});
}}
</script>
</body>
</html>"""

out_path = ROOT / 'geraete.html'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(geraete_html)

print(f"✓ geraete.html: {len(geraete)} Geräte, {hersteller_count} Hersteller")
print(f"✓ Datalist aktualisiert in: {', '.join(DATALIST_FILES)}")
print(f"✓ Letzte Aktualisierung: {heute}")
