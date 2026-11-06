from data import SPACES, CATS, PN
from apps import APPS, FIELDS
from cites import PIBASE, PIBASE_URL, STEEN
SP2APP = {}
for _a in APPS:
    for _sp in _a['spaces']: SP2APP.setdefault(_sp, []).append(_a)
SPNAME = {x['id']: x['n'] for x in SPACES}

def pv(v):
    return {1: "yes", 0: "no", "b": "with boundary", None: "---"}.get(v, v)

pre = r"""\documentclass[11pt,twoside]{book}
\usepackage[utf8]{inputenc}\usepackage[T1]{fontenc}\usepackage{lmodern}
\usepackage{amsmath,amssymb,graphicx,booktabs,array}
\usepackage[margin=1.05in,headheight=14pt]{geometry}
\usepackage{fancyhdr}\pagestyle{fancy}\fancyhf{}
\fancyhead[LE]{\thepage\hfill\textsc{a zoo of topological spaces}}
\fancyhead[RO]{\textsc{\leftmark}\hfill\thepage}\renewcommand{\headrulewidth}{0pt}
\renewcommand{\chaptermark}[1]{\markboth{#1}{}}
\usepackage[hidelinks]{hyperref}
\setlength{\parskip}{3pt}
\newcommand{\entry}[2]{\section{#1}\label{sp:#2}}
\newcommand{\pt}[1]{\par\smallskip\noindent\textit{#1.}\enspace}
\begin{document}
\frontmatter
\begin{titlepage}\centering\vspace*{1.6in}
{\Huge A Zoo of Topological Spaces}\par\vspace{.3in}
{\large Fifty examples with their point-set properties,\\ fundamental groups, homology, derivations, and applications}\par\vfill
{\small Every figure is schematic where a faithful picture is impossible.}\end{titlepage}
\chapter*{Preface}
Courses in topology state general theorems and then say that fundamental groups are hard to compute for most spaces, often without showing why. This collection lists concrete spaces, their invariants, and the reasoning that produces them.

Each entry gives the space, a figure, a table of invariants, a list of point-set properties, and then derivations: first of the point-set properties, then of the fundamental group, homology, and Euler characteristic. Homology is singular homology with integer coefficients, listed as $H_0,H_1,H_2,\dots$; trailing zeros are omitted. The point-set properties of many further spaces can be looked up in the $\pi$-Base database (\texttt{topology.pi-base.org}), which is built on Steen and Seebach's \emph{Counterexamples in Topology}; that database does not record homotopy or homology.

This document is a compilation of standard material, prepared with the assistance of an AI model. None of the definitions, properties, or arguments is original to the compiler. Where a space appears in the $\pi$-Base or in L.~A.~Steen and J.~A.~Seebach, \emph{Counterexamples in Topology}, its entry gives the $\pi$-Base identifier and the example number and page in Steen and Seebach. The standard reference for the algebraic material is A.~Hatcher, \emph{Algebraic Topology}. Full references are at the end.

\tableofcontents
\mainmatter
"""

def sources(i):
    # Which outside sources treat this space? Each one becomes a clause in the line.
    parts = []
    for uid, note in PIBASE.get(i, []):
        parts.append(r"$\pi$-Base \href{" + PIBASE_URL + uid + "}{" + uid + "}" + (f" ({note})" if note else ""))
    if i in STEEN:
        ex, pg = STEEN[i]
        parts.append(rf"Steen and Seebach, \emph{{Counterexamples in Topology}}, Example {ex}, p.~{pg}")
    if not parts:
        parts.append(r"Not listed in the $\pi$-Base or in Steen and Seebach")
    return r"\pt{Sources} " + "; ".join(parts) + "."

def entry(s):
    o = [rf"\entry{{{s['n']}}}{{{s['id']}}}", r"\noindent$" + s["sym"] + r"$.\enspace " + s["d"]]
    o.append(r"\begin{center}\includegraphics[width=" + ("0.82" if s["id"] in WIDE else "0.5") + r"\textwidth,height=2.3in,keepaspectratio]{figs/" + s["id"] + r".pdf}\end{center}")
    o.append(r"\begin{center}\renewcommand{\arraystretch}{1.25}\begin{tabular}{>{\raggedleft\arraybackslash}p{.17\textwidth}p{.68\textwidth}}\toprule")
    o.append(rf"$\pi_1$ & ${s['pi']}$\\ $H_*$ & ${s['H']}$\\ $\chi$ & ${s['chi']}$\\ \midrule")
    props = "; ".join(f"{PN[i]}: {pv(v)}" for i, v in enumerate(s["p"]))
    o.append(rf"properties & \small {props}\\ \bottomrule\end{{tabular}}\end{{center}}")
    o.append(r"\pt{Method} " + s["how"])
    o.append(sources(s["id"]))
    o.append(r"\subsection*{Point-set properties}")
    o += [rf"\pt{{{k}}}{v}" for k, v in s["ps"]]
    o.append(r"\subsection*{Algebraic invariants}")
    o += [rf"\pt{{{k}}}{v}" for k, v in s["alg"]]
    o.append(r"\subsection*{Why it is in the zoo}" + s["why"])
    if s["id"] in SP2APP:
        o.append(r"\pt{Where it appears} " + "; ".join(a["title"] + r" (\S\ref{app:" + a["id"] + "})" for a in SP2APP[s["id"]]) + ".")
    o.append(r"\bigskip")
    return "\n".join(o)

