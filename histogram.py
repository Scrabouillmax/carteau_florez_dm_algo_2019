def rectangle_area(histogram, i, j):
    if i == j:
        return 0
    minimum_height = min(histogram[i:j])
    return minimum_height * (j - i)


def max_rectangles(histogram):
    n = len(histogram)
    S = [0] * (n + 1)

    for j in range(1, n+1):
        maximum = rectangle_area(histogram, 0, j)
        for k in range(1, j):
            area = rectangle_area(histogram, k + 1, j)
            print((k, area, S[k] + area))
            if S[k] + area > maximum:
                maximum = S[k] + area
        S[j] = maximum

    return S[n]


def test():
    test_cases = [
        # 7
        ([7], 7),
        # 7, 7
        ([7, 8], 14),
        # 7, 7, 7
        ([7, 8, 7], 21),
        # 7, 7, 7, 0
        ([7, 8, 7, 4], 21),
        # 7, 7, 7, 0, 5
        ([7, 8, 7, 4, 5], 26),
        # 7, 7, 7, 0, 5, 5
        ([7, 8, 7, 4, 5, 6], 31),
        # 7, 7, 7, 0, 5, 5, 5
        ([7, 8, 7, 4, 5, 6, 6], 36),
        # 7, 7, 7, 0, 5, 5, 5, 0
        ([7, 8, 7, 4, 5, 6, 6, 3], 36),
        # 7, 7, 7, 0, 5, 5, 5, 0, 4
        ([7, 8, 7, 4, 5, 6, 6, 3, 4], 40),
        # 7, 7, 7, 0, 5, 5, 5, 0, 0, 8
        ([7, 8, 7, 4, 5, 6, 6, 3, 4, 8], 44),
    ]

    for hist, maxi in test_cases:
        print(hist, " Expected: ", maxi, " / Actual: ", max_rectangles(hist))


test()
