from data1 import D1
from data2 import D2
from data3 import D3
from data4 import D4
SPACES = D1 + D2 + D3 + D4
CATS = []
for s in SPACES:
    if s["cat"] not in CATS: CATS.append(s["cat"])
PN = ["compact","connected","path-connected","Hausdorff","manifold","orientable","simply connected","contractible"]
