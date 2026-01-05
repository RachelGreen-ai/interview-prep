# LeetCode 79: Word Search
#%%
"""
Problem Statement:
Given an m x n board of characters and a string word, return true if word exists
in the grid.

The word can be constructed from letters of sequentially adjacent cells, where
adjacent cells are horizontally or vertically neighboring. The same letter cell
may not be used more than once.

Example 1:
Input: board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]]
       word = "ABCCED"
Output: true

Example 2:
Input: board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]]
       word = "SEE"
Output: true

Example 3:
Input: board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]]
       word = "ABCB"
Output: false

INTERVIEW EXPLANATION: Why Backtracking DFS for Word Search?

1. **Problem Structure**: We need to find a path in a 2D grid that spells the
   word. At each cell, we can move to adjacent cells (up/down/left/right) and
   cannot reuse cells.

2. **Why Backtracking DFS?**
   - **Exploration**: We need to explore all possible paths from each starting
     position. DFS naturally explores paths depth-first.
   
   - **State Management**: We need to mark cells as visited during exploration
     and restore them when backtracking. This is classic backtracking.
   
   - **Time Complexity**: O(m * n * 4^L) where L = word length
     * Start from each cell: O(m * n)
     * Each path explores up to 4^L possibilities (4 directions, L steps)
     * In practice, pruning makes it much faster
   
   - **Space Complexity**: O(L) for recursion stack

3. **Key Techniques**:
   - Mark visited cells temporarily (e.g., change to '#')
   - Restore after backtracking
   - Prune early if current path cannot form word
   - Check bounds before exploring neighbors

4. **Optimization**: Early termination - return True immediately when word found
"""

from typing import List


class Solution:
    """Solution for Word Search problem"""
    
    def exist(self, board: List[List[str]], word: str) -> bool:
        """
        Check if word exists in the board.
        
        Args:
            board: 2D grid of characters
            word: Word to search for
            
        Returns:
            True if word exists, False otherwise
        """
        if not board or not board[0] or not word:
            return False
        
        rows, cols = len(board), len(board[0])
        
        def dfs(r: int, c: int, idx: int) -> bool:
            """
            DFS to find word starting from position (r, c).
            
            Args:
                r: Row index
                c: Column index
                idx: Current index in word
                
            Returns:
                True if word found, False otherwise
            """
            # Base case: found the word
            if idx == len(word):
                return True
            
            # Check bounds
            if r < 0 or r >= rows or c < 0 or c >= cols:
                return False
            
            # Check if current cell matches current character
            if board[r][c] != word[idx]:
                return False
            
            # Mark as visited (temporarily)
            temp = board[r][c]
            board[r][c] = '#'
            
            # Explore all 4 directions
            found = (dfs(r + 1, c, idx + 1) or
                    dfs(r - 1, c, idx + 1) or
                    dfs(r, c + 1, idx + 1) or
                    dfs(r, c - 1, idx + 1))
            
            # Backtrack: restore original value
            board[r][c] = temp
            
            return found
        
        # Try starting from each cell
        for i in range(rows):
            for j in range(cols):
                if dfs(i, j, 0):
                    return True
        
        return False


def test_word_search():
    """Test cases for Word Search"""
    sol = Solution()
    
    # Test case 1: Example 1
    board1 = [
        ["A", "B", "C", "E"],
        ["S", "F", "C", "S"],
        ["A", "D", "E", "E"]
    ]
    word1 = "ABCCED"
    result1 = sol.exist(board1, word1)
    assert result1 == True, f"Expected True, got {result1}"
    print(f"✓ Test 1: Word '{word1}' found")
    
    # Test case 2: Example 2
    board2 = [
        ["A", "B", "C", "E"],
        ["S", "F", "C", "S"],
        ["A", "D", "E", "E"]
    ]
    word2 = "SEE"
    result2 = sol.exist(board2, word2)
    assert result2 == True, f"Expected True, got {result2}"
    print(f"✓ Test 2: Word '{word2}' found")
    
    # Test case 3: Example 3
    board3 = [
        ["A", "B", "C", "E"],
        ["S", "F", "C", "S"],
        ["A", "D", "E", "E"]
    ]
    word3 = "ABCB"
    result3 = sol.exist(board3, word3)
    assert result3 == False, f"Expected False, got {result3}"
    print(f"✓ Test 3: Word '{word3}' not found")
    
    # Test case 4: Single character
    board4 = [["A"]]
    word4 = "A"
    result4 = sol.exist(board4, word4)
    assert result4 == True, f"Expected True, got {result4}"
    print(f"✓ Test 4: Single character found")
    
    # Test case 5: Empty word
    board5 = [["A", "B"]]
    word5 = ""
    result5 = sol.exist(board5, word5)
    assert result5 == False, f"Expected False, got {result5}"
    print("✓ Test 5: Empty word handled")
    
    print("\nAll tests passed!")


if __name__ == "__main__":
    test_word_search()
    
    # Example usage
    print("\nExample usage:")
    sol = Solution()
    board = [
        ["A", "B", "C", "E"],
        ["S", "F", "C", "S"],
        ["A", "D", "E", "E"]
    ]
    word = "ABCCED"
    result = sol.exist(board, word)
    print(f"Board:")
    for row in board:
        print(f"  {row}")
    print(f"\nSearching for: '{word}'")
    print(f"Result: {result}")
# %%

