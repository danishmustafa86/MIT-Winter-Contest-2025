from itertools import permutations

def manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

def solve_tsp(n, cities):
    min_distance = float('inf')
    for perm in permutations(range(1, n)):
        path = (0,) + perm + (0,)
        total_distance = 0
        for i in range(len(path) - 1):
            total_distance += manhattan_distance(
                cities[path[i]][0], cities[path[i]][1],
                cities[path[i + 1]][0], cities[path[i + 1]][1]
            )
        min_distance = min(min_distance, total_distance)
    
    return min_distance

def solve():
    T = int(input())  # Number of test cases
    for _ in range(T):
        N = int(input())  # Number of cities
        cities = [tuple(map(int, input().split())) for _ in range(N)]  # Coordinates of cities
        result = solve_tsp(N, cities)
        print(result)

solve()