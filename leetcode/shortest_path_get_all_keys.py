# LeetCode 864: Shortest Path to Get All Keys
#%%
"""
Problem Statement:
You are given an m x n grid grid where:
- '.' is an empty cell.
- '#' is a wall.
- '@' is the starting point.
- Lowercase letters represent keys.
- Uppercase letters represent locks.

You start at the starting point and one move consists of walking one space in one of
the four cardinal directions. You cannot walk outside the grid, or walk into a wall.

If you walk over a key, you can pick it up and you cannot walk over a lock unless
you have its corresponding key.

For some 1 <= k <= 6, there is exactly one lowercase and one uppercase letter of the
first k letters of the English alphabet in the grid. This means that there is exactly
one key for each lock, and one lock for each key, and keys and locks are paired.

Return the lowest number of moves to acquire all keys. If it is impossible, return -1.

Example 1:
Input: grid = ["@.a..","###.#","b.A.B"]
Output: 8
Explanation: Note that the goal is to obtain all the keys not to open all the locks.

Example 2:
Input: grid = ["@..aA","..B#.","....b"]
Output: 6

Example 3:
Input: grid = ["@Aa"]
Output: -1

INTERVIEW EXPLANATION: Why BFS with State for Shortest Path to Get All Keys?

1. **Problem Structure**: This is a shortest path problem with state (keys collected).
   We need to find the minimum steps to collect all keys, where having keys allows
   us to pass through corresponding locks.

2. **Why BFS with State?**
   - **Shortest Path**: BFS finds shortest path in unweighted graph
   - **State Space**: Each position (x, y) with a set of keys is a unique state
   - **State Tracking**: Use bitmask to represent which keys we have (k <= 6, so 2^6 = 64 states)
   - **Visited Set**: Track (x, y, keys_mask) to avoid revisiting same state

3. **Algorithm**:
   a. Find starting position and count total keys
   b. Use BFS with state (x, y, keys_collected)
   c. For each state, try moving to 4 neighbors
   d. If neighbor is a key, pick it up (update keys_mask)
   e. If neighbor is a lock, check if we have the key
   f. If we've collected all keys, return current steps
   g. Track visited states to avoid cycles

4. **Key Insights**:
   - Use bitmask to represent keys: keys_mask = 0b111111 means all 6 keys collected
   - State is (row, col, keys_mask)
   - Can visit same cell multiple times if we have different keys
   - Early termination when all keys collected

5. **Time Complexity**: O(m * n * 2^k) where k is number of keys
   - m * n positions
   - 2^k possible key combinations
   - Each state visited at most once

6. **Space Complexity**: O(m * n * 2^k) for visited set and queue
"""

from collections import deque


