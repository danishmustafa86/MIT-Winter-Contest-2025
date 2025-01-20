import sys

input = sys.stdin.read
data = input().split()
idx = 0

# Read N and Q from first line
n, q = int(data[idx]), int(data[idx+1])
idx += 2

# Read initial array
a = list(map(int, data[idx:idx+n]))
idx += n

results = []

# Process Q queries
for _ in range(q):
    query_type = int(data[idx])
    if query_type == 1:
        # Update operation
        x, y = int(data[idx+1]), int(data[idx+2])
        a[x-1] = y
        idx += 3
    elif query_type == 2:
        # Find missing number operation
        l, r = int(data[idx+1]), int(data[idx+2])
        idx += 3
        
        # Get the numbers present in the range [l,r]
        present = set(a[l-1:r])
        
        # Find first missing number from 1 to N
        for num in range(1, n+1):
            if num not in present:
                results.append(num)
                break

# Output results
sys.stdout.write("\n".join(map(str, results)) + "\n")