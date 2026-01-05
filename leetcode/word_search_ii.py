# LeetCode 212: Word Search II
#%%
"""
Problem Statement:
Given an m x n board of characters and a list of strings words, return all words
on the board.

Each word must be constructed from letters of sequentially adjacent cells, where
adjacent cells are horizontally or vertically neighboring. The same letter cell
may not be used more than once in a word.

Example 1:
Input: board = [["o","a","a","n"],
                ["e","t","a","e"],
                ["i","h","k","r"],
                ["i","f","l","v"]]
       words = ["oath","pea","eat","rain"]
Output: ["eat","oath"]

Example 2:
Input: board = [["a","b"],["c","d"]]
       words = ["abcb"]
Output: []

INTERVIEW EXPLANATION: Why Trie + DFS for Word Search II?

1. **Problem Structure**: We need to find ALL words from a list in the board.
   Running Word Search I for each word would be O(N × 4^L × #words) which is
   too slow. Instead, we use a Trie to combine all words and do one DFS.

2. **Why Trie + DFS?**
   - **Trie Structure**: Build a Trie of all words. Each node represents a
     character, and we can check if a path in the Trie matches a path in the board.
   
   - **Single DFS Traversal**: Instead of searching for each word separately,
     we traverse the board once and simultaneously check all possible word
     matches using the Trie.
   
   - **Time Complexity**: 
     * Building Trie: O(W × L) where W = #words, L = avg word length
     * DFS: O(m × n × 4^L) in worst case, but Trie pruning makes it much faster
     * Overall: Much better than O(N × 4^L × #words)
   
   - **Space Complexity**: O(W × L) for Trie + O(L) for recursion stack

3. **Key Optimizations**:
   - Remove found words from Trie to avoid duplicates
   - Prune Trie nodes when they become leaves (no more words)
   - Early termination when no words match current path

4. **Key Insight**: The Trie allows us to check multiple words simultaneously
   as we traverse the board, rather than searching for each word independently.
"""

from typing import List, Set


class TrieNode:
    """Trie node for storing words"""
    def __init__(self):
        self.children = {}
        self.word = None  # Store full word at end node


class Solution:
    """Solution for Word Search II"""
    
    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:
        """
        Find all words from the list that exist in the board.
        
        Args:
            board: 2D grid of characters
            words: List of words to search for
            
        Returns:
            List of words found in the board
        """
        if not board or not board[0] or not words:
            return []
        
        # Build Trie
        root = TrieNode()
        for word in words:
            node = root
            for ch in word:
                if ch not in node.children:
                    node.children[ch] = TrieNode()
                node = node.children[ch]
            node.word = word  # Store word at end node
        
        rows, cols = len(board), len(board[0])
        result = []
        
        def dfs(r: int, c: int, node: TrieNode) -> None:
            """
            DFS to find words starting from position (r, c).
            
            Args:
                r: Row index
                c: Column index
                node: Current Trie node
            """
            ch = board[r][c]
            
            # Check if current character exists in Trie
            if ch not in node.children:
                return
            
            nxt = node.children[ch]
            
            # If we found a word, add it to result
            if nxt.word:
                result.append(nxt.word)
                nxt.word = None  # Avoid duplicates
            
            # Mark as visited
            board[r][c] = '#'
            
            # Explore all 4 directions
            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] != '#':
                    dfs(nr, nc, nxt)
            
            # Restore original value
            board[r][c] = ch
            
            # Pruning: remove leaf node if it has no children
            if not nxt.children:
                node.children.pop(ch)
        
        # Start DFS from each cell
        for i in range(rows):
            for j in range(cols):
                dfs(i, j, root)
        
        return result


def test_word_search_ii():
    """Test cases for Word Search II"""
    sol = Solution()
    
    # Test case 1: Example 1
    board1 = [
        ["o","a","a","n"],
        ["e","t","a","e"],
        ["i","h","k","r"],
        ["i","f","l","v"]
    ]
    words1 = ["oath","pea","eat","rain"]
    result1 = sol.findWords(board1, words1)
    result1_set = set(result1)
    expected1_set = {"eat", "oath"}
    assert result1_set == expected1_set, f"Expected {expected1_set}, got {result1_set}"
    print(f"✓ Test 1: Found {result1}")
    
    # Test case 2: Example 2
    board2 = [["a","b"],["c","d"]]
    words2 = ["abcb"]
    result2 = sol.findWords(board2, words2)
    assert result2 == [], f"Expected [], got {result2}"
    print(f"✓ Test 2: No words found (correct)")
    
    # Test case 3: Single word
    board3 = [["a"]]
    words3 = ["a"]
    result3 = sol.findWords(board3, words3)
    assert result3 == ["a"], f"Expected ['a'], got {result3}"
    print(f"✓ Test 3: Single word found")
    
    # Test case 4: Empty words
    board4 = [["a","b"]]
    words4 = []
    result4 = sol.findWords(board4, words4)
    assert result4 == [], f"Expected [], got {result4}"
    print(f"✓ Test 4: Empty words list")
    
    print("\nAll tests passed!")


if __name__ == "__main__":
    test_word_search_ii()
    
    # Example usage
    print("\nExample usage:")
    sol = Solution()
    board = [
        ["o","a","a","n"],
        ["e","t","a","e"],
        ["i","h","k","r"],
        ["i","f","l","v"]
    ]
    words = ["oath","pea","eat","rain"]
    result = sol.findWords(board, words)
    print(f"Board:")
    for row in board:
        print(f"  {row}")
    print(f"\nSearching for: {words}")
    print(f"Found: {result}")
# %%