WIDE = {"torus", "klein", "genusg", "rp2", "rose", "graph", "s1vs2", "moore", "rpn", "pseudocircle", "hpn"}

def app_tex(a):
    o = [r"\subsection{" + a["title"] + r"}\label{app:" + a["id"] + "}"]
    o.append(r"\noindent\textit{Spaces:} " + ", ".join(SPNAME[x] + r" (\S\ref{sp:" + x + "})" for x in a["spaces"]) + r".\enspace\textit{Invariant:} $" + a["inv"] + "$.\n")
    if a.get("fig"): o.append(r"\begin{center}\includegraphics[width=0.55\textwidth,height=2.6in,keepaspectratio]{figs/" + a["fig"] + r".pdf}\end{center}")
    o.append(a["text"])
    o.append(r"\begin{list}{}{\leftmargin=1.2em\itemindent=-1.2em\itemsep=0pt}\small " + "".join(r"\item " + t + (r" \url{" + u + "}" if u else "") for t, u in a["refs"]) + r"\end{list}")
    return "\n".join(o)

def apps_chapter():
    o = [r"\chapter{Why we care: applications}",
         "The spaces in this zoo were not invented for their own sake. Each section below names a problem from physics, data analysis, music theory, engineering, or economics, the spaces it uses, and the invariant that does the work, with references back to the entries where those invariants are derived."]
    for fl in FIELDS:
        o.append(r"\section{" + fl + "}")
        o += [app_tex(a) for a in APPS if a["field"] == fl]
    return "\n".join(o)

post = r"""
\chapter{Where computation gets hard}
\section{Homotopy groups of spheres}
Homology of $S^n$ vanishes above degree $n$, yet $\pi_k(S^n)$ is nonzero for infinitely many $k$ when $n\ge2$, and no closed formula is known.
\begin{center}\renewcommand{\arraystretch}{1.2}
\begin{tabular}{c|cccccccc}
 & $\pi_1$ & $\pi_2$ & $\pi_3$ & $\pi_4$ & $\pi_5$ & $\pi_6$ & $\pi_7$ & $\pi_8$\\\hline
$S^1$ & $\mathbb{Z}$ & $0$ & $0$ & $0$ & $0$ & $0$ & $0$ & $0$\\
$S^2$ & $0$ & $\mathbb{Z}$ & $\mathbb{Z}$ & $\mathbb{Z}_2$ & $\mathbb{Z}_2$ & $\mathbb{Z}_{12}$ & $\mathbb{Z}_2$ & $\mathbb{Z}_2$\\
$S^3$ & $0$ & $0$ & $\mathbb{Z}$ & $\mathbb{Z}_2$ & $\mathbb{Z}_2$ & $\mathbb{Z}_{12}$ & $\mathbb{Z}_2$ & $\mathbb{Z}_2$\\
$S^4$ & $0$ & $0$ & $0$ & $\mathbb{Z}$ & $\mathbb{Z}_2$ & $\mathbb{Z}_2$ & $\mathbb{Z}\oplus\mathbb{Z}_{12}$ & $\mathbb{Z}_2^2$\\
$S^5$ & $0$ & $0$ & $0$ & $0$ & $\mathbb{Z}$ & $\mathbb{Z}_2$ & $\mathbb{Z}_2$ & $\mathbb{Z}_{24}$
\end{tabular}\end{center}
\section{Undecidability}
Every finitely presented group is $\pi_1$ of a closed 4-manifold, and by the Adian--Rabin theorem no algorithm decides whether a finite presentation defines the trivial group. So no algorithm takes a triangulated 4-manifold and decides whether it is simply connected. In dimension 3, geometrization makes the word problem for fundamental groups solvable.
\section{Wild local behavior}
Van Kampen's theorem and covering space theory assume open sets that are path-connected and semilocally simply connected. The Hawaiian earring, the Warsaw circle, and the solenoid break these hypotheses, and their singular invariants stop agreeing with \v{C}ech invariants or with intuition.
\section{References}
A.~Hatcher, \emph{Algebraic Topology}, Cambridge, 2002 (free online). L.~A.~Steen and J.~A.~Seebach, Jr., \emph{Counterexamples in Topology}, 2nd ed., Springer-Verlag, New York, 1978; Dover reprint, 1995. The $\pi$-Base Community, S.~Clontz, and J.~Dabbs, $\pi$-Base, a community database of topological counterexamples, \url{https://topology.pi-base.org/}, data at \url{https://github.com/pi-base/data}, licensed CC BY 4.0. The Manifold Atlas, \texttt{map.mpim-bonn.mpg.de}. KnotInfo, \texttt{knotinfo.math.indiana.edu}.
\end{document}
"""

body = []
for c in CATS:
    body.append(rf"\chapter{{{c}}}")
    body += [entry(s) for s in SPACES if s["cat"] == c]
open("zoo.tex", "w").write(pre + "\n".join(body) + "\n" + apps_chapter() + post)
print("ok")