class Solution:
    """Solution for Shortest Path to Get All Keys"""
    
    def shortestPathAllKeys(self, grid: list[str]) -> int:
        """
        Find shortest path to collect all keys.
        
        Args:
            grid: 2D grid with walls, keys, locks, and starting point
            
        Returns:
            Minimum steps to collect all keys, or -1 if impossible
        """
        m, n = len(grid), len(grid[0])
        
        # Find starting position and count keys
        start_row, start_col = -1, -1
        total_keys = 0
        
        for i in range(m):
            for j in range(n):
                if grid[i][j] == '@':
                    start_row, start_col = i, j
                elif grid[i][j].islower():
                    total_keys += 1
        
        if total_keys == 0:
            return 0
        
        # Target: all keys collected (bitmask with all bits set)
        target_keys = (1 << total_keys) - 1
        
        # BFS: (row, col, keys_mask, steps)
        queue = deque([(start_row, start_col, 0, 0)])
        visited = {(start_row, start_col, 0)}
        
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        while queue:
            row, col, keys_mask, steps = queue.popleft()
            
            # Try moving to 4 neighbors
            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc
                
                # Check bounds
                if not (0 <= new_row < m and 0 <= new_col < n):
                    continue
                
                cell = grid[new_row][new_col]
                
                # Hit a wall
                if cell == '#':
                    continue
                
                # Check if it's a lock
                if cell.isupper():
                    # Need corresponding key
                    key_index = ord(cell) - ord('A')
                    if not (keys_mask & (1 << key_index)):
                        continue  # Don't have the key
                
                # Update keys if we pick up a new key
                new_keys_mask = keys_mask
                if cell.islower():
                    key_index = ord(cell) - ord('a')
                    new_keys_mask |= (1 << key_index)
                
                # Check if we've collected all keys
                if new_keys_mask == target_keys:
                    return steps + 1
                
                # Check if we've visited this state before
                state = (new_row, new_col, new_keys_mask)
                if state not in visited:
                    visited.add(state)
                    queue.append((new_row, new_col, new_keys_mask, steps + 1))
        
        return -1  # Impossible to collect all keys
    
    def shortestPathAllKeys_verbose(self, grid: list[str]) -> int:
        """
        More verbose version with detailed comments.
        """
        m, n = len(grid), len(grid[0])
        
        # Step 1: Find starting position and identify all keys
        start_row, start_col = -1, -1
        key_positions = {}  # Map key letter to its index
        
        for i in range(m):
            for j in range(n):
                if grid[i][j] == '@':
                    start_row, start_col = i, j
                elif grid[i][j].islower():
                    # Assign index to each key (0, 1, 2, ...)
                    if grid[i][j] not in key_positions:
                        key_positions[grid[i][j]] = len(key_positions)
        
        total_keys = len(key_positions)
        if total_keys == 0:
            return 0
        
        # Step 2: BFS with state tracking
        # State: (row, col, keys_bitmask)
        # keys_bitmask: bit i is set if we have key with index i
        target_mask = (1 << total_keys) - 1
        
        queue = deque([(start_row, start_col, 0, 0)])
        visited = {(start_row, start_col, 0)}
        
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        while queue:
            row, col, keys_mask, steps = queue.popleft()
            
            for dr, dc in directions:
                nr, nc = row + dr, col + dc
                
                # Boundary check
                if not (0 <= nr < m and 0 <= nc < n):
                    continue
                
                cell = grid[nr][nc]
                
                # Wall: cannot pass
                if cell == '#':
                    continue
                
                # Lock: need corresponding key
                if cell.isupper():
                    lock_index = ord(cell) - ord('A')
                    if lock_index >= total_keys:
                        continue  # Invalid lock
                    if not (keys_mask & (1 << lock_index)):
                        continue  # Don't have the key
                
                # Key: pick it up
                new_keys_mask = keys_mask
                if cell.islower():
                    key_index = ord(cell) - ord('a')
                    if key_index < total_keys:
                        new_keys_mask |= (1 << key_index)
                
                # Check if we've collected all keys
                if new_keys_mask == target_mask:
                    return steps + 1
                
                # Add to queue if not visited
                state = (nr, nc, new_keys_mask)
                if state not in visited:
                    visited.add(state)
                    queue.append((nr, nc, new_keys_mask, steps + 1))
        
        return -1


def test_shortest_path_all_keys():
    """Test cases for Shortest Path to Get All Keys"""
    sol = Solution()
    
    # Test case 1: Example 1
    grid1 = ["@.a..","###.#","b.A.B"]
    result1 = sol.shortestPathAllKeys(grid1)
    assert result1 == 8, f"Expected 8, got {result1}"
    print(f"✓ Test 1: {len(grid1)}x{len(grid1[0])} grid")
    print(f"  Result: {result1} steps")
    
    # Test case 2: Example 2
    grid2 = ["@..aA","..B#.","....b"]
    result2 = sol.shortestPathAllKeys(grid2)
    assert result2 == 6, f"Expected 6, got {result2}"
    print(f"✓ Test 2: {len(grid2)}x{len(grid2[0])} grid")
    print(f"  Result: {result2} steps")
    
    # Test case 3: Example 3
    grid3 = ["@Aa"]
    result3 = sol.shortestPathAllKeys(grid3)
    assert result3 == -1, f"Expected -1, got {result3}"
    print(f"✓ Test 3: Impossible case")
    print(f"  Result: {result3}")
    
    # Test case 4: No keys
    grid4 = ["@.."]
    result4 = sol.shortestPathAllKeys(grid4)
    assert result4 == 0, f"Expected 0, got {result4}"
    print(f"✓ Test 4: No keys to collect")
    print(f"  Result: {result4}")
    
    print("\nAll tests passed!")


if __name__ == "__main__":
    test_shortest_path_all_keys()
    
    # Example usage
    print("\nExample usage:")
    sol = Solution()
    
    grid = ["@.a..","###.#","b.A.B"]
    result = sol.shortestPathAllKeys(grid)
    print(f"Grid: {grid}")
    print(f"Minimum steps to collect all keys: {result}")
# %%

