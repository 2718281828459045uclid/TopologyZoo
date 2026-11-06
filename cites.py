# Per-space citations to the pi-Base and to Steen and Seebach, Counterexamples in Topology.
# Read by build_html.py and build_tex.py.
#
# PIBASE: zoo id -> list of (pi-Base id, note). The note is "" when the pi-Base space
#   is the zoo space itself, and names the special case when it covers only part of it.
# STEEN: zoo id -> (example number, page) in the Dover 1995 reprint of the 1978 2nd edition.
#   Example numbers match the counterexamples_id field in the pi-Base data repository;
#   pages come from the book's table of contents.
# Spaces absent from both dictionaries appear in neither source.

PIBASE_URL = "https://topology.pi-base.org/spaces/"

PIBASE = {
    "point": [("S000162", "")],
    "rn": [("S000025", "the case $n=1$"), ("S000176", "the case $n=2$")],
    "circle": [("S000170", "")],
    "sphere": [("S000169", "")],
    "torus": [("S000224", "")],
    "rp2": [("S000168", "")],
    "infwedge": [("S000139", "")],
    "hilbert": [("S000032", "")],
    "hawaii": [("S000201", "")],
    "warsaw": [("S000205", "")],
    "sine": [("S000114", "")],
    "cantor": [("S000026", "")],
    "longline": [("S000038", "")],
    "rationals": [("S000027", "")],
    "sorgenfrey": [("S000043", "")],
    "twoorigins": [("S000083", "")],
    "pseudocircle": [("S000213", "")],
    "sierpinski": [("S000010", "")],
    "cofinite": [("S000015", "")],
}

STEEN = {
    "rn": (28, 56),          # Euclidean Topology (the real line, n = 1)
    "hilbert": (38, 65),     # Hilbert Cube
    "sine": (117, 137),      # Closed Topologist's Sine Curve
    "cantor": (29, 57),      # The Cantor Set
    "longline": (45, 71),    # The Long Line
    "rationals": (30, 59),   # The Rational Numbers
    "sorgenfrey": (51, 75),  # Right Half-Open Interval Topology
    "sierpinski": (11, 44),  # Sierpinski Space
    "cofinite": (18, 49),    # Finite Complement Topology on a Countable Space
}

STEEN_FULL = "L. A. Steen and J. A. Seebach, Jr., Counterexamples in Topology, 2nd ed., Springer-Verlag, New York, 1978; Dover reprint, 1995"
PIBASE_FULL = "The pi-Base Community, S. Clontz, and J. Dabbs, pi-Base: a community database of topological counterexamples, https://topology.pi-base.org/, data licensed CC BY 4.0"
