import math

NUMS = list(range(2, 101))


def l2(x):
    return math.log(x, 2)


def p2rep(tower):
    if len(tower) <= 3:
        # pad the end of the tower with 1s
        tower.extend([1] * (3 - len(tower)))

        a1 = tower[0]
        a2 = tower[1]
        a3 = tower[2]

        r = a3 * l2(a2) + l2(l2(a1))
        return (2, r)

    else:
        k, top_rep = p2rep(tower[1:])
        lli = l2(l2(tower[0]))


p2rep([2, 2, 2])
p2rep([2, 25, 2])
p2rep([2, 7, 71])
p2rep([2, 75, 32])
