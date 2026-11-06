import html, re
from data import SPACES, CATS, PN
from apps import APPS, FIELDS
from cites import PIBASE, PIBASE_URL, STEEN
SPNO = {}
for _ci, _c in enumerate(CATS, 1):
    for _si, _s in enumerate([x for x in SPACES if x["cat"] == _c], 1): SPNO[_s["id"]] = f"{_ci}.{_si}"
SPNAME = {x["id"]: x["n"] for x in SPACES}
ACH = len(CATS) + 1
APPNO = {a["id"]: f"{ACH}.{k}" for k, a in enumerate(APPS, 1)}
SP2APP = {}
for _a in APPS:
    for _sp in _a["spaces"]: SP2APP.setdefault(_sp, []).append(_a)

def e(s): return html.escape(s, quote=False)
def m(s): return "$" + e(s) + "$"
def pv(v): return {1: "yes", 0: "no", "b": "with boundary", None: "—"}.get(v, v)
def svg(i, alt):
    # Figures load as separate files (figs/<id>.svg) instead of being pasted into the page.
    # Why? Inlined, they made up 1.5 MB of a 1.7 MB page, and Safari in the claude.ai viewer
    # did not finish loading the end of the page (the last chapter and the page script).
    # The width and height attributes come from the viewBox, so the browser knows the
    # aspect ratio and reserves the right amount of space before the image arrives.
    t = open(f"figs/{i}.svg").read(400)
    w, h = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', t).groups()
    return f'<img src="figs/{i}.svg" alt="{html.escape(alt)}" width="{round(float(w))}" height="{round(float(h))}" loading="lazy">'

def sources(i):
    # Which outside sources treat this space? Each one becomes a clause in the line.
    parts = []
    for uid, note in PIBASE.get(i, []):
        link = f'<a href="{PIBASE_URL}{uid}" target="_blank" rel="noopener">{uid}</a>'
        parts.append(f"π-Base {link}" + (f" ({e(note)})" if note else ""))
    if i in STEEN:
        ex, pg = STEEN[i]
        parts.append(f"Steen and Seebach, <i>Counterexamples in Topology</i>, Example {ex}, p. {pg}")
    # Is the space in neither source? Then say so, so the reader knows no line was omitted.
    if not parts:
        parts.append("Not listed in the π-Base or in Steen and Seebach")
    return f'<p class="method src"><i>Sources.</i>{"; ".join(parts)}.</p>'

