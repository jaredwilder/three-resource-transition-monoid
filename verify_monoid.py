#!/usr/bin/env python3
"""Regenerate the three-resource transition monoid from its six generators.

This does not trust the historical class-count constants or the recovered transition
catalog. The only inputs are the six one-event semantic summaries.
"""
from collections import Counter, deque
from math import ceil, log2

EVENTS = ["open0", "close0", "open1", "close1", "open2", "close2"]

# A summary is (final_states, deltas).  For each of the 9 semantic states,
# final_states[i] is the output state and deltas[i] is a Z^3 additive change.
GENERATOR_DATA = [
    ([1,8,3,8,5,8,7,8,8], [[1,0,0],[0,0,0],[1,0,0],[0,0,0],[1,0,0],[0,0,0],[1,0,0],[0,0,0],[0,0,0]]),
    ([8,0,8,2,8,4,8,6,8], [[0,0,0],[-1,0,0],[0,0,0],[-1,0,0],[0,0,0],[-1,0,0],[0,0,0],[-1,0,0],[0,0,0]]),
    ([2,3,8,8,6,7,8,8,8], [[0,1,0],[0,1,0],[0,0,0],[0,0,0],[0,1,0],[0,1,0],[0,0,0],[0,0,0],[0,0,0]]),
    ([8,8,0,1,8,8,4,5,8], [[0,0,0],[0,0,0],[0,-1,0],[0,-1,0],[0,0,0],[0,0,0],[0,-1,0],[0,-1,0],[0,0,0]]),
    ([4,5,6,7,8,8,8,8,8], [[0,0,1],[0,0,1],[0,0,1],[0,0,1],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]),
    ([8,8,8,8,0,1,2,3,8], [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,-1],[0,0,-1],[0,0,-1],[0,0,-1],[0,0,0]]),
]

EXPECTED_HISTOGRAM = {0:1, 1:6, 2:36, 3:145, 4:432, 5:876, 6:1088, 7:776, 8:176}
EXPECTED_SIZE = 3536


def canonical(final_states, deltas):
    return tuple(final_states), tuple(tuple(v) for v in deltas)


def compose(a, b):
    """Apply summary a, then b."""
    af, ad = a
    bf, bd = b
    finals = []
    deltas = []
    for i in range(9):
        mid = af[i]
        finals.append(bf[mid])
        deltas.append(tuple(ad[i][j] + bd[mid][j] for j in range(3)))
    return tuple(finals), tuple(deltas)


def main():
    identity = canonical(range(9), [[0,0,0] for _ in range(9)])
    generators = [canonical(fs, ds) for fs, ds in GENERATOR_DATA]

    index = {identity: 0}
    reps = [()]
    depth = [0]
    queue = deque([identity])

    while queue:
        a = queue.popleft()
        i = index[a]
        for event, g in zip(EVENTS, generators):
            c = compose(a, g)
            if c not in index:
                index[c] = len(index)
                reps.append(reps[i] + (event,))
                depth.append(depth[i] + 1)
                queue.append(c)

    hist = dict(sorted(Counter(depth).items()))
    size = len(index)
    radius = max(depth)

    assert size == EXPECTED_SIZE, (size, EXPECTED_SIZE)
    assert hist == EXPECTED_HISTOGRAM, (hist, EXPECTED_HISTOGRAM)
    assert radius == 8
    assert sum(hist.values()) == size
    assert len(set(index)) == size
    assert ceil(log2(size)) == 12

    # Every stored representative actually evaluates back to its summary.
    inv = [None] * size
    for summary, i in index.items():
        inv[i] = summary
    for i, word in enumerate(reps):
        cur = identity
        for event in word:
            cur = compose(cur, generators[EVENTS.index(event)])
        assert cur == inv[i]
        assert len(word) == depth[i]

    print(f"semantic_states=9 generators={len(generators)}")
    print(f"monoid_size={size}")
    print(f"minimal_binary_bits={ceil(log2(size))}")
    print(f"max_shortest_representative_length={radius}")
    print("depth_histogram=" + repr(hist))
    print("distinct_summaries=3536/3536 PASS")
    print("representatives=3536/3536 PASS")
    print("ALL CHECKS PASS")


if __name__ == "__main__":
    main()
