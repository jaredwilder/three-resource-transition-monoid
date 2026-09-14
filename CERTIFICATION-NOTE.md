# Certification note

The historical `HumuFinisher` Lean port and the exact computational census are different authority layers.

## What the old Lean files established

The formal source contains the summary composition structure and several elementary quotient/monoid lemmas. But the class counts `3536` and `417874` were introduced as constants. Lean therefore checked statements about those constants; it did **not** perform the monoid enumeration.

The historical kernel audit correctly identified this gap and required a certificate establishing reachability, distinctness, generator closure, and inclusion of the identity/generators before treating the census as kernel-certified.

## What this repository now establishes independently

`verify_monoid.py` removes the count from the trusted input. It hard-codes only the six single-event summaries for the three-resource system and closes them under the declared summary composition law.

The resulting generated set contains exactly **3,536 pairwise distinct semantic summaries**. Breadth-first generation gives the exact shortest-word histogram

`1, 6, 36, 145, 432, 876, 1088, 776, 176`

at depths `0..8`.

This is an ordinary exact computation, not a Lean kernel theorem. It does, however, independently reproduce the headline census rather than merely asserting it.

## Recovered catalog

The Library also contains `MONOID-CATALOG.json` (715,927 bytes, SHA-256 `db97435513af7880efa2e9f04c461b24cd5893797a623d9ff888a204ad6aad7b`). It stores all 3,536 summaries, shortest representatives, and the six generator transitions for every catalog state. Independent inspection confirmed:

- 3,536/3,536 summaries are pairwise distinct;
- every transition target stays in the catalog;
- all 3,536 states are reachable from the identity;
- all stored representative lengths equal BFS shortest depths;
- recomposing each catalog summary with each one-event generator agrees with all 21,216 stored transition edges.

The focused verifier is intentionally stronger as a reproduction artifact: it regenerates the same monoid without trusting the 715 KB catalog.