CSS = r"""
/* Layout: a single book page, one column of numbered sections, ink on white paper, no tint or shadow anywhere */
:root { --paper: #ffffff; --ink: #000000; --faint: #000000;
  --serif: "Old Standard TT", "Latin Modern Roman", "Computer Modern Serif", Georgia, "Times New Roman", serif; }
html { background: var(--paper); }
body { background: var(--paper); color: var(--ink); font-family: var(--serif); font-size: 17px; line-height: 1.5;
  -webkit-font-smoothing: antialiased; }
.page { max-width: 36em; margin: 0 auto; overflow-x: clip; padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); padding-block: 28px 80px; }
.runhead { display: flex; justify-content: space-between; font-size: 12px; letter-spacing: .14em; text-transform: uppercase; padding-bottom: 6px; border-bottom: 0.5px solid var(--ink); }
.title { text-align: center; padding-block: 56px 36px; }
.title h1 { font-weight: 400; font-size: clamp(1.9rem, 6vw, 2.6rem); line-height: 1.15; margin: 0 0 14px; text-wrap: balance; }
.title .sub { font-style: italic; margin: 0; }
.title .rule { width: 5em; border-top: 0.5px solid var(--ink); margin: 22px auto; }
h2.chap { font-weight: 400; font-size: 1.45rem; margin: 64px 0 6px; text-align: center; }
h2.chap .num { display: block; font-size: 12px; letter-spacing: .2em; text-transform: uppercase; margin-bottom: 6px; }
.preface p, .entry p, .closing p { margin: 0 0 .7em; text-align: justify; hyphens: auto; -webkit-hyphens: auto; }
.preface p + p, .entry .body p + p { text-indent: 1.5em; }
a { color: var(--ink); }
/* contents */
.toc { margin: 8px 0 0; padding: 0; list-style: none; }
.toc li.c { margin-top: 10px; font-variant: small-caps; letter-spacing: .03em; }
.toc li.s, .toc li.s2 { display: flex; gap: 6px; padding-left: 1.6em; }
.toc li.s2 a, .toc li.s a { text-decoration: none; display: flex; gap: 6px; width: 100%; }
.toc li .lead { flex: 1; border-bottom: 1px dotted var(--ink); transform: translateY(-5px); min-width: 1em; }
.toc li .no { min-width: 2.4em; }
.toc li[hidden] { display: none; }
h4.field { font-weight: 400; font-size: 1.1rem; font-variant: small-caps; letter-spacing: .05em; text-align: center; margin: 48px 0 0; }
.app .spaces { font-size: 15px; text-align: left; }
.app .spaces a, .body a { text-decoration: underline; text-underline-offset: 2px; }
ol.refs { font-size: 14px; margin: 8px 0 0; padding-left: 1.4em; }
ol.refs li { margin-bottom: 3px; }
.fld { font-style: italic; }
/* finder */
.finder { margin: 28px 0 0; font-size: 15px; }
.finder label { font-style: italic; }
#q { width: 100%; box-sizing: border-box; font: inherit; font-size: 16px; border: 0; border-bottom: 0.5px solid var(--ink); background: transparent; color: var(--ink); padding: 6px 0; border-radius: 0; outline: none; }
#q:focus-visible { border-bottom-width: 1.5px; }
summary:focus-visible { outline: 1px dotted var(--ink); outline-offset: 2px; }
#count { font-style: italic; font-size: 14px; margin-top: 6px; }
/* entries */
.entry { margin-top: 44px; }
.entry h3 { font-weight: 700; font-size: 1.12rem; margin: 0 0 6px; }
.entry h3 .no { margin-right: .6em; }
.fig { margin: 18px 0 10px; text-align: center; }
.fig img { display: block; width: 100%; height: auto; max-height: 15em; object-fit: contain; }
.fig.wide img { max-height: 13em; }
.fig figcaption { font-size: 14px; margin-top: 4px; }
.fig figcaption .lab { font-variant: small-caps; letter-spacing: .04em; }
table.inv { border-collapse: collapse; margin: 14px auto 6px; font-size: 16px; }
table.inv td { padding: 3px 10px; vertical-align: baseline; }
table.inv td:first-child { text-align: right; font-style: italic; white-space: nowrap; }
table.inv tr:first-child td { border-top: 1px solid var(--ink); padding-top: 7px; }
table.inv tr:last-child td { border-bottom: 1px solid var(--ink); padding-bottom: 7px; }
.invwrap { overflow-x: auto; }
.props { font-size: 14.5px; text-align: center; margin: 8px 0 12px; line-height: 1.6; }
.props .y::before { content: ""; } .props .n { font-style: italic; }
.method { font-size: 16px; }
.method i { margin-right: .4em; }
details { margin: 4px 0; }
summary { cursor: pointer; list-style: none; font-style: italic; padding: 3px 0; }
summary::-webkit-details-marker { display: none; }
summary::before { content: "\25B8"; display: inline-block; width: 1.1em; font-style: normal; }
details[open] > summary::before { content: "\25BE"; }
.body { padding: 4px 0 8px 1.1em; }
.entry .body p { font-size: 16px; text-align: left; }
.body .k { font-style: italic; margin-right: .35em; }
.entry .body p.qed { text-align: right; text-indent: 0; margin-top: -4px; }
.closing { margin-top: 30px; }
.tbl { overflow-x: auto; margin: 12px 0 18px; }
.tbl table { border-collapse: collapse; margin: 0 auto; font-size: 15px; font-variant-numeric: tabular-nums; }
.tbl th, .tbl td { padding: 4px 9px; text-align: center; white-space: nowrap; }
.tbl tr:first-child th { border-top: 1px solid var(--ink); border-bottom: 0.5px solid var(--ink); font-weight: 400; }
.tbl tr:last-child td, .tbl tr:last-child th { border-bottom: 1px solid var(--ink); }
.tbl th:first-child { border-right: 0.5px solid var(--ink); font-weight: 400; }
.foot { margin-top: 56px; text-align: center; font-size: 13px; }
mjx-container[jax="SVG"][display="true"] { overflow-x: auto; overflow-y: hidden; max-width: 100%; }
.entry[hidden], .chapwrap[hidden] { display: none; }
@media (max-width: 560px) { .runhead span:last-child { display: none; } .runhead { font-size: 11px; } body { font-size: 16px; } .preface p, .entry p, .closing p { text-align: left; } .body { padding-left: .4em; } }
"""

WIDE = {"torus", "klein", "genusg", "rp2", "rose", "graph", "s1vs2", "moore", "rpn", "pseudocircle", "hpn"}

