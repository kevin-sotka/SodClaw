#!/usr/bin/env python3
"""
Build SodClaw/dashboard.html from portfolio.json.

The dashboard is GENERATED, not hand-edited. Change projects/portfolio.json
(status, scores, next_action, decision, _meta.doc_briefing), then run:

    python3 SodClaw/build_dashboard.py

...and re-publish the "sodclaw-portfolio-command-center" artifact. This keeps
the dashboard and the source-of-truth JSON from ever drifting apart.

Wild-west / "AI Company Trail" theme: parchment, gold, slate, Doc's portrait,
serif briefing. Light-mode only (Cowork artifact).
"""
import os, io, json, base64

ROOT = os.path.dirname(os.path.abspath(__file__))

pf = json.load(open(os.path.join(ROOT, "projects", "portfolio.json")))
keys = ["id","name","tier","status","autonomy","progress","value","complexity","next_action","decision","git_state"]
projects = [{k: p.get(k) for k in keys} for p in pf["projects"]]
data = {"last_updated": pf["_meta"].get("last_updated"), "projects": projects,
        "sodclaw_git_state": pf["_meta"].get("sodclaw_git_state"),
        # Projects that need to be reachable from mobile (Claude Code) — SodClaw
        # (the orchestrator entry point) is handled separately via sodclaw_git_state.
        "git_priority": ["train_lore", "the_wall", "gridiron_gazette"]}
briefing = pf["_meta"].get("doc_briefing", "")
bdate = pf["_meta"].get("doc_briefing_date", "")

# ---- Static SVG value-vs-complexity scatter (no external lib; always renders) ----
TIER_C = {"autonomous": "#1f6b46", "active": "#c08a2e", "exploratory": "#9a5b2b"}

def _esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;"))

