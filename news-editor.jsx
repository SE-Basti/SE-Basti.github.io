import { useState, useEffect } from "react";

const KATEGORIEN = ["Akkreditierung", "Kalibrierung", "Temperatur", "Elektrisch", "Prüfmittelmanagement", "Allgemein"];

const MONATE = ["Januar","Februar","März","April","Mai","Juni","Juli","August","September","Oktober","November","Dezember"];

function formatDatum(d) {
  if (!d) return "";
  const [y, m, day] = d.split("-");
  return `${parseInt(day)}. ${MONATE[parseInt(m) - 1]} ${y}`;
}

function titelToSlug(t) {
  return t.toLowerCase()
    .replace(/ä/g,"ae").replace(/ö/g,"oe").replace(/ü/g,"ue").replace(/ß/g,"ss")
    .replace(/[^a-z0-9]+/g,"-").replace(/^-|-$/g,"").substring(0, 50);
}

function heute() {
  return new Date().toISOString().split("T")[0];
}

export default function NewsEditor() {
  const [kategorie, setKategorie] = useState("Akkreditierung");
  const [stichwort, setStichwort] = useState("");
  const [titel, setTitel] = useState("");
  const [teaser, setTeaser] = useState("");
  const [volltext, setVolltext] = useState("");
  const [slug, setSlug] = useState("");
  const [datum, setDatum] = useState(heute());
  const [aiStatus, setAiStatus] = useState({ text: "", type: "" });
  const [jsonStatus, setJsonStatus] = useState({ text: "", type: "" });
  const [jsonOutput, setJsonOutput] = useState("");
  const [aiLoading, setAiLoading] = useState(false);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    if (titel) setSlug(titelToSlug(titel));
  }, [titel]);

  async function generateAI() {
    if (!stichwort.trim()) {
      setAiStatus({ text: "Bitte ein Stichwort eingeben.", type: "err" });
      return;
    }
    setAiLoading(true);
    setAiStatus({ text: "KI generiert Text …", type: "" });

    const prompt = `Du bist Redakteur für Systems Engineering Kalibrierlaboratorium GmbH & Co. KG, ein DAkkS-akkreditiertes Kalibrierlabor in Stolberg (ISO 17025, elektrische Messgrößen und Temperatur).

Erstelle einen Newsbeitrag zum Thema: "${stichwort.trim()}"
Kategorie: ${kategorie}

Antworte NUR mit einem JSON-Objekt (kein Markdown, keine Erklärung):
{
  "titel": "Titel max 70 Zeichen, professionell, konkret",
  "teaser": "1-2 Sätze Teaser max 160 Zeichen",
  "volltext": "Vollständiger Beitragstext 3-5 Sätze, fachlich, seriös, ohne Werbeklischees"
}`;

    try {
      const res = await fetch("https://api.anthropic.com/v1/messages", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          model: "claude-sonnet-4-6",
          max_tokens: 1000,
          messages: [{ role: "user", content: prompt }]
        })
      });
      const data = await res.json();
      const text = data.content.map(i => i.text || "").join("");
      const clean = text.replace(/```json|```/g, "").trim();
      const parsed = JSON.parse(clean);
      setTitel(parsed.titel || "");
      setTeaser(parsed.teaser || "");
      setVolltext(parsed.volltext || "");
      setAiStatus({ text: "Vorschlag generiert — bitte prüfen und anpassen.", type: "ok" });
    } catch (e) {
      setAiStatus({ text: "Fehler beim Generieren. Bitte manuell ausfüllen.", type: "err" });
    }
    setAiLoading(false);
  }

  function generateJSON() {
    if (!titel.trim() || !teaser.trim() || !slug.trim()) {
      setJsonStatus({ text: "Bitte Titel, Teaser und Slug ausfüllen.", type: "err" });
      return;
    }
    const entry = {
      datum: formatDatum(datum),
      titel: titel.trim(),
      teaser: teaser.trim(),
      volltext: volltext.trim(),
      slug: slug.trim(),
      kategorie
    };
    const json = JSON.stringify(entry, null, 2) + ",";
    setJsonOutput(json);
    setJsonStatus({ text: "JSON bereit — kopieren und in news.json einfügen.", type: "ok" });
  }

  function copyJSON() {
    if (!jsonOutput) { generateJSON(); return; }
    navigator.clipboard.writeText(jsonOutput).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
      setJsonStatus({ text: "In Zwischenablage kopiert ✓", type: "ok" });
    });
  }

  const s = {
    wrap: { fontFamily: "system-ui, sans-serif", maxWidth: 640, margin: "0 auto", padding: "1.5rem 1rem", color: "#08152E" },
    h1: { fontSize: 22, fontWeight: 700, marginBottom: 4, color: "#08152E" },
    sub: { fontSize: 13, color: "#55657B", marginBottom: 24 },
    card: { background: "#fff", border: "1px solid #E2E8F0", borderRadius: 10, padding: "1.25rem", marginBottom: "1rem" },
    stepTitle: { display: "flex", alignItems: "center", gap: 8, fontSize: 15, fontWeight: 600, marginBottom: 14, color: "#08152E" },
    stepNum: { display: "inline-flex", alignItems: "center", justifyContent: "center", width: 22, height: 22, borderRadius: "50%", background: "#0B53F0", color: "#fff", fontSize: 12, fontWeight: 700, flexShrink: 0 },
    label: { fontSize: 12, color: "#55657B", display: "block", marginBottom: 4, fontWeight: 500 },
    input: { width: "100%", fontSize: 13, padding: "7px 10px", border: "1px solid #CBD5E1", borderRadius: 6, marginBottom: 12, fontFamily: "inherit", color: "#08152E", background: "#fff", boxSizing: "border-box" },
    textarea: { width: "100%", fontSize: 13, padding: "7px 10px", border: "1px solid #CBD5E1", borderRadius: 6, marginBottom: 12, fontFamily: "inherit", color: "#08152E", background: "#fff", resize: "vertical", boxSizing: "border-box" },
    tagRow: { display: "flex", flexWrap: "wrap", gap: 6, marginBottom: 12 },
    tagActive: { fontSize: 12, padding: "3px 10px", borderRadius: 20, border: "1px solid #0B53F0", background: "#EEF3FF", color: "#0B53F0", cursor: "pointer", fontWeight: 500 },
    tag: { fontSize: 12, padding: "3px 10px", borderRadius: 20, border: "1px solid #CBD5E1", background: "#F8FAFC", color: "#55657B", cursor: "pointer" },
    row: { display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 },
    btnAI: { fontSize: 13, padding: "8px 16px", borderRadius: 6, border: "1px solid #CBD5E1", background: "#F8FAFC", color: "#08152E", cursor: "pointer", fontWeight: 500, display: "inline-flex", alignItems: "center", gap: 6 },
    btnPrimary: { fontSize: 13, padding: "8px 16px", borderRadius: 6, border: "none", background: "#0B53F0", color: "#fff", cursor: "pointer", fontWeight: 600 },
    btnSecondary: { fontSize: 13, padding: "8px 16px", borderRadius: 6, border: "1px solid #CBD5E1", background: "#F8FAFC", color: "#08152E", cursor: "pointer", marginLeft: 8 },
    statusOk: { fontSize: 12, color: "#16A34A", marginTop: 6 },
    statusErr: { fontSize: 12, color: "#DC2626", marginTop: 6 },
    statusNeutral: { fontSize: 12, color: "#55657B", marginTop: 6 },
    jsonBox: { background: "#F8FAFC", border: "1px solid #E2E8F0", borderRadius: 6, padding: "1rem", fontFamily: "monospace", fontSize: 12, whiteSpace: "pre-wrap", wordBreak: "break-all", maxHeight: 260, overflowY: "auto", marginTop: 12, color: "#08152E" },
    hint: { fontSize: 12, color: "#55657B", fontStyle: "italic", marginBottom: 10, lineHeight: 1.6 },
    code: { background: "#F1F5F9", padding: "1px 5px", borderRadius: 4, fontFamily: "monospace", fontSize: 11 }
  };

  function statusStyle(type) {
    if (type === "ok") return s.statusOk;
    if (type === "err") return s.statusErr;
    return s.statusNeutral;
  }

  return (
    <div style={s.wrap}>
      <div style={s.h1}>📰 News-Editor</div>
      <div style={s.sub}>Systems Engineering Kalibrierlaboratorium — Beiträge für news.json erstellen</div>

      {/* Schritt 1 */}
      <div style={s.card}>
        <div style={s.stepTitle}>
          <span style={s.stepNum}>1</span> Thema & KI-Vorschlag
        </div>
        <span style={s.label}>Kategorie</span>
        <div style={s.tagRow}>
          {KATEGORIEN.map(k => (
            <span key={k} style={kategorie === k ? s.tagActive : s.tag} onClick={() => setKategorie(k)}>{k}</span>
          ))}
        </div>
        <span style={s.label}>Stichwort / Thema für die KI</span>
        <input style={s.input} value={stichwort} onChange={e => setStichwort(e.target.value)}
          placeholder="z. B. neue Kapazitäten Pt100, DAkkS-Überwachung bestanden …"
          onKeyDown={e => e.key === "Enter" && generateAI()} />
        <div style={s.hint}>Beschreibe kurz worum es geht — die KI schlägt Titel, Teaser und Volltext vor.</div>
        <button style={s.btnAI} onClick={generateAI} disabled={aiLoading}>
          {aiLoading ? "⏳ Wird generiert …" : "✨ Text vorschlagen"}
        </button>
        {aiStatus.text && <div style={statusStyle(aiStatus.type)}>{aiStatus.text}</div>}
      </div>

      {/* Schritt 2 */}
      <div style={s.card}>
        <div style={s.stepTitle}>
          <span style={s.stepNum}>2</span> Inhalt prüfen & anpassen
        </div>
        <span style={s.label}>Titel</span>
        <input style={s.input} value={titel} onChange={e => setTitel(e.target.value)} placeholder="z. B. Erfolgreiche DAkkS-Überwachung 2026" />
        <span style={s.label}>Teaser (1–2 Sätze für die Übersicht)</span>
        <textarea style={{ ...s.textarea, minHeight: 60 }} value={teaser} onChange={e => setTeaser(e.target.value)} placeholder="Kurze Zusammenfassung die auf der Startseite erscheint …" />
        <span style={s.label}>Volltext (erscheint auf der Detailseite)</span>
        <textarea style={{ ...s.textarea, minHeight: 120 }} value={volltext} onChange={e => setVolltext(e.target.value)} placeholder="Der vollständige Beitragstext …" />
        <div style={s.row}>
          <div>
            <span style={s.label}>Datum</span>
            <input style={s.input} type="date" value={datum} onChange={e => setDatum(e.target.value)} />
          </div>
          <div>
            <span style={s.label}>Slug (URL-Kürzel)</span>
            <input style={s.input} value={slug} onChange={e => setSlug(e.target.value)} placeholder="z. B. dakks-2026" />
          </div>
        </div>
      </div>

      {/* Schritt 3 */}
      <div style={s.card}>
        <div style={s.stepTitle}>
          <span style={s.stepNum}>3</span> JSON generieren & kopieren
        </div>
        <div style={s.hint}>
          Diesen Eintrag in <span style={s.code}>news.json</span> im GitHub-Repository einfügen —
          vor dem ersten bestehenden Eintrag, direkt nach dem öffnenden <span style={s.code}>[</span>.
        </div>
        <button style={s.btnPrimary} onClick={generateJSON}>JSON generieren</button>
        <button style={s.btnSecondary} onClick={copyJSON}>
          {copied ? "✓ Kopiert!" : "📋 Kopieren"}
        </button>
        {jsonStatus.text && <div style={statusStyle(jsonStatus.type)}>{jsonStatus.text}</div>}
        {jsonOutput && <div style={s.jsonBox}>{jsonOutput}</div>}
      </div>
    </div>
  );
}
