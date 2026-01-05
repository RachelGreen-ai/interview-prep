# LeetCode 773: Sliding Puzzle
#%%
"""
Problem Statement:
On a 2x3 board, there are 5 tiles represented by the integers 1 through 5, and an empty square
represented by 0. A move consists of choosing 0 and a 4-directionally adjacent number and swapping it.

The state of the board is solved if and only if the board is [[1,2,3],[4,5,0]].

Given a puzzle board, return the least number of moves required so that the state of the board
is solved. If it is impossible for the state of the board to be solved, return -1.

Example 1:
Input: board = [[1,2,3],[4,0,5]]
Output: 1
Explanation: Swap the 0 and the 5 in one move.

Example 2:
Input: board = [[1,2,3],[5,4,0]]
Output: -1
Explanation: No number of moves will make the board solved.

Example 3:
Input: board = [[4,1,2],[5,0,3]]
Output: 5
Explanation: 5 is the smallest number of moves required to solve the puzzle.

INTERVIEW EXPLANATION: Why BFS for Sliding Puzzle?

1. **Problem Structure**: This is a shortest path problem in a state space.
   Each board configuration is a state, and we can transition between states by swapping 0
   with adjacent tiles. We need to find the minimum number of moves to reach the target state.

2. **Why BFS?**
   - **Shortest Path**: BFS guarantees finding the shortest path in an unweighted graph
   - **State Space Search**: Each board configuration is a node, swaps are edges
   - **Optimal Solution**: BFS explores level by level, so first solution found is optimal
   - **Avoid Cycles**: We can track visited states to avoid revisiting

3. **Algorithm**:
   a. Start from initial board state
   b. Use BFS to explore all possible next states
   c. For each state, generate all valid moves (swaps with 0)
   d. Check if we've reached target state [[1,2,3],[4,5,0]]
   e. Track visited states to avoid cycles
   f. Return minimum moves when target is found

4. **Key Insights**:
   - Represent board as a string or tuple for hashing/equality checks
   - Only swap 0 with adjacent tiles (up, down, left, right)
   - Track visited states to avoid infinite loops
   - Early termination when target is found

5. **Time Complexity**: O(6! * 6) = O(4320) in worst case
   - There are 6! = 720 possible board states
   - Each state can have up to 4 neighbors (swaps)
   - We visit each state at most once

6. **Space Complexity**: O(6!) for visited set and queue
"""

from collections import deque


class Solution:
    """Solution for Sliding Puzzle"""
    
    def slidingPuzzle(self, board: list[list[int]]) -> int:
        """
        Find minimum moves to solve the sliding puzzle.
        
        Args:
            board: 2x3 board with tiles 0-5
            
        Returns:
            Minimum moves to solve, or -1 if impossible
        """
        # Convert board to string for easier manipulation
        start = self._board_to_string(board)
        target = "123450"
        
        # If already solved
        if start == target:
            return 0
        
        # BFS to find shortest path
        queue = deque([(start, 0)])  # (state, moves)
        visited = {start}
        
        while queue:
            state, moves = queue.popleft()
            
            # Generate all possible next states
            next_states = self._get_next_states(state)
            
            for next_state in next_states:
                if next_state == target:
                    return moves + 1
                
                if next_state not in visited:
                    visited.add(next_state)
                    queue.append((next_state, moves + 1))
        
        return -1  # Impossible to solve
    
    def _board_to_string(self, board: list[list[int]]) -> str:
        """Convert 2x3 board to string representation."""
        return ''.join(str(board[i][j]) for i in range(2) for j in range(3))
    
    def _get_next_states(self, state: str) -> list[str]:
        """
        Generate all possible next states by swapping 0 with adjacent tiles.
        
        Args:
            state: Current board state as string "123450"
            
        Returns:
            List of next possible states
        """
        # Find position of 0
        zero_pos = state.index('0')
        row, col = zero_pos // 3, zero_pos % 3
        
        next_states = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # right, left, down, up
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            
            # Check bounds
            if 0 <= new_row < 2 and 0 <= new_col < 3:
                # Calculate new position index
                new_pos = new_row * 3 + new_col
                
                # Swap 0 with tile at new_pos
                state_list = list(state)
                state_list[zero_pos], state_list[new_pos] = state_list[new_pos], state_list[zero_pos]
                next_states.append(''.join(state_list))
        
        return next_states
    
    def slidingPuzzle_optimized(self, board: list[list[int]]) -> int:
        """
        Optimized version with bidirectional BFS.
        """
        start = self._board_to_string(board)
        target = "123450"
        
        if start == target:
            return 0
        
        # Bidirectional BFS
        forward_queue = deque([start])
        backward_queue = deque([target])
        forward_visited = {start: 0}
        backward_visited = {target: 0}
        
        while forward_queue or backward_queue:
            # Expand forward
            if forward_queue:
                state = forward_queue.popleft()
                moves = forward_visited[state]
                
                for next_state in self._get_next_states(state):
                    if next_state in backward_visited:
                        return moves + 1 + backward_visited[next_state]
                    
                    if next_state not in forward_visited:
                        forward_visited[next_state] = moves + 1
                        forward_queue.append(next_state)
            
            # Expand backward
            if backward_queue:
                state = backward_queue.popleft()
                moves = backward_visited[state]
                
                for next_state in self._get_next_states(state):
                    if next_state in forward_visited:
                        return moves + 1 + forward_visited[next_state]
                    
                    if next_state not in backward_visited:
                        backward_visited[next_state] = moves + 1
                        backward_queue.append(next_state)
        
        return -1


def test_sliding_puzzle():
    """Test cases for Sliding Puzzle"""
    sol = Solution()
    
    # Test case 1: Example 1
    board1 = [[1,2,3],[4,0,5]]
    result1 = sol.slidingPuzzle(board1)
    assert result1 == 1, f"Expected 1, got {result1}"
    print(f"✓ Test 1: board={board1}")
    print(f"  Result: {result1} moves")
    
    # Test case 2: Example 2
    board2 = [[1,2,3],[5,4,0]]
    result2 = sol.slidingPuzzle(board2)
    assert result2 == -1, f"Expected -1, got {result2}"
    print(f"✓ Test 2: board={board2}")
    print(f"  Result: {result2} (impossible)")
    
    # Test case 3: Example 3
    board3 = [[4,1,2],[5,0,3]]
    result3 = sol.slidingPuzzle(board3)
    assert result3 == 5, f"Expected 5, got {result3}"
    print(f"✓ Test 3: board={board3}")
    print(f"  Result: {result3} moves")
    
    # Test case 4: Already solved
    board4 = [[1,2,3],[4,5,0]]
    result4 = sol.slidingPuzzle(board4)
    assert result4 == 0, f"Expected 0, got {result4}"
    print(f"✓ Test 4: Already solved")
    print(f"  Result: {result4} moves")
    
    print("\nAll tests passed!")


if __name__ == "__main__":
    test_sliding_puzzle()
    
    # Example usage
    print("\nExample usage:")
    sol = Solution()
    
    board = [[1,2,3],[4,0,5]]
    result = sol.slidingPuzzle(board)
    print(f"Initial board: {board}")
    print(f"Minimum moves to solve: {result}")
# %%

