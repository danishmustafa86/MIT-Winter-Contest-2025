def solve():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    c = list(map(int, data[1:N+1]))
    
    # To keep track of visited containers
    visited = [False] * N
    actions = []
    
    for i in range(N):
        if not visited[i]:
            # Start a new cycle
            cycle = []
            x = i
            while not visited[x]:
                visited[x] = True
                cycle.append(x)
                x = c[x] - 1  # Move to the next container in the cycle
            
            # Resolve the cycle
            for j in range(len(cycle) - 1):
                actions.append(f"1 {cycle[j] + 1} {cycle[j + 1] + 1}")
    
    # Output the result
    print(len(actions))
    for action in actions:
        print(action)

if __name__ == "__main__":
    solve()