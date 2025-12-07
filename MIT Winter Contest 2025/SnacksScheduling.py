def count_inversions(arr):
    """Count inversions using merge sort - O(n log n)"""
    def merge_sort(arr):
        if len(arr) <= 1:
            return arr, 0
        
        mid = len(arr) // 2
        left, left_inv = merge_sort(arr[:mid])
        right, right_inv = merge_sort(arr[mid:])
        
        merged = []
        inversions = left_inv + right_inv
        i = j = 0
        
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                inversions += len(left) - i
                j += 1
        
        merged.extend(left[i:])
        merged.extend(right[j:])
        
        return merged, inversions
    
    _, inversions = merge_sort(arr)
    return inversions

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        # Check if any value is blocked everywhere
        blocked_count = [0] * (n + 1)
        for x in a:
            blocked_count[x] += 1
        
        if any(blocked_count[j] == n for j in range(1, n + 1)):
            print(-1)
            continue
        
        # Precompute: for each value, count available positions
        avail_count = [0] * (n + 1)
        for val in range(1, n + 1):
            avail_count[val] = n - blocked_count[val]
        
        # Simple greedy without expensive checks
        p = []
        used = [False] * (n + 1)
        impossible = False
        
        for i in range(n):
            # Find smallest unused value that can go at position i
            best_val = -1
            
            for val in range(1, n + 1):
                if not used[val] and a[i] != val:
                    # This value is available
                    # Heuristic: prefer values with fewer total options (more constrained)
                    best_val = val
                    break
            
            if best_val == -1:
                impossible = True
                break
            
            p.append(best_val)
            used[best_val] = True
        
        if impossible:
            print(-1)
        else:
            # Verify the solution is valid
            valid = True
            if len(p) != n or len(set(p)) != n:
                valid = False
            for i in range(n):
                if p[i] == a[i]:
                    valid = False
                    break
            
            if valid:
                inversions = count_inversions(p)
                print(inversions)
            else:
                print(-1)

solve()

