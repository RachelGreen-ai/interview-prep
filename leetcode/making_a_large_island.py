# LeetCode 827: Making A Large Island
#%%
"""
Problem Statement:
You are given an n x n binary matrix grid. You are allowed to change at most one 0 to be 1.

Return the size of the largest island in grid after applying this operation.

An island is a 4-directionally connected group of 1s.

Example 1:
Input: grid = [[1,0],[0,1]]
Output: 4
Explanation: Change one 0 to 1 and connect two 1s, then we get an island with area = 4.

Example 2:
Input: grid = [[1,1],[1,0]]
Output: 4
Explanation: Change the 0 to 1 and make the island bigger, only one island with area = 4.

Example 3:
Input: grid = [[1,1],[1,1]]
Output: 4
Explanation: Can't change any 0 to 1, only one island with area = 4.

INTERVIEW EXPLANATION: Why Two-Pass DFS for Making A Large Island?

1. **Problem Structure**: We need to:
   - Find all existing islands and their sizes
   - For each 0, check which islands it can connect
   - Find the maximum island size after connecting

2. **Why Two-Pass Approach?**
   - **First Pass**: Identify all islands and assign IDs, calculate sizes
   - **Second Pass**: For each 0, check adjacent islands and calculate potential size
   - **Union Find Alternative**: Could use Union-Find, but DFS is simpler here

3. **Algorithm**:
   a. First pass: DFS to label each island with unique ID and store sizes
   b. For each cell with value 1, mark it with island ID
   c. Store island sizes in a map: island_id -> size
   d. Second pass: For each 0:
      - Check 4 neighbors
      - Collect unique island IDs adjacent to this 0
      - Sum sizes of adjacent islands + 1 (for the 0 we're changing)
      - Track maximum

4. **Key Insights**:
   - Use island IDs to avoid double-counting when a 0 connects multiple islands
   - Only consider unique adjacent islands (use set)
   - If no 0s exist, return size of largest island
   - Handle edge case: all 1s or all 0s

5. **Time Complexity**: O(n²) - visit each cell at most twice
   
6. **Space Complexity**: O(n²) for island labels and size map
"""


class Solution:
    """Solution for Making A Large Island"""
    
    def largestIsland(self, grid: list[list[int]]) -> int:
        """
        Find largest island after changing at most one 0 to 1.
        
        Args:
            grid: Binary matrix (0 or 1)
            
        Returns:
            Size of largest island after operation
        """
        n = len(grid)
        island_id = 2  # Start from 2 (0 and 1 are already used)
        island_sizes = {}  # island_id -> size
        
        # First pass: label islands and calculate sizes
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        def dfs(row: int, col: int, current_id: int) -> int:
            """DFS to label island and return size."""
            if not (0 <= row < n and 0 <= col < n) or grid[row][col] != 1:
                return 0
            
            grid[row][col] = current_id
            size = 1
            
            for dr, dc in directions:
                size += dfs(row + dr, col + dc, current_id)
            
            return size
        
        # Label all islands
        for i in range(n):
            for j in range(n):
                if grid[i][j] == 1:
                    size = dfs(i, j, island_id)
                    island_sizes[island_id] = size
                    island_id += 1
        
        # If no islands found, return 0 or 1
        if not island_sizes:
            return 1 if any(any(row) for row in grid) else 0
        
        max_size = max(island_sizes.values())
        
        # Second pass: try changing each 0 to 1
        for i in range(n):
            for j in range(n):
                if grid[i][j] == 0:
                    # Find adjacent unique islands
                    adjacent_islands = set()
                    for dr, dc in directions:
                        ni, nj = i + dr, j + dc
                        if 0 <= ni < n and 0 <= nj < n and grid[ni][nj] > 1:
                            adjacent_islands.add(grid[ni][nj])
                    
                    # Calculate size if we change this 0 to 1
                    new_size = 1 + sum(island_sizes[island_id] for island_id in adjacent_islands)
                    max_size = max(max_size, new_size)
        
        return max_size
    
    def largestIsland_optimized(self, grid: list[list[int]]) -> int:
        """
        Optimized version with better structure.
        """
        n = len(grid)
        island_id = 2
        island_sizes = {}
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        # First pass: label islands
        def dfs(r: int, c: int, id: int) -> int:
            if r < 0 or r >= n or c < 0 or c >= n or grid[r][c] != 1:
                return 0
            grid[r][c] = id
            return 1 + sum(dfs(r + dr, c + dc, id) for dr, dc in directions)
        
        for i in range(n):
            for j in range(n):
                if grid[i][j] == 1:
                    size = dfs(i, j, island_id)
                    island_sizes[island_id] = size
                    island_id += 1
        
        if not island_sizes:
            return 1 if any(any(row) for row in grid) else 0
        
        max_size = max(island_sizes.values())
        
        # Second pass: try changing 0s
        for i in range(n):
            for j in range(n):
                if grid[i][j] == 0:
                    neighbors = {grid[i+dr][j+dc] for dr, dc in directions
                                if 0 <= i+dr < n and 0 <= j+dc < n and grid[i+dr][j+dc] > 1}
                    max_size = max(max_size, 1 + sum(island_sizes[nid] for nid in neighbors))
        
        return max_size


def test_making_large_island():
    """Test cases for Making A Large Island"""
    sol = Solution()
    
    # Test case 1: Example 1
    grid1 = [[1,0],[0,1]]
    result1 = sol.largestIsland([row[:] for row in grid1])  # Copy to avoid modification
    assert result1 == 4, f"Expected 4, got {result1}"
    print(f"✓ Test 1: 2x2 grid")
    print(f"  Result: {result1}")
    
    # Test case 2: Example 2
    grid2 = [[1,1],[1,0]]
    result2 = sol.largestIsland([row[:] for row in grid2])
    assert result2 == 4, f"Expected 4, got {result2}"
    print(f"✓ Test 2: 2x2 grid")
    print(f"  Result: {result2}")
    
    # Test case 3: Example 3
    grid3 = [[1,1],[1,1]]
    result3 = sol.largestIsland([row[:] for row in grid3])
    assert result3 == 4, f"Expected 4, got {result3}"
    print(f"✓ Test 3: All 1s")
    print(f"  Result: {result3}")
    
    # Test case 4: Single cell
    grid4 = [[0]]
    result4 = sol.largestIsland([row[:] for row in grid4])
    assert result4 == 1, f"Expected 1, got {result4}"
    print(f"✓ Test 4: Single 0")
    print(f"  Result: {result4}")
    
    print("\nAll tests passed!")


if __name__ == "__main__":
    test_making_large_island()
    
    # Example usage
    print("\nExample usage:")
    sol = Solution()
    
    grid = [[1,0],[0,1]]
    result = sol.largestIsland([row[:] for row in grid])
    print(f"Grid: {grid}")
    print(f"Largest island after changing one 0: {result}")
# %%

