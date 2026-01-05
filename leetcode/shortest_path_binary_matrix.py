# LeetCode 1091: Shortest Path in Binary Matrix
#%%
"""
Problem Statement:
Given an n x n binary matrix grid, return the length of the shortest clear path from
the top-left corner (0, 0) to the bottom-right corner (n - 1, n - 1). If such a path
does not exist, return -1.

A clear path in a binary matrix is a path from the top-left cell to the bottom-right cell such that:
- All the visited cells of the path are 0.
- All the adjacent cells of the path are 8-directionally connected (i.e., they are different
  and they share a corner or an edge).

The length of a clear path is the number of visited cells of this path.

Example 1:
Input: grid = [[0,1],[1,0]]
Output: 2

Example 2:
Input: grid = [[0,0,0],[1,1,0],[1,1,0]]
Output: 4

Example 3:
Input: grid = [[1,0,0],[1,1,0],[1,1,0]]
Output: -1

INTERVIEW EXPLANATION: Why BFS for Shortest Path in Binary Matrix?

1. **Problem Structure**: This is a shortest path problem in an unweighted graph.
   Each cell is a node, and edges connect to 8-directionally adjacent cells (if value is 0).

2. **Why BFS?**
   - **Shortest Path**: BFS guarantees finding shortest path in unweighted graph
   - **Level-by-Level**: Explores nodes level by level, first path found is shortest
   - **8 Directions**: Can move in 8 directions (up, down, left, right, and 4 diagonals)
   - **Visited Tracking**: Mark visited cells to avoid revisiting

3. **Algorithm**:
   a. Start BFS from (0, 0)
   b. If start or end is 1, return -1
   c. Use queue: (row, col, path_length)
   d. For each cell, try all 8 neighbors
   e. If neighbor is 0 and not visited, add to queue
   f. When we reach (n-1, n-1), return path length
   g. If queue empties without reaching end, return -1

4. **Key Insights**:
   - 8-directional movement (not just 4)
   - Path length = number of cells visited (including start and end)
   - Early termination when destination reached
   - Check boundaries and cell values (must be 0)

5. **Time Complexity**: O(n²) - visit each cell at most once
   
6. **Space Complexity**: O(n²) for queue and visited set
"""

from collections import deque


class Solution:
    """Solution for Shortest Path in Binary Matrix"""
    
    def shortestPathBinaryMatrix(self, grid: list[list[int]]) -> int:
        """
        Find shortest path from top-left to bottom-right.
        
        Args:
            grid: Binary matrix (0 = clear, 1 = blocked)
            
        Returns:
            Length of shortest path, or -1 if no path exists
        """
        n = len(grid)
        
        # Check if start or end is blocked
        if grid[0][0] == 1 or grid[n-1][n-1] == 1:
            return -1
        
        # BFS: (row, col, path_length)
        queue = deque([(0, 0, 1)])
        visited = {(0, 0)}
        
        # 8 directions: up, down, left, right, and 4 diagonals
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]
        
        while queue:
            row, col, length = queue.popleft()
            
            # Check if we reached destination
            if row == n - 1 and col == n - 1:
                return length
            
            # Try all 8 directions
            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc
                
                # Check bounds
                if not (0 <= new_row < n and 0 <= new_col < n):
                    continue
                
                # Check if cell is clear and not visited
                if grid[new_row][new_col] == 0 and (new_row, new_col) not in visited:
                    visited.add((new_row, new_col))
                    queue.append((new_row, new_col, length + 1))
        
        return -1  # No path found
    
    def shortestPathBinaryMatrix_optimized(self, grid: list[list[int]]) -> int:
        """
        Optimized version with early termination and better space usage.
        """
        n = len(grid)
        
        if grid[0][0] == 1 or grid[n-1][n-1] == 1:
            return -1
        
        # Use grid itself to mark visited (set to 1)
        queue = deque([(0, 0, 1)])
        grid[0][0] = 1  # Mark as visited
        
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]
        
        while queue:
            row, col, length = queue.popleft()
            
            if row == n - 1 and col == n - 1:
                return length
            
            for dr, dc in directions:
                nr, nc = row + dr, col + dc
                
                if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 0:
                    grid[nr][nc] = 1  # Mark as visited
                    queue.append((nr, nc, length + 1))
        
        return -1


def test_shortest_path_binary_matrix():
    """Test cases for Shortest Path in Binary Matrix"""
    sol = Solution()
    
    # Test case 1: Example 1
    grid1 = [[0,1],[1,0]]
    result1 = sol.shortestPathBinaryMatrix(grid1)
    assert result1 == 2, f"Expected 2, got {result1}"
    print(f"✓ Test 1: 2x2 grid")
    print(f"  Result: {result1}")
    
    # Test case 2: Example 2
    grid2 = [[0,0,0],[1,1,0],[1,1,0]]
    result2 = sol.shortestPathBinaryMatrix(grid2)
    assert result2 == 4, f"Expected 4, got {result2}"
    print(f"✓ Test 2: 3x3 grid")
    print(f"  Result: {result2}")
    
    # Test case 3: Example 3
    grid3 = [[1,0,0],[1,1,0],[1,1,0]]
    result3 = sol.shortestPathBinaryMatrix(grid3)
    assert result3 == -1, f"Expected -1, got {result3}"
    print(f"✓ Test 3: No path (start blocked)")
    print(f"  Result: {result3}")
    
    # Test case 4: Single cell
    grid4 = [[0]]
    result4 = sol.shortestPathBinaryMatrix(grid4)
    assert result4 == 1, f"Expected 1, got {result4}"
    print(f"✓ Test 4: Single cell")
    print(f"  Result: {result4}")
    
    # Test case 5: End blocked
    grid5 = [[0,0],[0,1]]
    result5 = sol.shortestPathBinaryMatrix(grid5)
    assert result5 == -1, f"Expected -1, got {result5}"
    print(f"✓ Test 5: End blocked")
    print(f"  Result: {result5}")
    
    print("\nAll tests passed!")


if __name__ == "__main__":
    test_shortest_path_binary_matrix()
    
    # Example usage
    print("\nExample usage:")
    sol = Solution()
    
    grid = [[0,0,0],[1,1,0],[1,1,0]]
    result = sol.shortestPathBinaryMatrix(grid)
    print(f"Grid: {grid}")
    print(f"Shortest path length: {result}")
# %%

