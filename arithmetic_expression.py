# i and j are always included.


def find_operators_indexes(expression, i, j):
    indexes = []
    for k in range(i, j+1):
        if expression[k] == '+':
            indexes.append(k)

    return indexes


def dist_to_correctness_with_operator(D, i, j, operator_index):
    if operator_index == i:
        return 1 + D[i + 1][j]

    if operator_index == j:
        return 1 + D[i][j - 1]

    if D[i][operator_index - 1] == operator_index - i or D[operator_index + 1][j] == j - operator_index:
        # one of the term of the sum needs to be deleted completely:
        # the + is at the beginning or the end of the valid expression.
        return D[i][operator_index - 1] + D[operator_index + 1][j] + 1

    return D[i][operator_index - 1] + D[operator_index + 1][j]


def dist_to_correctness(expression):
    n = len(expression)

    # initialisation
    D = [[float('inf') for _ in range(n)] for _ in range(n)]
    for i in range(0, n):
        if expression[i] == 'x' or expression[i] == 'y':
            D[i][i] = 0
        else:
            D[i][i] = 1

    # iteration diagonal by diagonal.
    for d in range(1, n):
        i = 0
        j = d
        while i < n - d:
            operator_indexes = find_operators_indexes(expression, i, j)

            # if we have a non empty expression between parenthesis
            if expression[i] == '(' and expression[j] == ')' and j - i + 1 >= 3:
                if D[i+1][j-1] == (j - 1) - (i + 1) + 1:
                    # if we suppressed all the characters between the parenthesis,
                    # we need to suppress the parenthesis as well.
                    D[i][j] = D[i+1][j-1] + 2
                else:
                    # if we did not suppress all the characters between parenthesis
                    D[i][j] = D[i+1][j-1]

            for k in operator_indexes:
                D[i][j] = min(D[i][j], dist_to_correctness_with_operator(D, i, j, k))

            # try deleting first or last letter
            if j - i + 1 > 1:
                D[i][j] = min(D[i][j], D[i+1][j] + 1, D[i][j-1] + 1)

            i += 1
            j += 1

    return D[0][n-1]


def test():
    test_cases = [
        ("x", 0),
        ("()", 2),
        ("(x)", 0),
        ("(x+y)", 0),
        ("(x+y)+(x+y)", 0),
        ("((x+y)+(x+y))", 0),
        ("(x)+(y)", 0),
        ("((x)+(y))", 0),
        ("x(", 1),
        ("x(x", 2),
        ("x()x", 3),
        ("x)(x", 3),
        ("x(+)y", 2),
        ("((x)(+)(y))", 2),
        ("+", 1),
        ("x++y", 1),
        ("(x+y)x", 1),
        ("(x+y)(x", 2),
        ("((x+y)x)+x(x+y)", 2),
        ("x+(y", 1),
        ("(x++y)x", 2),
        ("(x+(y)x((", 4),
        ("(x+(y)x))", 2),
        (")(", 2),
        ("(+)", 3),
        ("+++", 3),
        ("+++x+y+++", 6),
        ("))()()((", 8),
    ]

    for (expression, expected_distance) in test_cases:
        print("Computation for expression " + expression + " / Result should be " + str(expected_distance))
        computed_distance = dist_to_correctness(expression)
        if computed_distance != expected_distance:
            print("Got " + str(computed_distance) + " instead")


test()
