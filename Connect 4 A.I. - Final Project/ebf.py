def ebf(nNodes, depth, precision=0.01):
    if nNodes == 0:
        return 0

    def ebfRec(low, high):
        mid = (low + high) * 0.5
        if mid == 1:
            estimate = 1 + depth
        else:
            estimate = (1 - mid**(depth + 1)) / (1 - mid)
        if abs(estimate - nNodes) < precision:
            return mid
        if estimate > nNodes:
            return ebfRec(low, mid)
        else:
            return ebfRec(mid, high)

    return ebfRec(1, nNodes)