def apps_of(i):
    L = SP2APP.get(i, [])
    if not L: return ""
    items = "".join(f'<p><a href="#{a["id"]}">§{APPNO[a["id"]]} {e(a["title"])}</a> <span class="fld">({e(a["field"].lower())})</span></p>' for a in L)
    return f'<details><summary>Where it appears</summary><div class="body mj-defer">{items}</div></details>'

def app_html(a):
    sp = ", ".join(f'<a href="#{x}">§{SPNO[x]} {e(SPNAME[x])}</a>' for x in a["spaces"])
    fig_ = f'<figure class="fig">{svg(a["fig"], a["title"])}<figcaption><span class="lab">Figure {APPNO[a["id"]]}.</span> {e(a["title"])}.</figcaption></figure>' if a.get("fig") else ""
    refs = "".join(f'<li>{e(t)}' + (f' <a href="{u}" target="_blank" rel="noopener">Link</a>' if u else "") + '</li>' for t, u in a["refs"])
    return f'''<section class="entry app" id="{a["id"]}"><h3><span class="no">§{APPNO[a["id"]]}</span>{e(a["title"])}</h3>
<p class="spaces"><i>Spaces:</i> {sp}.&ensp;<i>Invariant:</i> {m(a["inv"])}.</p>{fig_}
<p>{e(a["text"])}</p><ol class="refs">{refs}</ol></section>'''

def entry(s, no):
    props = "; ".join(f'{PN[i]}: <span class="{"n" if v == 0 else "y"}">{e(pv(v))}</span>' for i, v in enumerate(s["p"]))
    ps = "".join(f'<p><span class="k">{e(k)}.</span>{e(v)}</p>' for k, v in s["ps"])
    al = "".join(f'<p><span class="k">{e(k)}.</span>{e(v)}</p>' for k, v in s["alg"])
    return f'''<section class="entry" id="{s["id"]}" data-i="{SPACES.index(s)}">
<h3><span class="no">§{no}</span>{e(s["n"])}</h3>
<p>{m(s["sym"])}. {e(s["d"])}</p>
<figure class="fig{' wide' if s['id'] in WIDE else ''}">{svg(s["id"], s["n"])}<figcaption><span class="lab">Figure {no}.</span> {e(s["n"])}.</figcaption></figure>
<div class="invwrap"><table class="inv"><tr><td>{m(r"\pi_1")}</td><td>{m(s["pi"])}</td></tr><tr><td>{m(r"H_0,H_1,\dots")}</td><td>{m(s["H"])}</td></tr><tr><td>{m(r"\chi")}</td><td>{m(s["chi"])}</td></tr></table></div>
<p class="props">{props}</p>
<p class="method"><i>Method.</i>{e(s["how"])}</p>
{sources(s["id"])}
<details><summary>Derivation of the point-set properties</summary><div class="body mj-defer">{ps}<p class="qed">∎</p></div></details>
<details><summary>Derivation of the fundamental group and homology</summary><div class="body mj-defer">{al}<p class="qed">∎</p></div></details>
<details><summary>Why it is in the zoo</summary><div class="body mj-defer"><p>{e(s["why"])}</p></div></details>{apps_of(s["id"])}
</section>'''

toc, chaps = [], []
for ci, c in enumerate(CATS, 1):
    toc.append(f'<li class="c" data-c="{ci}">{ci}.&ensp;{e(c)}</li>')
    items = [s for s in SPACES if s["cat"] == c]; secs = []
    for si, s in enumerate(items, 1):
        no = f"{ci}.{si}"; s["no"] = no
        toc.append(f'<li class="s" data-i="{SPACES.index(s)}"><a href="#{s["id"]}"><span class="no">{no}</span><span>{e(s["n"])}</span><span class="lead"></span></a></li>')
        secs.append(entry(s, no))
    chaps.append(f'<div class="chapwrap" data-c="{ci}"><h2 class="chap"><span class="num">Chapter {ci}</span>{e(c)}</h2>' + "\n".join(secs) + "</div>")

import json
data_js = json.dumps([{"t": (s["n"] + " " + s["cat"] + " " + s["sym"] + " " + s["d"] + " " + s["pi"] + " " + s["H"] + " " + s["how"] + " " + s["why"] + " " + " ".join(k + " " + v for k, v in s["ps"] + s["alg"])).lower()} for s in SPACES])

