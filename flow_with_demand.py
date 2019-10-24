def _augment_ford_fulkerson(graph, capacity, flow, upper_boundary, u, target, visit):
    visit[u] = True
    if u == target:
        return upper_boundary
    for v in graph[u]:
        cuv = capacity[u][v]
        if not visit[v] and cuv > flow[u][v]:
            res = min(upper_boundary, cuv - flow[u][v])
            delta = _augment_ford_fulkerson(graph, capacity, flow, res, v, target, visit)
            if delta > 0:
                flow[u][v] += delta
                flow[v][u] -= delta
                return delta

    return 0


def ford_fulkerson(graph, capacity, s, t):
    n = len(graph)
    flow = [[0] * n for _ in range(n)]
    delta = 1
    while delta > 0:
        visit = [False] * n
        delta = _augment_ford_fulkerson(graph, capacity, flow, float('inf'), s, t, visit)
    return flow


def display_flow(flow):
    for i in range(len(flow)):
        s = "flow for vertice " + str(i) + ": "
        for j in range(len(flow[0])):
            if i != j and flow[i][j] > 0:
                s += "(towards " + str(j) + ", value " + str(flow[i][j]) + "), "
        print(s)


def test_ford_fulkerson():
    graph = [
        [1, 2],  # 0
        [3, 4, 2],  # 1
        [4, 1],  # 2
        [5, 4, 1],  # 3
        [5, 3, 1, 2],  # 4
        [3, 4],  # 5
    ]
    capacity = [
        [0, 10, 10, 0, 0, 0],  # 0
        [10, 0, 2, 4, 8, 0],  # 1
        [10, 2, 0, 0, 9, 0],  # 2
        [0, 4, 0, 0, 5, 10],  # 3
        [0, 8, 9, 5, 0, 10],  # 4
        [0, 0, 0, 10, 10, 0],  # 5
    ]

    display_flow(ford_fulkerson(graph, capacity, 0, 5))


print("With Ford-Fulkerson:")
test_ford_fulkerson()


############################## with demand


def check_flow_satisfies_demand(flow, demand):
    for i in range(len(demand)):
        for j in range(0, len(demand[0])):
            if demand[i][j] > 0 and flow[i][j] < demand[i][j]:
                return False
    return True


def _augment_flow_with_demand(graph, capacity, demand, flow, upper_boundary, u, target, visit):
    visit[u] = True
    if u == target:
        return upper_boundary

    def iteration(demand_or_flow):
        for v in graph[u]:
            if not visit[v] and demand_or_flow[u][v] > flow[u][v]:
                res = min(upper_boundary, demand_or_flow[u][v] - flow[u][v])
                delta = _augment_flow_with_demand(graph, capacity, demand, flow, res, v, target, visit)
                if delta > 0:
                    flow[u][v] += delta
                    flow[v][u] -= delta
                    return delta
        return 0

    # satisfy demand in priority
    delta = iteration(demand)
    if delta > 0:
        return delta

    # if all demand for the children of u is satisfied, increase the flow based on capacity
    return iteration(capacity)


def flow_with_demand(graph, capacity, demand, s, t):
    n = len(graph)
    flow = [[0] * n for _ in range(n)]
    delta = 1
    while delta > 0:
        visit = [False] * n
        delta = _augment_flow_with_demand(graph, capacity, demand, flow, float('inf'), s, t, visit)

    if not check_flow_satisfies_demand(flow, demand):
        raise ValueError("This demand cannot be satisfied")

    return flow


def test_flow_with_demand():
    graph = [
        [1, 2],  # 0
        [3, 4, 2],  # 1
        [4, 1],  # 2
        [5, 4, 1],  # 3
        [5, 3, 1, 2],  # 4
        [3, 4],  # 5
    ]

    capacity = [
        [0, 10, 10, 0, 0, 0],  # 0
        [10, 0, 2, 4, 8, 0],  # 1
        [10, 2, 0, 0, 9, 0],  # 2
        [0, 4, 0, 0, 5, 10],  # 3
        [0, 8, 9, 5, 0, 10],  # 4
        [0, 0, 0, 10, 10, 0],  # 5
    ]

    demand = [
        [0, 5, 5, 0, 0, 0],  # 0
        [0, 0, 0, 4, 3, 0],  # 1
        [0, 2, 0, 0, 5, 0],  # 2
        [0, 0, 0, 0, 0, 7],  # 3
        [0, 0, 0, 1, 0, 7],  # 4
        [0, 0, 0, 0, 0, 0],  # 5
    ]

    display_flow(flow_with_demand(graph, capacity, demand, 0, 5))


print("With demand:")
test_flow_with_demand()