def build_scatter(projs):
    W, H = 660, 320
    PX0, PX1, PY0, PY1 = 46, 644, 14, 284  # plot box
    def sx(c): return PX0 + (c - 0.5) / 5.0 * (PX1 - PX0)
    def sy(v): return PY1 - (v - 0.5) / 5.0 * (PY1 - PY0)
    parts = ['<svg viewBox="0 0 %d %d" width="100%%" height="100%%" preserveAspectRatio="xMidYMid meet" '
             'xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Value versus complexity scatter of all projects.">' % (W, H)]
    ink, faint, gridc = "#3a2d18", "#6b5a3c", "rgba(74,58,36,.20)"
    # gridlines + ticks 1..5
    for n in range(1, 6):
        x = sx(n); y = sy(n)
        parts.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="1"/>' % (x, PY0, x, PY1, gridc))
        parts.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="%s" stroke-width="1"/>' % (PX0, y, PX1, y, gridc))
        parts.append('<text x="%.1f" y="%d" font-size="10" fill="%s" text-anchor="middle">%d</text>' % (x, PY1 + 15, faint, n))
        parts.append('<text x="%d" y="%.1f" font-size="10" fill="%s" text-anchor="end">%d</text>' % (PX0 - 6, y + 3, faint, n))
    # axis titles
    parts.append('<text x="%d" y="%d" font-size="11" fill="%s" text-anchor="middle">complexity &#8594;</text>' % ((PX0 + PX1) // 2, H - 2, ink))
    parts.append('<text transform="translate(11,%d) rotate(-90)" font-size="11" fill="%s" text-anchor="middle">value &#8594;</text>' % ((PY0 + PY1) // 2, ink))
    # bubbles (draw larger first so small ones stay clickable on top)
    pts = sorted(projs, key=lambda p: -(6 + p["progress"] / 8.0))
    for p in pts:
        V = sum(p["value"].values()) / 4.0
        C = sum(p["complexity"].values()) / 4.0
        cx, cy, r = sx(C), sy(V), 6 + p["progress"] / 8.0
        col = TIER_C.get(p["tier"], "#9a5b2b")
        short = p["name"].split(" — ")[0]
        if len(short) > 12: short = short[:11] + "…"
        anchor, lx = ("end", cx - r - 4) if cx > PX1 - 70 else ("start", cx + r + 4)
        parts.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" fill-opacity="0.82" stroke="#2b2520" stroke-width="1.5">'
                     '<title>%s — value %.1f, complexity %.1f, %d%%</title></circle>'
                     % (cx, cy, r, col, _esc(p["name"]), V, C, p["progress"]))
        parts.append('<text x="%.1f" y="%.1f" font-size="9.5" fill="%s" text-anchor="%s">%s</text>'
                     % (lx, cy + 3, ink, anchor, _esc(short)))
    parts.append('</svg>')
    return "".join(parts)

scatter_svg = build_scatter(projects)

# Doc portrait -> small base64 data URL (self-contained artifact)
doc_url = ""
doc_path = os.path.join(ROOT, "assets", "doc.png")
if os.path.exists(doc_path):
    try:
        from PIL import Image
        im = Image.open(doc_path).convert("RGBA")
        im.thumbnail((200, 200))
        buf = io.BytesIO(); im.save(buf, format="PNG", optimize=True)
        doc_url = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()
    except Exception:
        with open(doc_path, "rb") as f:
            doc_url = "data:image/png;base64," + base64.b64encode(f.read()).decode()

TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Meatbag Labs — Command Center</title>
<style>
:root{
  color-scheme: light;
  --paper:#f4ead2; --paper2:#fbf5e6; --card:#fffdf6; --ink:#2b2520; --ink2:#5c5347; --faint:#8a7f6d;
  --gold:#c08a2e; --gold-d:#8a6212; --gold-bg:#f1e2bd;
  --rule:#2b2520; --line:#d8c9a6;
  --green:#1f6b46; --green-bg:#dfeede; --rust:#9a5b2b; --rust-bg:#f0ddc6;
  --slate:#5b5346; --slate-bg:#e4ddcd; --red:#9a3322; --red-bg:#f4d9cf;
  --hd:"Helvetica Neue",Arial,sans-serif; --serif:Georgia,"Times New Roman",serif;
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font-size:15px;line-height:1.55;
  padding:18px;background-image:radial-gradient(var(--line) 0.5px, transparent 0.5px);background-size:16px 16px}
.frame{border:2px solid var(--rule);background:var(--paper2);padding:18px 18px 28px;
  box-shadow:6px 6px 0 rgba(43,37,32,.18)}
h1{font-family:var(--hd);font-size:23px;font-weight:800;letter-spacing:.04em;text-transform:uppercase;margin:0;display:flex;align-items:center;gap:9px}
h1 .ti{color:var(--gold);font-size:22px}
.sub{color:var(--ink2);font-size:12.5px;margin:5px 0 0;font-style:italic}
.hr{height:2px;background:var(--rule);margin:12px 0 0}
h2{font-family:var(--hd);font-size:15px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;margin:26px 0 12px;display:flex;align-items:center;gap:8px}
h2 .ti{color:var(--gold);font-size:17px}
.sr-only{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}

.doc{display:flex;gap:14px;align-items:flex-start;background:var(--card);border:2px solid var(--rule);
  box-shadow:5px 5px 0 rgba(43,37,32,.16);padding:15px 16px;margin-top:16px}
.doc img{width:74px;height:74px;border-radius:50%;border:2px solid var(--rule);object-fit:cover;flex:none;background:var(--slate-bg)}
.doc .label{font-family:var(--hd);font-size:12px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:var(--gold-d)}
.doc .text{font-family:var(--serif);font-style:italic;font-size:15.5px;line-height:1.6;color:var(--ink);margin:5px 0 0}
.doc .date{font-size:11px;color:var(--faint);text-transform:uppercase;letter-spacing:.08em;margin-top:7px}

.metrics{display:grid;grid-template-columns:repeat(auto-fit,minmax(110px,1fr));gap:10px;margin-top:16px}
.metric{background:var(--card);border:1.5px solid var(--rule);padding:11px 13px}
.metric .lab{font-size:11px;color:var(--ink2);text-transform:uppercase;letter-spacing:.06em}
.metric .val{font-family:var(--hd);font-size:25px;font-weight:800;margin-top:3px;color:var(--ink)}
.metric .val small{font-size:13px;font-weight:700;color:var(--ink2)}

.attn{background:var(--card);border:1.5px solid var(--rule);border-left:6px solid var(--gold);padding:11px 14px;margin:10px 0;box-shadow:3px 3px 0 rgba(43,37,32,.12)}
.attn.eighty{border-left-color:var(--red)}
.attn.git{border-left-color:var(--slate)}
.attn .tag{display:inline-block;font-family:var(--hd);font-size:10.5px;font-weight:800;text-transform:uppercase;letter-spacing:.06em;padding:2px 8px;margin-bottom:5px;border:1px solid var(--rule)}
.attn .tag.dec{background:var(--gold-bg);color:var(--gold-d)}
.attn .tag.eig{background:var(--red-bg);color:var(--red)}
.attn .tag.git{background:var(--slate-bg);color:var(--slate)}
.attn .nm{font-weight:700;font-size:14px}
.attn .why{font-size:13.5px;margin-top:3px}

.controls{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:14px 0 4px}
.controls label{font-size:11px;color:var(--ink2);text-transform:uppercase;letter-spacing:.06em}
select{font-family:inherit;font-size:13px;padding:6px 8px;border:1.5px solid var(--rule);background:var(--card);color:var(--ink)}

.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(258px,1fr));gap:12px;margin-top:4px}
.card{background:var(--card);border:1.5px solid var(--rule);padding:13px 14px;display:flex;flex-direction:column;gap:9px;box-shadow:3px 3px 0 rgba(43,37,32,.12)}
.card.flag{border-color:var(--gold);box-shadow:3px 3px 0 var(--gold-bg)}
.card .top{display:flex;justify-content:space-between;align-items:flex-start;gap:8px}
.card .nm{font-weight:700;font-size:14.5px;line-height:1.25}
.pill{font-family:var(--hd);font-size:10px;font-weight:800;padding:2px 8px;text-transform:uppercase;letter-spacing:.05em;white-space:nowrap;border:1px solid var(--rule)}
.p-active{background:var(--green-bg);color:var(--green)} .p-dormant{background:var(--gold-bg);color:var(--gold-d)}
.p-paused{background:var(--slate-bg);color:var(--slate)} .p-shipped{background:var(--green-bg);color:var(--green)}
.p-unknown{background:var(--gold-bg);color:var(--gold-d)} .p-shelved{background:var(--slate-bg);color:var(--slate)}
.p-launched-shelved{background:var(--slate-bg);color:var(--slate)}
.meta{display:flex;gap:6px;flex-wrap:wrap;align-items:center}
.chip{font-size:11px;color:var(--ink2);background:var(--paper);border:1px solid var(--line);padding:2px 7px}
.chip b{color:var(--ink);font-weight:700}
.dot{width:8px;height:8px;border-radius:50%;display:inline-block;margin-right:5px;vertical-align:1px}
.bar{height:8px;background:var(--paper);border:1px solid var(--rule);overflow:hidden}
.bar > span{display:block;height:100%}
.barrow{display:flex;align-items:center;gap:8px}
.barrow .pct{font-family:var(--hd);font-size:12px;font-weight:800;min-width:34px;text-align:right}
.next{font-size:13px}
.next .k{color:var(--faint);font-size:10.5px;text-transform:uppercase;letter-spacing:.06em;display:block;margin-bottom:1px}
.dec{font-size:12.5px;color:var(--gold-d);background:var(--gold-bg);border:1px solid var(--line);padding:7px 9px}
.acts{display:flex;gap:7px}
button.act{font-family:var(--hd);font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.04em;padding:6px 11px;border:1.5px solid var(--rule);background:var(--card);color:var(--ink);cursor:pointer}
button.act:hover{background:var(--gold-bg)}
button.act.pri{background:var(--gold);color:#fff;border-color:var(--gold-d)}
.chartwrap{background:var(--card);border:1.5px solid var(--rule);padding:15px 15px 9px;margin-top:6px;box-shadow:3px 3px 0 rgba(43,37,32,.12)}
.legend{display:flex;flex-wrap:wrap;gap:13px;font-size:11.5px;color:var(--ink2);margin-bottom:10px}
.legend span{display:flex;align-items:center;gap:5px}
.legend i{width:11px;height:11px;display:inline-block;border:1px solid var(--rule)}
.prairie{position:relative;width:100%;height:330px;border:1.5px solid var(--rule);overflow:hidden;
  background:
   radial-gradient(150px 150px at 78% 26%, rgba(255,247,222,.95), rgba(255,226,158,0) 70%),
   linear-gradient(to bottom,#ffd49b 0%,#fcbd76 26%,#f7a85c 46%,#ecbf78 58%,#ddb068 74%,#cda259 100%)}
.prairie .hills{position:absolute;left:0;right:0;bottom:0;height:54px;
  background:
   radial-gradient(120% 70px at 22% 130%, #8f6234 0 62%, transparent 63%),
   radial-gradient(120% 90px at 74% 135%, #7d5026 0 62%, transparent 63%);opacity:.5}
.prairie svg{position:relative;z-index:2;display:block}
.foot{color:var(--faint);font-size:11.5px;margin-top:24px;border-top:2px solid var(--rule);padding-top:11px;font-style:italic}
</style>
</head>
<body>
<div class="frame">
<span class="sr-only">Meatbag Labs portfolio command center, wild-west themed: Doc's briefing, project pipeline by tier with status, progress, value and complexity scores, and a panel of items needing attention.</span>

<h1><span class="ti">&#9650;</span> Meatbag Labs &mdash; Command Center</h1>
<p class="sub" id="subline"></p>
<div class="hr"></div>

<div class="doc">
  <img src="%%DOC_IMG%%" alt="Doc, the trail guide">
  <div>
    <div class="label">Doc&#39;s Wisdom</div>
    <p class="text">%%BRIEFING%%</p>
    <div class="date">Dispatch &middot; %%DATE%%</div>
  </div>
</div>

<div class="metrics" id="metrics"></div>

<h2><span class="ti">&#9888;</span> Needs your attention</h2>
<div id="attention"></div>

<h2><span class="ti">&#9906;</span> Git readiness &mdash; mobile access</h2>
<div id="gitreadiness"></div>

<h2><span class="ti">&#9878;</span> Value vs. complexity</h2>
<div class="chartwrap">
  <div class="legend">
    <span><i style="background:#1f6b46"></i>Autonomous</span>
    <span><i style="background:#c08a2e"></i>Active</span>
    <span><i style="background:#9a5b2b"></i>Exploratory</span>
    <span style="color:var(--faint)">bubble = progress &middot; top-left is the gold</span>
  </div>
  <div class="prairie">
    <div class="hills" aria-hidden="true"></div>
    %%SCATTER%%
  </div>
</div>

<div class="controls">
  <label>Sort</label>
  <select id="sort">
    <option value="attention">Needs attention first</option>
    <option value="value">Value (high to low)</option>
    <option value="progress">Progress (high to low)</option>
    <option value="complexity">Complexity (low to high)</option>
    <option value="ratio">Value / complexity</option>
  </select>
  <label style="margin-left:6px">Tier</label>
  <select id="ftier">
    <option value="all">All groups</option>
    <option value="autonomous">Autonomous</option>
    <option value="active">Active</option>
    <option value="exploratory">Exploratory</option>
    <option value="launched-shelved">Launched · shelved</option>
  </select>
</div>

<div id="pipeline"></div>

<p class="foot" id="foot"></p>
</div>

<script>
const DATA = %%DATA%%;
const TIER={autonomous:{c:"#1f6b46",label:"Autonomous"},active:{c:"#c08a2e",label:"Active"},exploratory:{c:"#9a5b2b",label:"Exploratory"}};
const GROUPS=[
  {key:"autonomous",label:"Autonomous",c:"#1f6b46",test:p=>p.tier==="autonomous"&&p.status!=="launched-shelved"},
  {key:"active",label:"Active",c:"#c08a2e",test:p=>p.tier==="active"&&p.status!=="launched-shelved"},
  {key:"exploratory",label:"Exploratory",c:"#9a5b2b",test:p=>p.tier==="exploratory"&&p.status!=="launched-shelved"},
  {key:"launched-shelved",label:"Launched · shelved",c:"#5b5346",test:p=>p.status==="launched-shelved"}
];
const TERMINAL=["shipped","shelved","paused","launched-shelved"];
const GIT_PRIORITY=DATA.git_priority||[];
const mean=o=>{const v=Object.values(o);return v.reduce((a,b)=>a+b,0)/v.length;};
// Reason a thing isn't mobile-reachable yet, or null if it's fine.
function gitReason(gs,isPriority){
  if(!gs) return null;
  if(gs.state==="not_a_repo") return isPriority?"Priority project, not in Git yet — unreachable from mobile until it has a repo + remote.":null;
  if(gs.state==="local_only") return "Repo exists but has no remote — add a private GitHub remote to make it portable.";
  if(gs.state==="partially_synced") return "In Git but drifted: "+(gs.uncommitted||0)+" uncommitted"+(gs.unpushed?(", "+gs.unpushed+" unpushed"):"")+".";
  return null;
}
DATA.projects.forEach(p=>{p.V=mean(p.value);p.C=mean(p.complexity);p.flag=(p.decision!==null)||(p.progress>=80 && !TERMINAL.includes(p.status));p.gitReason=gitReason(p.git_state,GIT_PRIORITY.includes(p.id));});
function barColor(p){return p>=80?"#1f6b46":p>=50?"#c08a2e":p>=25?"#9a5b2b":"#9a3322";}
function esc(s){return (s||"").replace(/'/g,"\\'").replace(/\n/g," ");}
function act(cmd){
  try{ if(typeof sendPrompt==="function"){sendPrompt(cmd);return;} }catch(e){}
  try{ if(window.cowork&&typeof window.cowork.sendPrompt==="function"){window.cowork.sendPrompt(cmd);return;} }catch(e){}
  try{ navigator.clipboard.writeText(cmd); }catch(e){}
  alert("Copied to clipboard — paste into chat:\n\n"+cmd);
}
function renderMetrics(){
  const ps=DATA.projects, n=ps.length;
  const attn=ps.filter(p=>p.flag).length;
  const avg=Math.round(ps.reduce((a,p)=>a+p.progress,0)/n);
  const live=ps.filter(p=>["active","dormant","shipped"].includes(p.status)).length;
  const eighty=ps.filter(p=>p.progress>=80).length;
  document.getElementById("metrics").innerHTML=[
    ["Claims",n,""],["Need you",attn,""],["Avg progress",avg,"<small>%</small>"],
    ["Live",live,""],["Near done",eighty,""]
  ].map(([l,v,s])=>`<div class="metric"><div class="lab">${l}</div><div class="val">${v}${s}</div></div>`).join("");
}
function renderAttention(){
  const items=DATA.projects.filter(p=>p.flag).sort((a,b)=>(b.progress>=80)-(a.progress>=80)||b.V-a.V);
  document.getElementById("attention").innerHTML=items.map(p=>{
    const eighty=p.progress>=80;
    const tag=eighty?`<span class="tag eig">80% watch &middot; ${p.progress}%</span>`:`<span class="tag dec">decision</span>`;
    const why=eighty?(p.decision||`This is ${p.progress}% done. Push through to ship, or consciously shelve?`):p.decision;
    return `<div class="attn ${eighty?'eighty':''}">${tag}<div class="nm">${p.name}</div><div class="why">${why}</div>
      <div class="acts" style="margin-top:8px">
        <button class="act pri" onclick="act('Work on ${esc(p.name)}')">Work on this</button>
        <button class="act" onclick="act('Help me decide on ${esc(p.name)}: ${esc(why)}')">Decide</button>
      </div></div>`;
  }).join("")||`<p class="sub">Nothing flagged. Clean trail.</p>`;
}
function renderGit(){
  const items=[];
  const sod=DATA.sodclaw_git_state;
  // SodClaw is the entry point — always treated as top priority.
  const sr=gitReason(sod,true);
  if(sr) items.push({name:"SodClaw (orchestrator)",why:"The entry point itself isn't in Git. Until SodClaw has a private repo + remote, nothing in Meatbag Labs is reachable from mobile.",top:true});
  DATA.projects.filter(p=>p.gitReason).sort((a,b)=>b.V-a.V).forEach(p=>items.push({name:p.name,why:p.gitReason,top:false}));
  document.getElementById("gitreadiness").innerHTML=items.map(it=>
    `<div class="attn git"><span class="tag git">git</span><div class="nm">${it.name}</div><div class="why">${it.why}</div>
      <div class="acts" style="margin-top:8px">
        <button class="act pri" onclick="act('Get ${esc(it.name)} into a private GitHub repo so I can reach it from mobile')">Set up Git</button>
      </div></div>`).join("")||`<p class="sub">Every priority project is in Git. Mobile can reach the trail.</p>`;
}
function cardHTML(p){
  return `<div class="card ${p.flag?'flag':''}">
    <div class="top"><div class="nm">${p.name}</div><span class="pill p-${p.status}">${p.status.replace('-',' · ')}</span></div>
    <div class="meta">
      <span class="chip"><span class="dot" style="background:${TIER[p.tier].c}"></span>${TIER[p.tier].label}</span>
      <span class="chip">value <b>${p.V.toFixed(1)}</b></span>
      <span class="chip">complexity <b>${p.C.toFixed(1)}</b></span>
    </div>
    <div class="barrow"><div class="bar" style="flex:1"><span style="width:${p.progress}%;background:${barColor(p.progress)}"></span></div><div class="pct">${p.progress}%</div></div>
    <div class="next"><span class="k">Next</span>${p.next_action}</div>
    ${p.decision?`<div class="dec">${p.decision}</div>`:""}
    <div class="acts"><button class="act pri" onclick="act('Work on ${esc(p.name)}')">Work on this</button>
    <button class="act" onclick="act('Give me a status update on ${esc(p.name)}')">Status</button></div>
  </div>`;
}
function renderPipeline(){
  const sort=document.getElementById("sort").value, ftier=document.getElementById("ftier").value;
  const ps=DATA.projects.slice();
  const sorters={
    attention:(a,b)=>(b.flag-a.flag)||((b.progress>=80)-(a.progress>=80))||b.V-a.V,
    value:(a,b)=>b.V-a.V, progress:(a,b)=>b.progress-a.progress,
    complexity:(a,b)=>a.C-b.C, ratio:(a,b)=>(b.V/b.C)-(a.V/a.C)
  };
  let html="";
  GROUPS.forEach(g=>{
    if(ftier!=="all"&&ftier!==g.key)return;
    const grp=ps.filter(g.test).sort(sorters[sort]);
    if(!grp.length)return;
    html+=`<h2><span class="dot" style="background:${g.c}"></span>${g.label} <span class="sub" style="font-weight:400;text-transform:none;letter-spacing:0">&middot; ${grp.length}</span></h2><div class="grid">${grp.map(cardHTML).join("")}</div>`;
  });
  document.getElementById("pipeline").innerHTML=html||`<p class="sub">No claims in this filter.</p>`;
}
function boot(){
  document.getElementById("subline").textContent="Last updated "+DATA.last_updated+" · "+DATA.projects.length+" projects · scores ratified by Kevin";
  document.getElementById("foot").textContent="Source of truth: SodClaw/projects/portfolio.json · generated by build_dashboard.py · a decision surface, not a to-do app.";
  renderMetrics();renderAttention();renderGit();renderPipeline();
  document.getElementById("sort").addEventListener("change",renderPipeline);
  document.getElementById("ftier").addEventListener("change",renderPipeline);
}
if(document.readyState!=="loading")boot(); else document.addEventListener("DOMContentLoaded",boot);
</script>
</body>
</html>
"""

html = (TEMPLATE
        .replace("%%SCATTER%%", scatter_svg)
        .replace("%%DATA%%", json.dumps(data))
        .replace("%%DOC_IMG%%", doc_url)
        .replace("%%BRIEFING%%", briefing)
        .replace("%%DATE%%", bdate))

out = os.path.join(ROOT, "dashboard.html")
with open(out, "w") as f:
    f.write(html)
print("Wrote %s (%d bytes); doc image %d bytes; %d projects" % (out, len(html), len(doc_url), len(projects)))