APPCH = f'<div class="chapwrap-app" id="apps"><h2 class="chap"><span class="num">Chapter {ACH}</span>Why we care: applications</h2>' \
  + '<div class="preface"><p>The spaces in this zoo were not invented for their own sake. Each section below names a problem from physics, data analysis, music theory, engineering, or economics, the spaces it uses, and the invariant that does the work. Links lead back to the entries where those invariants are derived.</p></div>' \
  + "".join(f'<h4 class="field">{e(fl)}</h4>' + "".join(app_html(a) for a in APPS if a["field"] == fl) for fl in FIELDS) + '</div>'
apptoc = f'<li class="c"><a href="#apps" style="text-decoration:none">{ACH}.&ensp;Why we care: applications</a></li>' + "".join(
  f'<li class="s2"><a href="#{a["id"]}"><span class="no">{APPNO[a["id"]]}</span><span>{e(a["title"])}</span><span class="lead"></span></a></li>' for a in APPS)

HARD = r"""
<div class="chapwrap closing" id="hard"><h2 class="chap"><span class="num">Chapter %d</span>Where computation gets hard</h2>
<p>Homology of $S^n$ vanishes above degree $n$, yet $\pi_k(S^n)$ is nonzero for infinitely many $k$ when $n\ge 2$, and no closed formula is known. The table gives $\pi_k(S^n)$.</p>
<div class="tbl"><table>
<tr><th></th><th>$\pi_1$</th><th>$\pi_2$</th><th>$\pi_3$</th><th>$\pi_4$</th><th>$\pi_5$</th><th>$\pi_6$</th><th>$\pi_7$</th><th>$\pi_8$</th></tr>
<tr><th>$S^1$</th><td>$\mathbb{Z}$</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr>
<tr><th>$S^2$</th><td>0</td><td>$\mathbb{Z}$</td><td>$\mathbb{Z}$</td><td>$\mathbb{Z}_2$</td><td>$\mathbb{Z}_2$</td><td>$\mathbb{Z}_{12}$</td><td>$\mathbb{Z}_2$</td><td>$\mathbb{Z}_2$</td></tr>
<tr><th>$S^3$</th><td>0</td><td>0</td><td>$\mathbb{Z}$</td><td>$\mathbb{Z}_2$</td><td>$\mathbb{Z}_2$</td><td>$\mathbb{Z}_{12}$</td><td>$\mathbb{Z}_2$</td><td>$\mathbb{Z}_2$</td></tr>
<tr><th>$S^4$</th><td>0</td><td>0</td><td>0</td><td>$\mathbb{Z}$</td><td>$\mathbb{Z}_2$</td><td>$\mathbb{Z}_2$</td><td>$\mathbb{Z}\oplus\mathbb{Z}_{12}$</td><td>$\mathbb{Z}_2^2$</td></tr>
<tr><th>$S^5$</th><td>0</td><td>0</td><td>0</td><td>0</td><td>$\mathbb{Z}$</td><td>$\mathbb{Z}_2$</td><td>$\mathbb{Z}_2$</td><td>$\mathbb{Z}_{24}$</td></tr>
</table></div>
<p>For fundamental groups the obstruction is logical. Every finitely presented group is $\pi_1$ of some closed 4-manifold, and by the Adian–Rabin theorem no algorithm decides whether a finite presentation defines the trivial group. So no algorithm takes a triangulated 4-manifold and decides whether it is simply connected. In dimension 3, geometrization makes the word problem for fundamental groups solvable.</p>
<p>The third difficulty is wild local behavior. Van Kampen's theorem and covering space theory assume open sets that are path-connected and semilocally simply connected. The Hawaiian earring, the Warsaw circle and the solenoid break these hypotheses, and their singular invariants stop agreeing with Čech invariants or with intuition.</p>
<h2 class="chap" style="margin-top:44px">References</h2>
<p>A. Hatcher, <a href="https://pi.math.cornell.edu/~hatcher/AT/ATpage.html" target="_blank" rel="noopener"><i>Algebraic Topology</i></a>, Cambridge, 2002, free online. L. A. Steen and J. A. Seebach, Jr., <i>Counterexamples in Topology</i>, 2nd ed., Springer-Verlag, New York, 1978; Dover reprint, 1995. The π-Base Community, S. Clontz, and J. Dabbs, <a href="https://topology.pi-base.org/" target="_blank" rel="noopener">π-Base</a>, a community database of topological counterexamples, data at <a href="https://github.com/pi-base/data" target="_blank" rel="noopener">github.com/pi-base/data</a>, licensed CC BY 4.0. <a href="https://map.mpim-bonn.mpg.de/" target="_blank" rel="noopener">The Manifold Atlas</a>. <a href="https://knotinfo.math.indiana.edu/" target="_blank" rel="noopener">KnotInfo</a>.</p>
</div>""" % (len(CATS) + 2)

