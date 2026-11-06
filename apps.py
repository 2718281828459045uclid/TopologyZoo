# Applications chapter. Text is LaTeX-compatible; math in $...$.
# Each: id, field, title, spaces (zoo ids), inv (math), text, refs [(text, url or None)], fig (optional figure id)
FIELDS = ["Physics", "Data, images, and the brain", "Music theory", "Engineering and computation", "Economics and everyday life"]

APPS = [
# ---------------- Physics
dict(id="app-spin", field="Physics", title="Spin one-half and the belt trick",
 spaces=["so3", "sphere"], inv=r"\pi_1(SO(3))=\mathbb{Z}/2",
 text="Quantum states only need to be defined up to a phase, so a rotation can act on a state through the universal cover $SU(2)\\cong S^3$ instead of through $SO(3)$ itself. Because $\\pi_1(SO(3))$ has order two, there are exactly two possibilities: a rotation by $2\\pi$ acts as $+1$ (integer spin) or as $-1$ (half-integer spin). Electrons, protons, and neutrons are of the second kind. The sign change was observed directly in 1975 by sending neutrons through an interferometer, rotating the spin on one arm by $2\\pi$, and watching the interference pattern invert; a rotation by $4\\pi$ restores it. The belt trick is the same fact for a physical belt: a $2\\pi$ twist cannot be undone without rotating the buckle, a $4\\pi$ twist can.",
 refs=[("H. Rauch et al., Verification of coherent spinor rotation of fermions, Physics Letters A 54 (1975) 425.", None),
       ("S. A. Werner et al., Observation of the phase shift of a neutron due to precession in a magnetic field, Phys. Rev. Lett. 35 (1975) 1053.", None)]),

dict(id="app-ab", field="Physics", title="The Aharonov–Bohm effect",
 spaces=["rose", "annulus", "circle"], inv=r"\pi_1(\mathbb{R}^2\setminus\{0\})=\mathbb{Z}",
 text="A long shielded solenoid confines its magnetic field to a thin tube, so electrons moving around it travel through a region where the field is zero. That region is the plane minus a disk, which deformation retracts onto a circle. Each path an electron can take has a winding number around the solenoid, and the quantum phase it picks up is $e^{iq\\Phi n/\\hbar}$, where $\\Phi$ is the enclosed flux and $n$ the winding number. Two beams passing on opposite sides differ by one winding, so their interference pattern shifts with $\\Phi$ even though no force acts on either beam. The effect is measurable precisely because the field-free region is not simply connected: in a simply connected region, a field-free potential could be gauged away entirely.",
 refs=[("Y. Aharonov and D. Bohm, Significance of electromagnetic potentials in the quantum theory, Phys. Rev. 115 (1959) 485.", None)], fig="app_ab"),

dict(id="app-anyons", field="Physics", title="Anyons and braid statistics",
 spaces=["conf", "graph"], inv=r"\pi_1(\mathrm{UConf}_n(\mathbb{C}))=B_n",
 text="The configuration space of $n$ identical particles is the space of unordered $n$-point subsets. Exchanging particles traces a loop in it, and the quantum state picks up a phase determined by a one-dimensional representation of its fundamental group. In three dimensions the diagonals have codimension three, the fundamental group is the symmetric group $S_n$, and the only one-dimensional representations give bosons ($+1$) and fermions ($-1$). In the plane the fundamental group is the braid group $B_n$, whose abelianization is $\\mathbb{Z}$, so any phase $e^{i\\theta}$ can occur. These intermediate particles, anyons, describe excitations of fractional quantum Hall systems, and non-abelian versions are the basis of proposals for topological quantum computing.",
 refs=[("J. M. Leinaas and J. Myrheim, On the theory of identical particles, Il Nuovo Cimento B 37 (1977) 1.", None),
       ("F. Wilczek, Quantum mechanics of fractional-spin particles, Phys. Rev. Lett. 49 (1982) 957.", None)]),

dict(id="app-defects", field="Physics", title="Topological defects in ordered media",
 spaces=["circle", "rp2", "sphere"], inv=r"\pi_1(S^1)=\mathbb{Z},\ \ \pi_1(\mathbb{RP}^2)=\mathbb{Z}/2,\ \ \pi_2(S^2)=\mathbb{Z}",
 text="An ordered medium assigns to each point a value in an order parameter space $M$. Around a line defect the order parameter traces a loop in $M$, so line defects are classified by $\\pi_1(M)$, and point defects in three dimensions by $\\pi_2(M)$. In superfluid helium the order parameter is a phase in $S^1$, and $\\pi_1=\\mathbb{Z}$ means vortices carry an integer winding number. In a nematic liquid crystal the molecules are rods with no head or tail, so the order parameter is a line through the origin, a point of $\\mathbb{RP}^2$. Since $\\pi_1(\\mathbb{RP}^2)=\\mathbb{Z}/2$, there is exactly one kind of stable line defect, the half-integer disclination, and two of them can annihilate. Point defects (hedgehogs) are classified by $\\pi_2(\\mathbb{RP}^2)=\\mathbb{Z}$.",
 refs=[("N. D. Mermin, The topological theory of defects in ordered media, Rev. Mod. Phys. 51 (1979) 591.", None)], fig="app_nematic"),

dict(id="app-monopole", field="Physics", title="The Dirac monopole and charge quantization",
 spaces=["sphere", "cpn", "un"], inv=r"\pi_1(U(1))=\mathbb{Z}",
 text="A magnetic monopole would have a field on the sphere surrounding it that cannot be written with a single vector potential. Instead one uses two potentials on the northern and southern hemispheres, related on the equator by a gauge transformation $S^1\\to U(1)$. For the electron's wavefunction to be single-valued, this transition function must be a closed loop in $U(1)$, which has a winding number in $\\pi_1(U(1))=\\mathbb{Z}$. The result is Dirac's condition that electric charge times magnetic charge is an integer multiple of a fixed constant. Geometrically, the monopole is a circle bundle over $S^2$, and the one with winding number one is the Hopf fibration $S^3\\to S^2=\\mathbb{CP}^1$.",
 refs=[("P. A. M. Dirac, Quantised singularities in the electromagnetic field, Proc. Roy. Soc. A 133 (1931) 60.", None)]),

dict(id="app-instanton", field="Physics", title="Instantons and the vacuum of gauge theory",
 spaces=["sphere", "un", "so3"], inv=r"\pi_3(SU(2))=\pi_3(S^3)=\mathbb{Z}",
 text="In Euclidean $SU(2)$ Yang–Mills theory, a finite-action field must approach a pure gauge at infinity. The sphere at infinity in $\\mathbb{R}^4$ is $S^3$, so the boundary data is a map $S^3\\to SU(2)\\cong S^3$, which has an integer degree. This degree is the instanton number. Configurations with different degrees cannot be deformed into each other, which splits the vacuum into sectors labeled by integers and leads to the $\\theta$-parameter of QCD. The same group $\\pi_3(S^3)=\\mathbb{Z}$ appears in the sphere entry as the statement that $\\pi_n(S^n)=\\mathbb{Z}$.",
 refs=[("A. A. Belavin, A. M. Polyakov, A. S. Schwartz, Yu. S. Tyupkin, Pseudoparticle solutions of the Yang–Mills equations, Phys. Lett. B 59 (1975) 85.", None)]),

dict(id="app-hall", field="Physics", title="The quantum Hall effect and Chern numbers",
 spaces=["torus", "ntorus", "cpn"], inv=r"c_1\in H^2(T^2;\mathbb{Z})=\mathbb{Z}",
 text="Electron momenta in a two-dimensional crystal are periodic in both directions, so the space of momenta, the Brillouin zone, is a torus $T^2$. Each filled energy band gives a line bundle over this torus, a map $T^2\\to\\mathbb{CP}^\\infty$ up to homotopy, and such a bundle has an integer invariant, the first Chern number. Thouless, Kohmoto, Nightingale, and den Nijs showed that the Hall conductance equals $e^2/h$ times the sum of these integers. This explains why the measured conductance sits on plateaus at exact integer multiples, to parts per billion, regardless of impurities in the sample. Topological insulators extend the same idea to other classes of bundles.",
 refs=[("D. J. Thouless, M. Kohmoto, M. P. Nightingale, M. den Nijs, Quantized Hall conductance in a two-dimensional periodic potential, Phys. Rev. Lett. 49 (1982) 405.", None)]),

dict(id="app-bloch", field="Physics", title="Qubits, the Bloch sphere, and geometric phase",
 spaces=["cpn", "sphere"], inv=r"\{\text{pure states of }\mathbb{C}^n\}=\mathbb{CP}^{n-1}",
 text="A quantum state is a unit vector up to a phase, so the pure states of an $n$-level system form $\\mathbb{CP}^{n-1}$. For a qubit this is $\\mathbb{CP}^1\\cong S^2$, the Bloch sphere used throughout quantum computing. When a spin-one-half system is carried slowly around a closed loop on this sphere, it returns with an extra phase equal to minus half the solid angle the loop encloses. This geometric (Berry) phase depends only on the path in $\\mathbb{CP}^1$, not on how fast it is traversed, and it is the holonomy of the Hopf bundle $S^3\\to S^2$.",
 refs=[("M. V. Berry, Quantal phase factors accompanying adiabatic changes, Proc. Roy. Soc. A 392 (1984) 45.", None)]),

dict(id="app-toric", field="Physics", title="The toric code",
 spaces=["torus", "genusg"], inv=r"H_1(\Sigma_g;\mathbb{Z}/2)=(\mathbb{Z}/2)^{2g}",
 text="Kitaev's toric code places qubits on the edges of a square lattice drawn on a torus. Its ground states are labeled by $H_1(T^2;\\mathbb{Z}/2)=(\\mathbb{Z}/2)^2$, so there are four of them, and they store two logical qubits. A logical operation is a string of flips along a loop that wraps the torus; a contractible loop does nothing. Local noise produces short strings that bound small regions, which can be detected and corrected, while changing the stored information requires an error chain that wraps all the way around. On a surface of genus $g$ the code stores $2g$ qubits. This homological idea underlies the surface codes used in current quantum error-correction experiments.",
 refs=[("A. Yu. Kitaev, Fault-tolerant quantum computation by anyons, Annals of Physics 303 (2003) 2.", None)], fig="app_toric"),

dict(id="app-cosmic", field="Physics", title="The shape of the universe",
 spaces=["poincare", "ntorus", "lens"], inv=r"\pi_1\ \text{finite}\Rightarrow\text{multiple images}",
 text="General relativity fixes the local geometry of space but not its global topology. If space were a quotient of $S^3$ or $\\mathbb{R}^3$ by a group of isometries, light could reach us along several paths, and the cosmic microwave background would contain pairs of matching circles. In 2003 Luminet and collaborators proposed that space is the Poincaré homology sphere, a dodecahedron with opposite faces glued, to explain the unusually weak large-angle correlations seen by WMAP. Later searches for matching circles, including with Planck data, found no such signal, and the proposal is now disfavored. The example shows how a quotient $S^3/\\pi_1$ makes a concrete, testable prediction.",
 refs=[("J.-P. Luminet, J. R. Weeks, A. Riazuelo, R. Lehoucq, J.-P. Uzan, Dodecahedral space topology as an explanation for weak wide-angle temperature correlations in the cosmic microwave background, Nature 425 (2003) 593.", "https://arxiv.org/abs/astro-ph/0310253")]),

dict(id="app-chaos", field="Physics", title="Chaotic dynamics: the horseshoe and the solenoid",
 spaces=["cantor", "solenoid", "annulus"], inv=r"\Lambda\cong\{0,1\}^{\mathbb{Z}}",
 text="Smale's horseshoe stretches a square, folds it, and lays it back over itself. The points that stay in the square forever form a Cantor set, and on it the map is the shift on two-sided sequences of $0$s and $1$s, so the dynamics contains periodic orbits of every period and orbits that are dense. The solenoid arises the same way from a solid torus: stretch it to twice its length, thin it, and wrap it twice around inside itself. The intersection of all the images is the dyadic solenoid, a compact attractor that is locally a Cantor set times an interval. Both spaces enter dynamics as invariant sets that a computer simulation shows only as a blur.",
 refs=[("S. Smale, Differentiable dynamical systems, Bull. Amer. Math. Soc. 73 (1967) 747.", None)]),

# ---------------- Data
dict(id="app-klein", field="Data, images, and the brain", title="A Klein bottle in natural images",
 spaces=["klein", "circle"], inv=r"H_*(\,\cdot\,;\mathbb{Z}/2)\ \text{of a point cloud}",
 text="Carlsson, Ishkhanov, de Silva, and Zomorodian took millions of $3\\times3$ pixel patches from photographs, kept the high-contrast ones, and normalized them to points on a 7-sphere. Persistent homology of the densest region showed a circle: patches that look like an edge at some angle. A larger region showed a space with the mod 2 homology of a Klein bottle, which they explained by a model in which each patch is a linear or quadratic profile in some direction. The direction gives one circle and the profile's position gives another, and the identifications between them are those of the Klein bottle. The model has since been used to build features for image analysis.",
 refs=[("G. Carlsson, T. Ishkhanov, V. de Silva, A. Zomorodian, On the local behavior of spaces of natural images, Int. J. Computer Vision 76 (2008) 1.", "https://link.springer.com/article/10.1007/s11263-007-0056-x")]),

dict(id="app-grid", field="Data, images, and the brain", title="Grid cells live on a torus",
 spaces=["torus", "circle"], inv=r"H_1(T^2)=\mathbb{Z}^2,\ H_2(T^2)=\mathbb{Z}",
 text="Grid cells in the entorhinal cortex fire when an animal is at the vertices of a triangular lattice in its environment. A network of such cells encodes position modulo that lattice, which predicts that the joint activity of a module should lie on a torus. Gardner and collaborators recorded hundreds of grid cells in rats and applied persistent homology to the population activity. They found one component, two independent 1-dimensional loops, and one 2-dimensional class, the Betti numbers $1,2,1$ of $T^2$, and the torus persisted during sleep. Head-direction cells, which encode the direction an animal faces, give a circle in the same way.",
 refs=[("R. J. Gardner et al., Toroidal topology of population activity in grid cells, Nature 602 (2022) 123.", None),
       ("R. Chaudhuri et al., The intrinsic attractor manifold and population dynamics of a canonical cognitive circuit across waking and sleep, Nature Neuroscience 22 (2019) 1512.", None)]),

dict(id="app-barcodes", field="Data, images, and the brain", title="Persistent homology and barcodes",
 spaces=["graph", "circle", "sphere"], inv=r"H_k(X_\varepsilon)\ \text{as }\varepsilon\ \text{grows}",
 text="A finite set of data points has no interesting topology by itself. Persistent homology connects points closer than $\\varepsilon$, fills in simplices, and tracks how the homology of the resulting complex changes as $\\varepsilon$ grows. Classes that persist over a long range of $\\varepsilon$ are read as features of the shape the data was sampled from; short-lived ones as noise. The output is a barcode, one bar per class. A long bar in degree $1$ says the data loops around, as in the circle entry; a long bar in degree $2$ says it encloses a void, as in the sphere entry. The graph entry is the case $\\varepsilon$ small: a graph's $H_1$ counts its independent cycles.",
 refs=[("G. Carlsson, Topology and data, Bull. Amer. Math. Soc. 46 (2009) 255.", None),
       ("R. Ghrist, Barcodes: the persistent topology of data, Bull. Amer. Math. Soc. 45 (2008) 61.", None)]),

dict(id="app-coverage", field="Data, images, and the brain", title="Coverage in sensor networks",
 spaces=["disk", "sphere", "graph"], inv=r"H_2(R,F)\ne0",
 text="Scatter sensors over a region; each can detect nearby intruders and can tell which other sensors are within range, but none knows its coordinates. De Silva and Ghrist showed that the communication graph alone can certify coverage. From it one builds a simplicial complex $R$ and a subcomplex $F$ along the fence at the boundary. If a certain relative homology class in $H_2(R,F)$ is nonzero, the sensing disks cover the whole region with no holes. The argument is the disk entry in disguise: a hole would let the boundary circle retract off the disk, which the homology class forbids.",
 refs=[("V. de Silva and R. Ghrist, Coverage in sensor networks via persistent homology, Algebraic and Geometric Topology 7 (2007) 339.", None)]),

dict(id="app-circular", field="Data, images, and the brain", title="Circular coordinates for periodic data",
 spaces=["circle", "rpinf", "cpinf"], inv=r"[X,S^1]\cong H^1(X;\mathbb{Z})",
 text="Since $S^1$ is a $K(\\mathbb{Z},1)$, homotopy classes of maps from a space to the circle correspond to classes in $H^1(X;\\mathbb{Z})$. De Silva, Morozov, and Vejdemo-Johansson turned this into an algorithm: find a persistent integer cohomology class in a point cloud, then compute a smoothest representative and read it as an angle-valued coordinate. The result assigns each data point a phase. It applies to any data governed by a cyclic parameter, such as a phase of a biological cycle or a position in a repeated rhythmic pattern. The same principle with $\\mathbb{RP}^\\infty$ and $\\mathbb{CP}^\\infty$ gives coordinates for other cohomology classes.",
 refs=[("V. de Silva, D. Morozov, M. Vejdemo-Johansson, Persistent cohomology and circular coordinates, Discrete Comput. Geom. 45 (2011) 737.", None)]),

# ---------------- Music
dict(id="app-pitchclass", field="Music theory", title="Octave equivalence and the pitch-class circle",
 spaces=["circle"], inv=r"\mathbb{R}/12\mathbb{Z}\cong S^1",
 text="Measure pitch in semitones on the real line. Treating pitches an octave apart as the same note identifies $x$ with $x+12$, and the quotient $\\mathbb{R}/12\\mathbb{Z}$ is a circle. Transposition is rotation and inversion is reflection, so the symmetries of pitch-class space form the dihedral group of the circle. The covering map $\\mathbb{R}\\to S^1$ is audible: a Shepard tone rises step by step and returns to its starting note, tracing a loop of degree one in pitch-class space whose lift in pitch never closes.",
 refs=[("R. N. Shepard, Circularity in judgments of relative pitch, J. Acoust. Soc. Am. 36 (1964) 2346.", None)]),

dict(id="app-dyads", field="Music theory", title="Two-note chords on a Möbius band",
 spaces=["mobius", "torus"], inv=r"T^2/S_2\cong\text{Möbius band}",
 text="An ordered pair of pitch classes is a point of $T^2=S^1\\times S^1$. A two-note chord forgets the order, so the space of dyads is $T^2/S_2$, the quotient by swapping coordinates. Tymoczko observed that this quotient is a Möbius band. Its boundary is the fixed set of the swap, the unisons; the tritones, which divide the octave evenly, lie on the central circle. A voice leading from one dyad to another is a path, and its size is the length of the path. Moving across the band and out the side brings you back with the voices exchanged, which is the half-twist.",
 refs=[("D. Tymoczko, The geometry of musical chords, Science 313 (2006) 72.", None)], fig="app_dyads"),

dict(id="app-orbifold", field="Music theory", title="Chord spaces as orbifolds",
 spaces=["ntorus", "mobius"], inv=r"T^n/S_n",
 text="For $n$-note chords, ordered pitch-class tuples form $T^n$ and unordered chords form the orbifold $T^n/S_n$. For three notes this is a triangular prism whose two ends are glued with a third of a turn. The augmented triad, which divides the octave into three equal parts, lies on the central axis; major and minor triads lie close to it, and chords with repeated notes lie on the mirror boundary. Efficient voice leading is motion along short paths, and chords near the center can reach many other chords by short paths. This gives a geometric reason that nearly even chords such as triads and seventh chords support smooth voice leading. Callender, Quinn, and Tymoczko extended the picture to a family of quotient spaces obtained by imposing octave, permutation, transposition, inversion, and cardinality equivalences.",
 refs=[("D. Tymoczko, The geometry of musical chords, Science 313 (2006) 72.", None),
       ("C. Callender, I. Quinn, D. Tymoczko, Generalized voice-leading spaces, Science 320 (2008) 346.", None),
       ("D. Tymoczko, A Geometry of Music, Oxford University Press, 2011.", None)]),

dict(id="app-tonnetz", field="Music theory", title="The Tonnetz is a torus",
 spaces=["torus"], inv=r"\mathbb{Z}^2/\Lambda\ \text{with}\ \Lambda\ \text{of index }12",
 text="Euler's Tonnetz arranges notes in a plane so that one direction moves by perfect fifths and another by major thirds; the third direction then moves by minor thirds. Major and minor triads are the triangles. In twelve-tone equal temperament, three major thirds return to the starting note and so do twelve fifths, so the plane is periodic in two independent directions and wraps into a torus. Neo-Riemannian theory studies the three operations that flip a triangle across one of its edges, keeping two notes and moving the third by a step. These flips generate chord progressions that move around the torus, common in late Romantic music and in film scores.",
 refs=[("R. Cohn, Introduction to neo-Riemannian theory: a survey and a historical perspective, Journal of Music Theory 42 (1998) 167.", None)], fig="app_tonnetz"),

dict(id="app-rhythm", field="Music theory", title="Meter, polyrhythm, and phasing",
 spaces=["circle", "torus", "solenoid"], inv=r"\text{lines of slope } p/q \text{ on } T^2",
 text="Cyclic meter puts time on a circle: a position in a bar is a point of $\\mathbb{R}/\\mathbb{Z}$. Two simultaneous cycles put time on a torus, and a $3{:}2$ polyrhythm is the closed line of slope $3/2$, with onsets where it crosses the edges of the square. If the two tempos drift apart slowly, as in Steve Reich's phasing pieces, the slope changes and the line moves across the torus; an irrational ratio of tempos would give a line that never closes and passes arbitrarily near every point. Iterated duple grouping (beat, bar, two-bar unit, four-bar unit) is a tower of circles each covering the next twice. The inverse limit of such a tower is the dyadic solenoid, with musical time running along a single path component. This last point is a modeling observation rather than an established result.",
 refs=[("S. Reich, Piano Phase (1967).", None)], fig="app_poly"),

dict(id="app-musicdata", field="Music theory", title="Topological analysis of recorded music",
 spaces=["torus", "circle"], inv=r"\text{persistent }H_1",
 text="Budney and Sethares applied persistent homology to features computed from recordings. Periodic structure in the sound shows up as persistent classes in degree one. In general, data governed by one cyclic parameter samples a circle, and data governed by two independent cyclic parameters samples a torus. The paper was among the most read in the Journal of Mathematics and Music, and it is a natural entry point for applying the data-analysis methods above to sound.",
 refs=[("R. Budney and W. Sethares, Topology of musical data, Journal of Mathematics and Music 8 (2014).", "https://arxiv.org/abs/1307.1201")]),

# ---------------- Engineering
dict(id="app-robots", field="Engineering and computation", title="Robot arms and motion planning",
 spaces=["ntorus", "conf", "graph"], inv=r"\text{continuous planner exists}\iff X\ \text{contractible}",
 text="A robot arm with $n$ rotating joints has configuration space $T^n$, one angle per joint. A motion planner is a rule that takes a start and an end configuration and returns a path between them. Farber showed that a planner depending continuously on its input exists only if the configuration space is contractible. Since $T^n$ is not, every planner for a jointed arm has discontinuities, and the minimal number of continuous pieces needed, the topological complexity, is a homotopy invariant. Configuration spaces of several robots moving on a network of tracks are configuration spaces of graphs, whose fundamental groups are braid groups of graphs.",
 refs=[("M. Farber, Topological complexity of motion planning, Discrete Comput. Geom. 29 (2003) 211.", None),
       ("R. Ghrist, Configuration spaces and braid groups on graphs in robotics, AMS/IP Stud. Adv. Math. 24 (2001) 29.", None)]),

dict(id="app-attitude", field="Engineering and computation", title="Orientations, gimbal lock, and quaternions",
 spaces=["so3", "sphere"], inv=r"SO(3)\cong\mathbb{RP}^3",
 text="The orientation of a rigid body is a point of $SO(3)$, a compact 3-manifold. A compact 3-manifold cannot be covered by a single chart, so any description by three numbers, such as Euler angles, must break down somewhere; the breakdown is called gimbal lock. Stuelpnagel proved that no three-parameter representation is both global and nonsingular. Spacecraft attitude control and computer graphics therefore use unit quaternions, points of the double cover $S^3$, with $q$ and $-q$ representing the same rotation.",
 refs=[("J. Stuelpnagel, On the parametrization of the three-dimensional rotation group, SIAM Review 6 (1964) 422.", None)]),

dict(id="app-kirchhoff", field="Engineering and computation", title="Kirchhoff's laws and the cycle space of a circuit",
 spaces=["graph", "rose"], inv=r"\operatorname{rank}H_1(\Gamma)=E-V+1",
 text="An electrical network is a graph. Kirchhoff's voltage law requires one equation for each independent loop, and Kirchhoff showed that the number needed is $E-V+1$, which is the rank of $H_1$ of the graph. A spanning tree, the tool used in the graph entry to compute the fundamental group, picks out the independent loops: each edge outside the tree closes exactly one. This 1847 argument is among the earliest uses of what became homology.",
 refs=[("G. Kirchhoff, Über die Auflösung der Gleichungen, auf welche man bei der Untersuchung der linearen Vertheilung galvanischer Ströme geführt wird, Annalen der Physik 72 (1847) 497.", None)]),

dict(id="app-observable", field="Engineering and computation", title="Observable properties and the Sierpiński space",
 spaces=["sierpinski", "cofinite"], inv=r"\{\text{open sets of }X\}\leftrightarrow C(X,\mathbb{S})",
 text="In the semantics of programming languages, an open set is read as a property that can be confirmed by a finite amount of observation: a program halts, a stream contains a 1. Such properties can be verified but not always refuted, which is the asymmetry of the Sierpiński space, where $1$ is open and $0$ is not. A property of a space of computations is observable exactly when it is a continuous map to the Sierpiński space. The resulting topologies are $T_0$ but rarely $T_1$, so the non-Hausdorff entries of this zoo are the normal case in domain theory.",
 refs=[("S. Vickers, Topology via Logic, Cambridge University Press, 1989.", None),
       ("M. B. Smyth, Power domains and predicate transformers: a topological view, ICALP 1983, LNCS 154.", None)]),

dict(id="app-digital", field="Engineering and computation", title="Digital topology and finite spaces",
 spaces=["pseudocircle", "sierpinski"], inv=r"|K(X)|\to X\ \text{weak equivalence}",
 text="A digital image is a finite grid of pixels, and the question of which pixels form a connected region, or whether a closed curve of pixels separates the plane, depends on how neighbors are defined. Khalimsky, Kopperman, and Meyer gave the grid a finite $T_0$ topology in which pixels alternate between open and closed points, as in the pseudocircle, and in which a digital Jordan curve theorem holds. McCord's theorem, used in the pseudocircle entry, guarantees that such finite spaces can model the homotopy type of any finite simplicial complex.",
 refs=[("E. Khalimsky, R. Kopperman, P. R. Meyer, Computer graphics and connected topologies on finite ordered sets, Topology and its Applications 36 (1990) 1.", None),
       ("M. C. McCord, Singular homology groups and homotopy groups of finite topological spaces, Duke Math. J. 33 (1966) 465.", None)]),

dict(id="app-zariski", field="Engineering and computation", title="The Zariski topology of a curve",
 spaces=["cofinite"], inv=r"\text{closed sets}=\text{finite sets}",
 text="In algebraic geometry, the closed subsets of an irreducible algebraic curve are the zero sets of polynomials, which are the finite sets and the whole curve. So the Zariski topology on the points of a curve is the cofinite topology. It is compact and $T_1$ but not Hausdorff, exactly as in the countable cofinite entry, which is the curve's topology when its points are countable, as for a curve over the algebraic numbers. Much of the machinery of algebraic geometry, including sheaf cohomology, was built to do useful topology on spaces this coarse.",
 refs=[("R. Hartshorne, Algebraic Geometry, Springer, 1977, Chapter I.", None)]),

# ---------------- Economics
dict(id="app-nash", field="Economics and everyday life", title="Nash equilibrium",
 spaces=["disk"], inv=r"f:D^n\to D^n\ \Rightarrow\ \exists\,x=f(x)",
 text="In a finite game, a mixed strategy for each player is a probability vector, and the set of all strategy profiles is a product of simplices, homeomorphic to a closed disk. Nash defined a continuous map on this disk that moves each player's strategy toward better responses. Its fixed points are exactly the profiles where no player gains by changing strategy alone. Brouwer's theorem, proved in the disk entry with $H_{n-1}$, guarantees a fixed point, so every finite game has an equilibrium. The proof gives no way to find it, and computing Nash equilibria is believed to be hard in general.",
 refs=[("J. Nash, Non-cooperative games, Annals of Mathematics 54 (1951) 286.", None)]),

dict(id="app-hairy", field="Economics and everyday life", title="The hairy ball theorem and the wind",
 spaces=["sphere", "torus"], inv=r"\chi(S^2)=2\ne0",
 text="A continuous tangent vector field on a closed surface has zeros whose indices add up to the Euler characteristic. Since $\\chi(S^2)=2$, every continuous tangent field on a sphere vanishes somewhere. For an idealized continuous horizontal wind on the Earth's surface, there is always a point where the horizontal wind is zero, such as the eye of a cyclone. A torus has $\\chi=0$ and carries nowhere-zero fields, which is one reason the torus entry and the sphere entry behave so differently.",
 refs=[("J. Milnor, Topology from the Differentiable Viewpoint, 1965, Chapter 6.", None)]),

dict(id="app-borsuk", field="Economics and everyday life", title="Borsuk–Ulam: antipodes and fair division",
 spaces=["sphere", "rpn"], inv=r"f:S^n\to\mathbb{R}^n\ \Rightarrow\ \exists\,x:\ f(x)=f(-x)",
 text="The Borsuk–Ulam theorem says every continuous map $S^n\\to\\mathbb{R}^n$ sends some pair of antipodal points to the same value. With $n=2$: at any moment there are two antipodal points on the Earth with the same temperature and the same pressure. The proof passes to $\\mathbb{RP}^n=S^n/\\pm1$ and uses its mod 2 cohomology. The same theorem gives the ham sandwich theorem, that one plane cut can bisect three solids at once, and the necklace splitting theorem, that two thieves can fairly divide a necklace with $k$ kinds of beads using at most $k$ cuts.",
 refs=[("N. Alon, Splitting necklaces, Advances in Mathematics 63 (1987) 247.", None),
       ("J. Matoušek, Using the Borsuk–Ulam Theorem, Springer, 2003.", None)]),
]
