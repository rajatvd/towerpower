from tqdm import tqdm
from decimal import Decimal, getcontext
from functools import cache

# Set precision (number of significant digits)
getcontext().prec = 50

NUMS = list(range(2, 101))
NUMS = [Decimal(x) for x in NUMS]


twoln = Decimal(2).ln()


def l2(x):
    return x.ln() / twoln


def l(x, base):
    return x.ln() / base.ln()


@cache
def p2rep(tower):
    if len(tower) == 1:
        return (0, tower[0])
    if len(tower) == 2:
        a1 = tower[0]
        a2 = tower[1]

        r = a2 * l2(a1)
        return (1, r)
    if len(tower) == 3:
        a1 = tower[0]
        a2 = tower[1]
        a3 = tower[2]

        r = a3 * l2(a2) + l2(l2(a1))
        return (2, r)

    if len(tower) == 4:
        new_tower = (tower[0], tower[1], tower[2] ** tower[3])
        shouldbe2, p2 = p2rep(new_tower)
        return (3, l2(p2))
    else:
        k, top_rep = p2rep(tower[1:])
        lli = l2(l2(tower[0]))


# %%
def cmp_height_4(a, b):
    assert len(a) == 4, "a must be a height 4 tower"
    assert len(b) == 4, "b must be a height 4 tower"

    shouldbe3, a_rep = p2rep(a)
    assert shouldbe3 == 3, "p2rep(a) must return height of 3"

    shouldbe3, b_rep = p2rep(b)
    assert shouldbe3 == 3, "p2rep(b) must return height of 3"

    if a_rep < b_rep:
        return -1
    if a_rep > b_rep:
        return 1

    return 0


# %%
def cmp_height_3(a, b):
    assert len(a) == 3, "a must be a height 3 tower"
    assert len(b) == 3, "b must be a height 3 tower"

    shouldbe2, a_rep = p2rep(a)
    assert shouldbe2 == 2, "p2rep(a) must return height of 2"

    shouldbe2, b_rep = p2rep(b)
    assert shouldbe2 == 2, "p2rep(b) must return height of 2"

    if a_rep < b_rep:
        return -1
    if a_rep > b_rep:
        return 1

    return 0


# %%
t1 = (5, 4, 7, 71)
t2 = (4, 5, 75, 32)
cmp_height_4(tuple(Decimal(x) for x in t1), tuple(Decimal(x) for x in t2))

# %%
# generate all possible height 3 towers:
HEIGHT3 = []
for a in NUMS:
    for b in NUMS:
        for c in NUMS:
            HEIGHT3.append((a, b, c))


# sort HEIGHT3 towers by their power of 2 representation
HEIGHT3.sort(key=lambda x: p2rep(x)[1])

loc = {tower: i for i, tower in enumerate(HEIGHT3)}

# %%
PAIRWISE_LOGS = [(i, j, l(j, i)) for i in NUMS for j in NUMS if j > i]
PAIRWISE_LOGS.sort(key=lambda x: x[2])
print(PAIRWISE_LOGS[-1])

# %%
for i in tqdm(list(range(len(HEIGHT3) - 1))[::-1]):
    a = HEIGHT3[i + 1]
    b = HEIGHT3[i]
    res3 = cmp_height_3(a, b)
    assert res3 >= 0, f"{a} {b}"
    if res3 == 0:
        continue
    result = cmp_height_4((Decimal(2), *a), (Decimal(100), *b))
    if result < 0:
        print("nihilism is false")
        print(a, b)
        break


# %%
def compute_height3_ratio(a, b):
    assert len(a) == 3, "a must be a height 3 tower"
    assert len(b) == 3, "b must be a height 3 tower"

    if cmp_height_3(a, b) == 0:
        return (1,)

    if cmp_height_3(a, b) < 0:
        a, b = b, a

    # a > b always now
    # binary search over PAIRWISE_LOGS to find
    # the pair (i, j, lij) such that
    # (i, *a) / (j, *b) is < log_i(j)

    lo = 0
    hi = len(PAIRWISE_LOGS) - 1

    while lo < hi:
        mid = (lo + hi) // 2
        i, j, lij = PAIRWISE_LOGS[mid]
        result = cmp_height_4((i, *a), (j, *b))
        if result == 0:
            return (i, j, lij)
        if result < 0:
            print("WOW")
            hi = mid
        else:
            lo = mid + 1

    mid = (lo + hi) // 2
    i, j, lij = PAIRWISE_LOGS[mid]
    return (i, j, lij)


# %%
for i in tqdm(list(range(len(HEIGHT3) - 1))[::-1][800000:]):
    j = i + 1
    a = HEIGHT3[i]
    b = HEIGHT3[j]
    ratio = compute_height3_ratio(a, b)
    if len(ratio) == 1:
        print(f"{a} {b}")
        continue
    if ratio[2] < PAIRWISE_LOGS[-1][2]:
        if a[0] == b[0]:
            continue
        print(f"{a} {b}")
        print(f"{ratio}")
        print("nihilism is false")
        break


# %%
sa = tuple(str(Decimal(x)) for x in a)
sb = tuple(str(Decimal(x)) for x in b)
print(sa, sb, cmp_height_3(a, b))
print((100, *sa), (99, *sb), cmp_height_4((Decimal(100), *a), (Decimal(99), *b)))
