from collections import deque
from typing import List, Set, Tuple

def generate_base_snake(k: int) -> Set[Tuple[int, int]]:
    """Generate base snake pattern of size k*k with alternating right and down steps."""
    snake = set()
    x, y = 0, 0
    moves = 0
    right = True
    
    while moves < k * k:
        snake.add((x, y))
        moves += 1
        
        if right:
            if y + 1 < k:
                y += 1
            else:
                x += 1
            right = False
        else:
            x += 1
            right = True
            
    return snake

def get_all_transformations(pattern: Set[Tuple[int, int]]) -> List[Set[Tuple[int, int]]]:
    """Generate all valid transformations (rotations and reflections) of a pattern."""
    transformations = []
    current = pattern.copy()
    
    # Generate rotations
    for _ in range(4):
        transformations.append(current.copy())
        # Reflect horizontally
        transformations.append({(x, -y) for x, y in current})
        # Reflect vertically
        transformations.append({(-x, y) for x, y in current})
        # Rotate 90 degrees
        current = {(-y, x) for x, y in current}
    
    return transformations

class SnakeValidator:
    def __init__(self):
        self.valid_patterns = {}  # Cache for valid snake patterns
        
    def get_valid_patterns(self, size: int) -> List[Set[Tuple[int, int]]]:
        """Get or generate valid snake patterns of given size."""
        if size not in self.valid_patterns:
            if int(size ** 0.5) ** 2 != size:  # Not a perfect square
                self.valid_patterns[size] = []
            else:
                k = int(size ** 0.5)
                base = generate_base_snake(k)
                self.valid_patterns[size] = get_all_transformations(base)
        return self.valid_patterns[size]
    
    def is_valid_snake(self, component: Set[Tuple[int, int]]) -> bool:
        """Check if a component is a valid snake."""
        if not component:
            return True
            
        size = len(component)
        if size > 25:  # Maximum possible snake size in constraints
            return False
            
        # Normalize component to origin
        min_x = min(x for x, y in component)
        min_y = min(y for x, y in component)
        normalized = {(x - min_x, y - min_y) for x, y in component}
        
        patterns = self.get_valid_patterns(size)
        return any(normalized == pattern for pattern in patterns)

def find_components(grid: List[List[int]], x1: int, y1: int, x2: int, y2: int) -> List[Set[Tuple[int, int]]]:
    """Find all connected components in the subgrid."""
    components = []
    visited = set()
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    for i in range(x1, x2 + 1):
        for j in range(y1, y2 + 1):
            if (i, j) not in visited:
                val = grid[i][j]
                component = set()
                queue = deque([(i, j)])
                
                while queue:
                    x, y = queue.popleft()
                    if (x, y) in visited:
                        continue
                    
                    visited.add((x, y))
                    component.add((x - x1, y - y1))
                    
                    for dx, dy in dirs:
                        nx, ny = x + dx, y + dy
                        if (x1 <= nx <= x2 and y1 <= ny <= y2 and
                            grid[nx][ny] == val and (nx, ny) not in visited):
                            queue.append((nx, ny))
                            
                components.append(component)
    
    return components

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    idx = 0
    N, M = int(data[idx]), int(data[idx+1])
    idx += 2
    
    grid = []
    for i in range(N):
        grid.append(list(map(int, data[idx:idx+M])))
        idx += M
    
    Q = int(data[idx])
    idx += 1
    
    validator = SnakeValidator()
    results = []
    
    for _ in range(Q):
        x1, y1, x2, y2 = int(data[idx]), int(data[idx+1]), int(data[idx+2]), int(data[idx+3])
        idx += 4
        components = find_components(grid, x1, y1, x2, y2)
        
        is_good = all(validator.is_valid_snake(comp) for comp in components)
        results.append("YESYES" if is_good else "NONO")
    
    sys.stdout.write("\n".join(results) + "\n")

if __name__ == "____":
    main()