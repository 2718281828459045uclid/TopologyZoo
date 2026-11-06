# Topology Zoo

AI-driven experiment to motivate topology students.

A reference of 50 topological spaces with point-set properties, fundamental groups, homology, Euler characteristics, derivations, and an applications chapter. It is built from one Python data source into two outputs: a web page and a LaTeX book.

## Files

- `data1.py` … `data4.py`: the spaces, and `data.py` combines them into `SPACES`, `CATS`, `PN`. Each space has `id`, `n` (name), `sym`, `cat`, `d`, `p` (8 properties: compact, connected, path-connected, Hausdorff, manifold, orientable, simply connected, contractible; 1/0/"b"/None/string), `pi`, `H`, `chi`, `how`, `why`, `ps` (point-set derivations), `alg` (algebraic derivations).
- `apps.py`: `APPS` and `FIELDS` for the applications chapter. Each application has `id`, `field`, `title`, `spaces` (zoo ids), `inv`, `text`, `refs`, and an optional `fig`.
- `cites.py`: `PIBASE` (zoo id to π-Base space ids, with links) and `STEEN` (zoo id to example number and page in Steen and Seebach, Dover 1995 reprint). Both builders read it to print a Sources line in each entry. A space missing from both dictionaries is marked as not listed in either source.
- `Counterexamples in Topology.pdf`: the reference copy of Steen and Seebach used for the example numbers and pages.
- `figs.py`: matplotlib line-art figures in black ink, written to `figs/<id>.svg` (for the site) and `figs/<id>.pdf` (for the book). Run `python3 figs.py` to make all of them or `python3 figs.py torus klein` to make some.
- `build_html.py`: writes `topology-zoo.html`, a page body with no doctype, in the published Artifact format. The page loads each figure as `figs/<id>.svg` instead of inlining it, so a publish must include the `figs/*.svg` files alongside the page. Inlined figures made the page 1.7 MB, and Safari in the claude.ai viewer did not load its end. MathJax 3.2.2 comes from jsDelivr, and the font is Old Standard TT.
- `build_tex.py`: writes `zoo.tex`. Compile it with `latexmk -pdf zoo.tex` to get `zoo.pdf`.

## Conventions

- All text fields are LaTeX-compatible. Math goes in `$...$`. Avoid `&`, `%` and `#` in prose, because they break pdflatex.
- The site defers MathJax inside `<details>` (class `mj-defer`) and typesets it when a drop-down opens.
- The design is a 1960s textbook: black on white with no shading.

## Rebuild

The builders use backslashes inside f-strings, which requires Python 3.12 or later (`/opt/homebrew/bin/python3.12` on this machine).

```
python3 figs.py && python3 build_html.py && python3 build_tex.py && latexmk -pdf zoo.tex
```


## Unverified items

- The Budney–Sethares entry in `apps.py` was written without access to the paper.
- The solenoid-and-metre remark is a modeling observation.
- References not confirmed by search should be checked.
