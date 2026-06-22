# west-kal.de — Systems Engineering Kalibrierlaboratorium
**Aktueller Stand: Produktionsbereit** · Letzte Aktualisierung: 19. Juni 2026

---

## 📁 Dateistruktur

```
west-kal.de/
│
├── index.html               ← Startseite (vollständig)
├── leistungen.html          ← Leistungen & Gerätetypen
├── akkreditierung.html      ← DAkkS-Akkreditierung + CMC-Tabellen
├── ueber-uns.html           ← Über uns, Team, Laborausstattung
├── impressum.html           ← Impressum (vollständig ausgefüllt)
├── datenschutz.html         ← Datenschutzerklärung (DSGVO)
│
├── sitemap.xml              ← SEO: bei Google Search Console einreichen
├── robots.txt               ← Crawler-Steuerung
│
├── news.json                ← ← NUR HIER News pflegen
├── news-editor.jsx          ← Claude-gestützter News-Editor (in Claude.ai öffnen)
│
├── css/
│   └── style.css            ← Gemeinsame Styles (alle Seiten haben CSS inline)
│
├── img/
│   ├── logo.jpg             ← Systems Engineering Logo
│   └── labor-gebaeude.jpg   ← Gebäudefoto Standort Stolberg
│
└── downloads/
    ├── dakks-urkunde-elektrisch-D-K-19425-01-01.pdf
    └── dakks-urkunde-temperatur-D-K-19425-01-02.pdf
```

---

## 🚀 GitHub Pages – Website live schalten

### Einmalig: Repository einrichten

1. **GitHub-Account** anlegen: [github.com](https://github.com) (falls noch nicht vorhanden)

2. **Neues Repository** erstellen:
   - Name: `west-kal.de`
   - Sichtbarkeit: **Public** (kostenlos für GitHub Pages)

3. **Alle Dateien hochladen** (Drag & Drop im Browser oder Git in VS Code):
   ```bash
   git init
   git add .
   git commit -m "Website Launch"
   git remote add origin https://github.com/DEIN-USERNAME/west-kal.de.git
   git push -u origin main
   ```

4. **GitHub Pages aktivieren**:
   - Repository → Settings → Pages
   - Source: **Deploy from a branch** → main → / (root) → Save

5. **Domain einrichten** (`west-kal.de`):
   - Settings → Pages → Custom domain → `www.west-kal.de` → Save
   - DNS beim Anbieter: CNAME `www` → `DEIN-USERNAME.github.io`
   - Apex-Domain (A-Records auf 185.199.108-111.153)
   - "Enforce HTTPS" aktivieren (nach DNS-Propagation ~48h)

---

## 📝 News veröffentlichen

### Workflow

1. **news-editor.jsx** in Claude.ai öffnen → Beitrag schreiben
2. Claude verbessert Text und generiert LinkedIn-Post
3. JSON-Snippet kopieren → in `news.json` oben einfügen
4. Git commit + push → live in Minuten

### news.json Struktur
```json
{
  "datum": "19. Juni 2026",
  "titel": "Titel des Beitrags",
  "teaser": "Kurzbeschreibung (max. 160 Zeichen)",
  "slug": "url-freundlicher-name",
  "inhalt": "Vollständiger Beitragstext"
}
```

---

## ✅ Go-Live Checkliste

- [x] Logo eingebettet (alle Seiten)
- [x] Telefon +49 2402 900180
- [x] DAkkS-Nummern D-K-19425-01-01 / -02
- [x] calServer https://systems-engineering.calserver.com/
- [x] E-Mail info@systems-engineering-gmbh.de
- [x] Impressum vollständig (Peter Reinhardt, Bastian Hahn, HRA 5617, HRB 11194, DE160367476)
- [x] DAkkS-Urkunden als PDF verlinkt
- [x] Schema.org / SEO-Markup
- [x] Sitemap.xml
- [x] robots.txt
- [x] Anfrage-Konfigurator
- [x] Neuigkeiten-Sektion (HTML-Fallback + news.json)
- [ ] **Web3Forms Key** holen → [web3forms.com](https://web3forms.com) → in index.html `WEB3FORMS_KEY` eintragen
- [ ] **Plausible Analytics** → [plausible.io](https://plausible.io) einrichten + 1 Zeile in index.html einkommentieren
- [ ] **Google Business Profile** → [business.google.com](https://business.google.com)
- [ ] **Google Search Console** → [search.google.com/search-console](https://search.google.com/search-console) + sitemap.xml einreichen
- [ ] **LinkedIn-Profil** anlegen → URL in index.html Schema.org eintragen

---

## 🔧 Lokale Vorschau

```bash
# Python (immer verfügbar)
python -m http.server 8000
# → http://localhost:8000

# VS Code: "Live Server" Extension → Rechtsklick auf index.html → "Open with Live Server"
```

> ⚠️ Dateien direkt per Doppelklick öffnen: Die meisten Funktionen klappen,
> aber news.json-Laden schlägt fehl (kein Server) → Fallback-Posts werden angezeigt.

---

## 📬 Anfrage-Konfigurator → spätere BC-Integration

**Aktueller Stand**: Konfigurator sendet strukturierte E-Mail an info@systems-engineering-gmbh.de.

**Geplante Erweiterung (Phase 2)**:
1. Power Automate liest eingehende Kalibrieranfragen
2. Claude API extrahiert strukturierte Daten (Geräte, Kontakt, Kalibrierart)
3. BC-Connector erstellt automatisch: Kontakt + Verkaufsangebot

Das E-Mail-Format ist bereits maschinenlesbar gestaltet — kein Umbau nötig.

---

*Erstellt mit Claude (Anthropic) · claude.ai · Systems Engineering Kalibrierlaboratorium GmbH & Co. KG*