page = f'''<title>Topological Space Zoo</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Old+Standard+TT:ital,wght@0,400;0,700;1,400&display=swap">
<script>
window.MathJax = {{ tex: {{ inlineMath: [['$','$']], processEscapes: true }},
  svg: {{ fontCache: 'global' }}, options: {{ ignoreHtmlClass: 'mj-defer' }} }};
</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-svg.js" defer></script>
<style>{CSS}</style>
<div class="page">
<div class="runhead"><span>A Zoo of Topological Spaces</span><span>Fifty examples</span></div>
<header class="title"><h1>A Zoo of Topological Spaces</h1>
<p class="sub">with their point-set properties, fundamental groups, homology,<br>and the derivations behind them</p><div class="rule"></div></header>
<div class="preface">
<p>Courses in topology state general theorems and then remark that fundamental groups are hard to compute for most spaces, often without showing why. This collection lists concrete spaces, their invariants, and the reasoning that produces them.</p>
<p>This document is a compilation of standard material, prepared with the assistance of an AI model. None of the definitions, properties, or arguments is original to the compiler. Where a space appears in the <a href="https://topology.pi-base.org/" target="_blank" rel="noopener">π-Base</a> or in L. A. Steen and J. A. Seebach, <i>Counterexamples in Topology</i>, its entry gives the π-Base identifier with a link, and the example number and page in Steen and Seebach. The standard reference for the algebraic material is A. Hatcher, <i>Algebraic Topology</i>. Full references are at the end.</p>
<p>Each section gives the space, a figure, a table of invariants, its point-set properties, and derivations that open on request. Chapter {ACH} turns to applications: where these spaces appear in physics, data analysis, music theory, engineering, and economics, and which invariant matters in each case. Homology is singular homology with integer coefficients, listed as $H_0,H_1,H_2,\\dots$ with trailing zeros omitted. Figures are schematic where a faithful picture is impossible. For point-set properties of many further spaces, see the <a href="https://topology.pi-base.org/" target="_blank" rel="noopener">π-Base</a>, built on Steen and Seebach's <i>Counterexamples in Topology</i>.</p>
</div>
<h2 class="chap"><span class="num">Contents</span>Table of Spaces</h2>
<div class="finder"><label for="q">Search the zoo</label>
<input id="q" type="search" autocomplete="off" placeholder="a name, a group, a method: Klein, free group, van Kampen"><div id="count"></div></div>
<ul class="toc">{"".join(toc)}{apptoc}<li class="c"><a href="#hard" style="text-decoration:none">{len(CATS) + 2}.&ensp;Where computation gets hard</a></li></ul>
{"".join(chaps)}
{APPCH}
{HARD}
</div>
<script>
const S = {data_js};
let q = "";
const ents = [...document.querySelectorAll(".entry:not(.app)")], tocs = [...document.querySelectorAll(".toc li.s")];
function apply() {{
  let n = 0; const vis = new Set();
  S.forEach((s, i) => {{
    let ok = !q || q.split(/\\s+/).every(w => s.t.includes(w));
    ents[i].hidden = !ok; tocs[i].hidden = !ok; if (ok) {{ n++; vis.add(ents[i].closest(".chapwrap").dataset.c); }}
  }});
  document.querySelectorAll(".chapwrap[data-c]").forEach(c => c.hidden = !vis.has(c.dataset.c));
  document.querySelectorAll(".toc li.c[data-c]").forEach(c => c.hidden = !vis.has(c.dataset.c));
  document.getElementById("count").textContent = q ? `${{n}} of ${{S.length}} spaces shown.` : `${{S.length}} spaces.`;
}}
document.getElementById("q").addEventListener("input", ev => {{ q = ev.target.value.trim().toLowerCase(); apply(); }});
document.querySelectorAll("details").forEach(d => d.addEventListener("toggle", () => {{
  const b = d.querySelector(".mj-defer"); if (!d.open || !b) return;
  b.classList.remove("mj-defer");
  const go = () => {{
    if (!(window.MathJax && MathJax.startup && MathJax.startup.promise)) return setTimeout(go, 200);
    MathJax.startup.promise = MathJax.startup.promise.then(() => MathJax.typesetPromise([b]))
      .catch(err => {{ console.error(err); b.classList.add("mj-defer"); }});
  }};
  go();
}}));
apply();
</script>'''
open("topology-zoo.html", "w").write(page)
print(len(page) // 1024, "KB")
