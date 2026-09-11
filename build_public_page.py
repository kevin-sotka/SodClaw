#!/usr/bin/env python3
"""
Build the PUBLIC portfolio page for meatbagmade.com/projects.

Reads projects/portfolio.json and emits public/projects.html — a self-contained
HTML *fragment* (scoped <style> + markup, all classes prefixed `mbm-`) meant to be
pasted into a WordPress Custom HTML block. No <html>/<head>/<body>, no JS, no
external assets (Doc's portrait is embedded base64).

Rules (see prompts/doc_voice.md → "Public copy"):
- Only projects with a `public` field are shown (live + active; shelved/paused stay private).
- No progress %, scores, decisions, or next actions on the public surface.
- Blurbs and intro are Doc's voice. Edit them in portfolio.json, not here.
- A project's `public.name` overrides the card title; without it the title is the
  project name up to the em dash. Use it when the internal name is not the public one.

Usage:  python3 build_public_page.py
Also writes public/projects-preview.html (full document) for local browser preview.
"""
import json, os, base64, html, datetime
from io import BytesIO

ROOT = os.path.dirname(os.path.abspath(__file__))
PF_PATH = os.path.join(ROOT, "projects", "portfolio.json")
OUT_DIR = os.path.join(ROOT, "public")

LABEL_ORDER = {"Live": 0, "Shipped": 1, "On the workbench": 2}
LABEL_CLASS = {"Shipped": "ship", "Live": "live", "On the workbench": "bench"}


def doc_portrait():
    """Small base64 portrait so the fragment stays paste-able."""
    path = os.path.join(ROOT, "assets", "doc.png")
    if not os.path.exists(path):
        return ""
    try:
        from PIL import Image
        im = Image.open(path).convert("RGBA")
        im.thumbnail((148, 148))
        buf = BytesIO()
        im.save(buf, "PNG", optimize=True)
        data = buf.getvalue()
    except Exception:
        with open(path, "rb") as f:
            data = f.read()
    return "data:image/png;base64," + base64.b64encode(data).decode()


CSS = """
.mbm-projects{--paper:#f4ead2;--card:#fffdf6;--ink:#2b2520;--rule:#2b2520;--line:#d8c9a6;
  --gold:#c08a2e;--gold-d:#8a6212;--gold-bg:#f1e2bd;--green:#1f6b46;--green-bg:#dfeede;
  --rust:#9a5b2b;--rust-bg:#f0ddc6;--slate:#5b5346;--slate-bg:#e4ddcd;--faint:#8a7f6d;
  --serif:Georgia,'Times New Roman',serif;
  background:var(--paper);color:var(--ink);font-family:var(--serif);
  padding:28px 22px;border:2px solid var(--rule);border-radius:6px;max-width:860px;margin:0 auto;
  box-sizing:border-box}
.mbm-projects *{box-sizing:border-box}
.mbm-hd{text-align:center;border-bottom:3px double var(--rule);padding-bottom:16px;margin-bottom:18px}
.mbm-hd h2{font-family:var(--serif);font-size:30px;letter-spacing:.06em;text-transform:uppercase;
  margin:0 0 4px;color:var(--ink)}
.mbm-hd .mbm-sub{font-style:italic;color:var(--faint);font-size:14px;margin:0}
.mbm-doc{display:flex;gap:14px;align-items:flex-start;background:var(--card);
  border:2px solid var(--rule);border-radius:6px;padding:14px 16px;margin-bottom:24px}
.mbm-doc img{width:74px;height:74px;border-radius:50%;border:2px solid var(--rule);
  object-fit:cover;flex:none;background:var(--slate-bg)}
.mbm-doc .mbm-label{font-size:12px;font-weight:800;letter-spacing:.12em;
  text-transform:uppercase;color:var(--gold-d);margin:0}
.mbm-doc .mbm-text{font-style:italic;font-size:15.5px;line-height:1.6;margin:5px 0 0}
.mbm-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:16px}
.mbm-card{background:var(--card);border:2px solid var(--rule);border-radius:6px;
  padding:16px 16px 14px;display:flex;flex-direction:column;gap:8px}
.mbm-card h3{margin:0;font-size:18px;line-height:1.3;color:var(--ink)}
.mbm-badge{align-self:flex-start;font-size:11px;font-weight:800;letter-spacing:.1em;
  text-transform:uppercase;padding:3px 9px;border-radius:3px;border:1px solid currentColor}
.mbm-badge.ship{color:var(--green);background:var(--green-bg)}
.mbm-badge.live{color:var(--gold-d);background:var(--gold-bg)}
.mbm-badge.bench{color:var(--rust);background:var(--rust-bg)}
.mbm-card p{margin:0;font-size:14.5px;line-height:1.55;font-style:italic;color:var(--slate);flex:1}
.mbm-btn{display:inline-block;align-self:flex-start;margin-top:4px;padding:7px 14px;
  background:var(--ink);color:var(--paper) !important;text-decoration:none;font-size:13px;
  font-weight:700;letter-spacing:.06em;text-transform:uppercase;border-radius:4px;
  border:1px solid var(--rule)}
.mbm-btn:hover{background:var(--gold-d)}
.mbm-ft{margin-top:24px;padding-top:12px;border-top:3px double var(--rule);
  text-align:center;font-style:italic;color:var(--faint);font-size:13px}
"""


