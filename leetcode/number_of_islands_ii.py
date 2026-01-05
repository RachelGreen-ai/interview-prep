# LeetCode 305: Number of Islands II (Finding Ocean)
#%%
"""
Problem Statement:
You are given an empty 2D binary grid grid of size m x n. The grid represents
a map where 0's represent water and 1's represent land. Initially, all the
cells of grid are water cells (i.e., all the cells are 0's).

We may perform an add land operation which turns the water at position into a
land. You are given an array positions where positions[i] = [ri, ci] is the
position (ri, ci) at which we should operate the i-th operation.

Return an array of integers answer where answer[i] is the number of islands
after turning the cell (ri, ci) into a land.

An island is surrounded by water and is formed by connecting adjacent lands
horizontally or vertically. You may assume all four edges of the grid are all
surrounded by water.

Example 1:
Input: m = 3, n = 3, positions = [[0,0], [0,1], [1,2], [2,1]]
Output: [1,1,2,3]
Explanation:
Initially, the 2d grid is filled with water.
- Operation #1: addLand(0, 0) turns the water at grid[0][0] into a land.
  We have 1 island.
- Operation #2: addLand(0, 1) turns the water at grid[0][1] into a land.
  We have 1 island.
- Operation #3: addLand(1, 2) turns the water at grid[1][2] into a land.
  We have 2 islands.
- Operation #4: addLand(2, 1) turns the water at grid[2][1] into a land.
  We have 3 islands.

INTERVIEW EXPLANATION: Why Union-Find for Number of Islands II?

1. **Problem Structure**: We're adding land cells one by one and need to track
   the number of islands after each addition. This is a dynamic connectivity
   problem - perfect for Union-Find (Disjoint Set Union).

2. **Why Union-Find?**
   - **Dynamic Connectivity**: As we add land, we need to:
     * Check if new land connects to existing islands
     * Merge islands if they become connected
     * Count total islands efficiently
   
   - **Key Operations**:
     * find(x): Find root of component containing x
     * union(x, y): Merge components containing x and y
     * addLand(x): Add new land and check neighbors
   
   - **Time Complexity**: 
     * find: O(α(n)) amortized (almost constant with path compression)
     * union: O(α(n)) amortized
     * Overall: O(k × α(m×n)) where k = #operations
   
   - **Space Complexity**: O(m×n) for Union-Find structure

3. **Key Insight**: When adding a new land cell:
   - Initially, it's a new island (+1)
   - Check 4 neighbors (up, down, left, right)
   - If neighbor is land and in different component → merge (-1 per merge)
   - Final count = previous_count + 1 - merges

4. **Optimizations**:
   - Path compression: Flatten tree during find
   - Union by rank: Always attach smaller tree to larger
   - Track count in Union-Find class
"""

from typing import List


class UnionFind:
    """Union-Find (Disjoint Set Union) data structure"""
    
    def __init__(self, size: int):
        self.parent = [-1] * size  # -1 means water, >= 0 means land
        self.rank = [0] * size
        self.count = 0  # Number of islands
    
    def find(self, x: int) -> int:
        """Find root with path compression"""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]
    
    def union(self, x: int, y: int) -> None:
        """Union two components with union by rank"""
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            return  # Already in same component
        
        # Union by rank
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1
        
        self.count -= 1  # Merged two islands into one
    
    def add_land(self, x: int) -> None:
        """Add a new land cell"""
        if self.parent[x] != -1:
            return  # Already land
        
        self.parent[x] = x
        self.count += 1


class Solution:
    """Solution for Number of Islands II"""
    
    def numIslands2(self, m: int, n: int, positions: List[List[int]]) -> List[int]:
        """
        Find number of islands after each land addition.
        
        Args:
            m: Number of rows
            n: Number of columns
            positions: List of [row, col] positions to add land
            
        Returns:
            List of island counts after each operation
        """
        uf = UnionFind(m * n)
        result = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        
        for r, c in positions:
            index = r * n + c
            
            # Add new land
            uf.add_land(index)
            
            # Check neighbors and merge if needed
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n:
                    neighbor_index = nr * n + nc
                    # If neighbor is land, try to union
                    if uf.parent[neighbor_index] != -1:
                        uf.union(index, neighbor_index)
            
            result.append(uf.count)
        
        return result


def test_number_of_islands_ii():
    """Test cases for Number of Islands II"""
    sol = Solution()
    
    # Test case 1: Example 1
    m1, n1, positions1 = 3, 3, [[0,0], [0,1], [1,2], [2,1]]
    result1 = sol.numIslands2(m1, n1, positions1)
    expected1 = [1, 1, 2, 3]
    assert result1 == expected1, f"Expected {expected1}, got {result1}"
    print(f"✓ Test 1: {result1}")
    
    # Test case 2: All connected
    m2, n2, positions2 = 2, 2, [[0,0], [0,1], [1,0], [1,1]]
    result2 = sol.numIslands2(m2, n2, positions2)
    expected2 = [1, 1, 1, 1]  # All merge into one island
    assert result2 == expected2, f"Expected {expected2}, got {result2}"
    print(f"✓ Test 2: {result2}")
    
    # Test case 3: No connections
    m3, n3, positions3 = 3, 3, [[0,0], [0,2], [2,0], [2,2]]
    result3 = sol.numIslands2(m3, n3, positions3)
    expected3 = [1, 2, 3, 4]  # All separate islands
    assert result3 == expected3, f"Expected {expected3}, got {result3}"
    print(f"✓ Test 3: {result3}")
    
    # Test case 4: Empty positions
    m4, n4, positions4 = 2, 2, []
    result4 = sol.numIslands2(m4, n4, positions4)
    assert result4 == [], f"Expected [], got {result4}"
    print("✓ Test 4: Empty positions")
    
    print("\nAll tests passed!")


if __name__ == "__main__":
    test_number_of_islands_ii()
    
    # Example usage
    print("\nExample usage:")
    sol = Solution()
    m, n = 3, 3
    positions = [[0,0], [0,1], [1,2], [2,1]]
    result = sol.numIslands2(m, n, positions)
    
    print(f"Grid: {m}×{n}")
    print("Operations:")
    for i, (r, c) in enumerate(positions, 1):
        print(f"  {i}. Add land at ({r}, {c}) → {result[i-1]} island(s)")
# %%

