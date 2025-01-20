from collections import deque
from typing import Set

def get_next_states(s: str) -> Set[str]:
    """Get all possible states after one transformation."""
    states = set()
    n = len(s)
    
    # Try AAB -> BAA transformation
    for i in range(n-2):
        if s[i:i+3] == "AAB":
            states.add(s[:i] + "BAA" + s[i+3:])
    
    # Try BAA -> AAB transformation
    for i in range(n-2):
        if s[i:i+3] == "BAA":
            states.add(s[:i] + "AAB" + s[i+3:])
    
    # Try BBA -> ABB transformation
    for i in range(n-2):
        if s[i:i+3] == "BBA":
            states.add(s[:i] + "ABB" + s[i+3:])
    
    # Try ABB -> BBA transformation
    for i in range(n-2):
        if s[i:i+3] == "ABB":
            states.add(s[:i] + "BBA" + s[i+3:])
    
    return states

def solve_subtask1(s1: str, s2: str) -> int:
    """Solve subtask 1: Exactly one B in both strings."""
    if s1.count('B') != 1 or s2.count('B') != 1:
        return -1
    
    pos1 = s1.index('B')
    pos2 = s2.index('B')
    return abs(pos1 - pos2)

def solve_subtask2(s1: str, s2: str) -> int:
    """Solve subtask 2: S1 is all A's followed by B's, S2 is all B's followed by A's."""
    if not (s1.count('A') == s2.count('A') and s1.count('B') == s2.count('B')):
        return -1
    
    # For the pattern AAAAAABBB -> BBBAAAAAA:
    # 1. We need to move each B to the front
    # 2. Each move can shift a B by one position through AAB -> BAA transformation
    # 3. For n B's and m A's, we need n*(m/3) rounded up moves
    # This is because we can move multiple B's simultaneously in some cases
    
    b_count = s1.count('B')
    a_count = s1.count('A')
    
    # Each B needs to move through all A's, but we can do it more efficiently
    # We need ceil(a_count/3) moves for each group of B's
    return ((a_count + 2) // 3) * 3

def solve_general(s1: str, s2: str) -> int:
    """Solve the general case using BFS."""
    if s1 == s2:
        return 0
        
    if len(s1) != len(s2) or sorted(s1) != sorted(s2):
        return -1
    
    visited = {s1}
    queue = deque([(s1, 0)])
    
    while queue:
        current, steps = queue.popleft()
        
        for next_state in get_next_states(current):
            if next_state == s2:
                return steps + 1
                
            if next_state not in visited:
                visited.add(next_state)
                queue.append((next_state, steps + 1))
    
    return -1

def main():
    import sys
    input = sys.stdin.read
    data = input().splitlines()
    
    T = int(data[0])
    results = []
    
    for i in range(1, T + 1):
        s1, s2 = data[i].split()
        
        if s1.count('B') == 1 and s2.count('B') == 1:
            result = solve_subtask1(s1, s2)
        elif all(c1 <= c2 for c1, c2 in zip(s1, s1[1:])) and \
             all(c1 >= c2 for c1, c2 in zip(s2, s2[1:])):
            result = solve_subtask2(s1, s2)
        else:
            result = solve_general(s1, s2)
        
        results.append(result)
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()