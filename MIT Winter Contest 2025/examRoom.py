def solve():
    n = int(input())
    points = []
    for _ in range(n):
        x, y = map(int, input().split())
        points.append((x, y))
    
    # Compute squared distances from origin
    dist_origin = []
    for x, y in points:
        dist_origin.append(x*x + y*y)
    
    # Build compatibility graph
    can_coexist = [[True] * n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            dx = points[i][0] - points[j][0]
            dy = points[i][1] - points[j][1]
            dist_sq = dx*dx + dy*dy
            if dist_sq <= dist_origin[i] or dist_sq <= dist_origin[j]:
                can_coexist[i][j] = False
                can_coexist[j][i] = False
    
    MOD = 998244353
    
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if not can_coexist[i][j]:
                adj[i].append(j)
                adj[j].append(i)
    
    # For small N, use bitmask enumeration
    if n <= 22:
        incomp = [0] * n
        for i in range(n):
            for j in adj[i]:
                incomp[i] |= (1 << j)
        
        count = 0
        for mask in range(1, 1 << n):
            valid = True
            for i in range(n):
                if (mask & (1 << i)) and (mask & incomp[i]):
                    valid = False
                    break
            if valid:
                count += 1
        print(count % MOD)
    else:
        # For larger N, use recursive DP with memoization
        import sys
        sys.setrecursionlimit(100000)
        
        memo = {}
        
        def dp(idx, forbidden):
            # idx: current point to decide
            # forbidden: frozenset of points we cannot use
            if idx == n:
                return 1
            
            # If current point is forbidden, skip it
            if idx in forbidden:
                return dp(idx + 1, forbidden)
            
            # Only keep forbidden points that are > idx for memoization
            key = (idx, frozenset(x for x in forbidden if x > idx))
            if key in memo:
                return memo[key]
            
            # Option 1: Don't use point idx
            result = dp(idx + 1, forbidden)
            
            # Option 2: Use point idx (forbid all neighbors)
            new_forbidden = forbidden | frozenset(adj[idx])
            result = (result + dp(idx + 1, new_forbidden)) % MOD
            
            memo[key] = result
            return result
        
        # Start DP, then subtract empty set
        total = dp(0, frozenset())
        print((total - 1) % MOD)

solve()