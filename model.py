"""Exact shortest-common-superstring search over small fragment sets."""

def overlap(left, right):
    for size in range(min(len(left), len(right)), 0, -1):
        if left.endswith(right[:size]):
            return size
    return 0


def assemble(fragments):
    if not isinstance(fragments, list) or not 1 <= len(fragments) <= 12:
        raise ValueError("Supply 1 to 12 fragments.")
    if any(not isinstance(f, str) or not f.strip() or len(f) > 256 for f in fragments):
        raise ValueError("Each fragment needs 1 to 256 characters and some non-whitespace text.")
    unique = sorted(set(fragments))
    parts = [f for f in unique if not any(f != g and f in g for g in unique)]
    suffix = {(i,j): b[overlap(a,b):] for i,a in enumerate(parts) for j,b in enumerate(parts) if i != j}
    # Two distinct witnesses suffice to detect ambiguity. At a fixed state
    # each future step appends the same suffix to every tied witness.
    states = {(1 << i,i): (f,) for i,f in enumerate(parts)}
    full = (1 << len(parts))-1
    for mask in range(1,full+1):
        for i in range(len(parts)):
            paths = states.get((mask,i), ())
            for j in range(len(parts)):
                if not paths or mask & (1 << j):
                    continue
                key = (mask | (1 << j),j)
                candidates = set(states.get(key, ()))
                candidates.update(p + suffix[i,j] for p in paths)
                shortest = min(map(len,candidates))
                states[key] = tuple(sorted(p for p in candidates if len(p)==shortest)[:2])
    finals = {p for i in range(len(parts)) for p in states[full,i]}
    size = min(map(len,finals))
    best = sorted(p for p in finals if len(p)==size)
    return {"text":best[0], "ambiguous":len(best)>1, "locations":[best[0].index(f) for f in fragments]}


def analyze(data):
    return assemble(data["fragments"])