def build():
    pf = json.load(open(PF_PATH))
    cfg = pf["_meta"].get("public_page", {})
    intro = cfg.get("doc_intro", "")
    pubs = [p for p in pf["projects"] if p.get("public")]
    pubs.sort(key=lambda p: (LABEL_ORDER.get(p["public"]["label"], 9),
                             0 if p["public"].get("link") else 1))

    cards = []
    for p in pubs:
        pub = p["public"]
        name = html.escape(pub.get("name") or p["name"].split("—")[0].strip())
        badge = f'<span class="mbm-badge {LABEL_CLASS.get(pub["label"], "bench")}">{html.escape(pub["label"])}</span>'
        btn = ""
        if pub.get("link"):
            btn = (f'<a class="mbm-btn" href="{html.escape(pub["link"])}" '
                   f'target="_blank" rel="noopener">{html.escape(pub.get("link_text") or "Take a look")}</a>')
        cards.append(
            f'<div class="mbm-card">{badge}<h3>{name}</h3>'
            f'<p>{html.escape(pub["blurb"])}</p>{btn}</div>')

    portrait = doc_portrait()
    img = f'<img src="{portrait}" alt="Doc, your frontier guide">' if portrait else ""
    fragment = f"""<!-- Generated by SodClaw/build_public_page.py — do not hand-edit.
     Source of truth: SodClaw/projects/portfolio.json (public fields). -->
<style>{CSS}</style>
<div class="mbm-projects">
  <div class="mbm-hd">
    <h2>The Meatbag Labs Territory</h2>
    <p class="mbm-sub">Games, gazettes &amp; other claims staked by Kevin Sotka</p>
  </div>
  <div class="mbm-doc">{img}
    <div>
      <p class="mbm-label">Doc says</p>
      <p class="mbm-text">{html.escape(intro)}</p>
    </div>
  </div>
  <div class="mbm-grid">
    {''.join(cards)}
  </div>
  <p class="mbm-ft">New claims get staked all the time. Ride back through whenever you're in the territory.</p>
</div>
"""
    # ASCII-safe: encode em dashes etc. as HTML entities so the fragment
    # renders correctly even when opened without a charset declaration.
    fragment = fragment.encode("ascii", "xmlcharrefreplace").decode("ascii")

    os.makedirs(OUT_DIR, exist_ok=True)
    frag_path = os.path.join(OUT_DIR, "projects.html")
    with open(frag_path, "w") as f:
        f.write(fragment)
    with open(os.path.join(OUT_DIR, "projects-preview.html"), "w") as f:
        f.write("<!doctype html><html><head><meta charset='utf-8'>"
                "<meta name='viewport' content='width=device-width,initial-scale=1'>"
                "<title>Preview — /projects</title></head><body style='margin:20px;background:#e8e0cf'>"
                + fragment + "</body></html>")

    cfg["last_generated"] = datetime.date.today().isoformat()
    pf["_meta"]["public_page"] = cfg
    json.dump(pf, open(PF_PATH, "w"), indent=2, ensure_ascii=False)

    missing = [p["name"] for p in pubs if not p["public"].get("link")]
    print(f"Built {frag_path} — {len(pubs)} projects, {os.path.getsize(frag_path)//1024} KB")
    if missing:
        print("No public link yet (shown without a button):")
        for m in missing:
            print("  -", m)


if __name__ == "__main__":
    build()
