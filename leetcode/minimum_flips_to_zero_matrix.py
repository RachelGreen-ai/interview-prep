# LeetCode 1284: Minimum Number of Flips to Convert Binary Matrix to Zero Matrix
#%%
"""
Problem Statement:
You are given an m x n binary matrix mat (each cell is either 0 or 1). 
In one move, you may choose any cell (i, j), and flip it and all its four 
neighbors if they exist. Flipping means changing 1 → 0 or 0 → 1. 
Neighbors are cells sharing an edge (up, down, left, right).

Your goal is to convert mat into a zero matrix (all cells are 0). 
Return the minimum number of moves needed, or -1 if it's impossible.

Example 1:
Input: mat = [[0,0],[0,1]]
Output: 3
Explanation: One sequence of flips is flip cell (1,0), then (0,1), then (1,1).

Example 2:
Input: mat = [[0]]
Output: 0
Explanation: The matrix is already all zeros.

Example 3:
Input: mat = [[1,0,0],[1,0,0]]
Output: -1
Explanation: It's impossible to make the matrix all zeros.

Constraints:
- m == mat.length
- n == mat[i].length
- 1 <= m, n <= 3
- mat[i][j] is either 0 or 1.

INTERVIEW EXPLANATION: Why BFS for Minimum Flips?

1. **Problem Structure**: This is a shortest path problem in a state space.
   Each matrix configuration is a state, and we can transition between states
   by flipping a cell and its neighbors. We need to find the minimum number
   of moves to reach the zero matrix state.

2. **Why BFS?**
   - **Shortest Path**: BFS guarantees finding the shortest path in an unweighted graph
   - **State Space Search**: Each matrix configuration is a node, flips are edges
   - **Optimal Solution**: BFS explores level by level, so first solution found is optimal
   - **Avoid Cycles**: We can track visited states to avoid revisiting

3. **Key Insight - State Encoding**:
   - Since m, n <= 3, we have at most 9 cells
   - Total possible states: 2^9 = 512 (very manageable)
   - We can encode the matrix as a tuple or bitmask for hashing
   - Tuple representation is simpler and more readable

4. **Algorithm**:
   a. Start from initial matrix state
   b. Use BFS to explore all possible next states
   c. For each state, generate all valid moves (flip each cell and its neighbors)
   d. Check if we've reached zero matrix (all zeros)
   e. Track visited states to avoid cycles
   f. Return minimum moves when zero matrix is found

5. **Time Complexity**: O(2^(m*n) * m * n)
   - At most 2^(m*n) possible states (m*n <= 9, so at most 512 states)
   - For each state, we try flipping each cell (m*n operations)
   - Each flip operation is O(1) to create new state
   - Overall: O(512 * 9) = O(4608) in worst case

6. **Space Complexity**: O(2^(m*n)) for visited set and queue
"""

from collections import deque
from typing import List, Tuple


