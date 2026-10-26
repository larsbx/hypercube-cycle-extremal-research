# Exhaustive Q3 edge-deletion envelope

The experiment enumerates all 4,096 spanning edge subsets of Q3. Cycle discovery
uses edge subsets inducing a connected 2-regular selected-edge subgraph, rather
than the vertex DFS or chord oracle of the other programs. It records minimum
and maximum counts at each retained-edge count, cycle length, and coordinate rank.

The full cube has 6 ordinary four-cycles, 16 six-cycles, and 6 eight-cycles.
The minimum four-cycle count is 0 for 0 through 9 retained edges, then 2, 4,
and 6 at 10, 11, and 12 retained edges. These are exhaustive Q3 facts only.

An incidence check independently verifies that the sum of surviving m-cycles
over all single-edge deletions is (12-m) times the full-cube m-cycle count.
The complete support-stratified envelopes are in `conformance/first.json`.
No arbitrary-dimensional inequality, supersaturation theorem, or inference
from a full-product symbol is claimed.
