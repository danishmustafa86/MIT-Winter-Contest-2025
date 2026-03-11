# Tart splitting problem

import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    s = input().strip()
    target = 'M' + 'IT' * n
    if s == target:
        print(0)
    elif target in s + s:
        print(1)
    else:
        print(-1)

t = int(input())
for _ in range(t):
    solve()