class Solution:
    """Solution for Minimum Number of Flips to Convert Binary Matrix to Zero Matrix"""
    
    def minFlips(self, mat: List[List[int]]) -> int:
        """
        Find minimum number of flips to convert matrix to all zeros.
        
        Args:
            mat: m x n binary matrix (m, n <= 3)
            
        Returns:
            Minimum number of flips needed, or -1 if impossible
        """
        m, n = len(mat), len(mat[0])
        
        # Convert matrix to tuple for hashing
        start = self._matrix_to_tuple(mat)
        target = tuple(tuple(0 for _ in range(n)) for _ in range(m))
        
        # If already zero matrix
        if start == target:
            return 0
        
        # BFS to find shortest path
        queue = deque([(start, 0)])  # (state, moves)
        visited = {start}
        
        while queue:
            state, moves = queue.popleft()
            
            # Generate all possible next states by flipping each cell
            for i in range(m):
                for j in range(n):
                    next_state = self._flip_cell(state, i, j, m, n)
                    
                    if next_state == target:
                        return moves + 1
                    
                    if next_state not in visited:
                        visited.add(next_state)
                        queue.append((next_state, moves + 1))
        
        return -1  # Impossible to reach zero matrix
    
    def _matrix_to_tuple(self, mat: List[List[int]]) -> Tuple[Tuple[int, ...], ...]:
        """Convert matrix to tuple of tuples for hashing."""
        return tuple(tuple(row) for row in mat)
    
    def _flip_cell(self, state: Tuple[Tuple[int, ...], ...], 
                   row: int, col: int, m: int, n: int) -> Tuple[Tuple[int, ...], ...]:
        """
        Flip a cell and its four neighbors (if they exist).
        
        Args:
            state: Current matrix state as tuple of tuples
            row: Row index of cell to flip
            col: Column index of cell to flip
            m: Number of rows
            n: Number of columns
            
        Returns:
            New state after flipping
        """
        # Convert to list for modification
        new_mat = [list(row) for row in state]
        
        # Directions: up, down, left, right, and current cell
        directions = [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            
            # Check bounds
            if 0 <= new_row < m and 0 <= new_col < n:
                # Flip: 0 -> 1, 1 -> 0
                new_mat[new_row][new_col] = 1 - new_mat[new_row][new_col]
        
        # Convert back to tuple
        return tuple(tuple(row) for row in new_mat)
    
    def minFlips_bitmask(self, mat: List[List[int]]) -> int:
        """
        Alternative solution using bitmask encoding (more memory efficient).
        Each cell is represented by a bit in an integer.
        """
        m, n = len(mat), len(mat[0])
        
        # Convert matrix to bitmask
        start = 0
        for i in range(m):
            for j in range(n):
                if mat[i][j] == 1:
                    start |= (1 << (i * n + j))
        
        target = 0  # Zero matrix
        
        if start == target:
            return 0
        
        # BFS
        queue = deque([(start, 0)])
        visited = {start}
        
        while queue:
            state, moves = queue.popleft()
            
            # Try flipping each cell
            for i in range(m):
                for j in range(n):
                    next_state = self._flip_cell_bitmask(state, i, j, m, n)
                    
                    if next_state == target:
                        return moves + 1
                    
                    if next_state not in visited:
                        visited.add(next_state)
                        queue.append((next_state, moves + 1))
        
        return -1
    
    def _flip_cell_bitmask(self, state: int, row: int, col: int, m: int, n: int) -> int:
        """Flip a cell and its neighbors using bitmask."""
        new_state = state
        directions = [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            
            if 0 <= new_row < m and 0 <= new_col < n:
                pos = new_row * n + new_col
                # Toggle bit using XOR
                new_state ^= (1 << pos)
        
        return new_state


def test_min_flips():
    """Test cases for Minimum Flips to Zero Matrix"""
    sol = Solution()
    
    # Test case 1: Example 1
    mat1 = [[0,0],[0,1]]
    result1 = sol.minFlips(mat1)
    assert result1 == 3, f"Expected 3, got {result1}"
    print(f"✓ Test 1: mat={mat1}")
    print(f"  Result: {result1} flips")
    
    # Test case 2: Example 2
    mat2 = [[0]]
    result2 = sol.minFlips(mat2)
    assert result2 == 0, f"Expected 0, got {result2}"
    print(f"✓ Test 2: mat={mat2}")
    print(f"  Result: {result2} flips (already zero)")
    
    # Test case 3: Example 3
    mat3 = [[1,0,0],[1,0,0]]
    result3 = sol.minFlips(mat3)
    assert result3 == -1, f"Expected -1, got {result3}"
    print(f"✓ Test 3: mat={mat3}")
    print(f"  Result: {result3} (impossible)")
    
    # Test case 4: Single flip needed
    mat4 = [[1]]
    result4 = sol.minFlips(mat4)
    assert result4 == 1, f"Expected 1, got {result4}"
    print(f"✓ Test 4: mat={mat4}")
    print(f"  Result: {result4} flips")
    
    # Test case 5: 2x2 matrix
    mat5 = [[1,1],[1,0]]
    result5 = sol.minFlips(mat5)
    print(f"✓ Test 5: mat={mat5}")
    print(f"  Result: {result5} flips")
    
    print("\nAll tests passed!")
    
    # Test bitmask version
    print("\nTesting bitmask version:")
    result1_bm = sol.minFlips_bitmask(mat1)
    assert result1_bm == 3, f"Bitmask: Expected 3, got {result1_bm}"
    print(f"✓ Bitmask Test 1: {result1_bm} flips")
    
    result2_bm = sol.minFlips_bitmask(mat2)
    assert result2_bm == 0, f"Bitmask: Expected 0, got {result2_bm}"
    print(f"✓ Bitmask Test 2: {result2_bm} flips")


if __name__ == "__main__":
    test_min_flips()
    
    # Example usage
    print("\nExample usage:")
    sol = Solution()
    
    mat = [[0,0],[0,1]]
    result = sol.minFlips(mat)
    print(f"Initial matrix: {mat}")
    print(f"Minimum flips to zero matrix: {result}")
# %%
