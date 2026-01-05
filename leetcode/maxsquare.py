# LeetCode 221: Maximal Square
#%%
"""
Problem Statement:
Given an m x n binary matrix filled with 0's and 1's, find the largest square
containing only 1's and return its area.

Example 1:
Input: matrix = [["1","0","1","0","0"],
                 ["1","0","1","1","1"],
                 ["1","1","1","1","1"],
                 ["1","0","0","1","0"]]
Output: 4
Explanation: The largest square is 2x2.

Example 2:
Input: matrix = [["0","1"],["1","0"]]
Output: 1

INTERVIEW EXPLANATION: Why DP for Maximal Square?

from typing import List

"""

1. **Problem Structure**: We need to find the largest square of 1's. 
   A square at position (i,j) can only exist if:
   - Current cell is '1'
   - The three adjacent squares (top, left, top-left) can also form squares
   
2. **Why DP?**
   - **Optimal Substructure**: The size of the largest square ending at (i,j) 
     depends on the largest squares ending at (i-1,j), (i,j-1), and (i-1,j-1).
     We can build up the solution from smaller subproblems.
   
   - **Overlapping Subproblems**: When checking if a square exists, we repeatedly 
     check the same sub-squares. DP avoids recomputation.
   
   - **Key Insight**: If we want a square of side length k at (i,j), we need:
     * A square of at least (k-1) at (i-1,j)
     * A square of at least (k-1) at (i,j-1)  
     * A square of at least (k-1) at (i-1,j-1)
     * Current cell must be '1'
     
     Therefore: dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1
     
     The minimum ensures we can only extend the square if ALL three neighbors 
     support a square of that size. If any neighbor has a smaller square, 
     that becomes our limiting factor.

3. **Time Complexity**: O(m*n) - single pass through matrix
4. **Space Complexity**: O(m*n) - DP table (can be optimized to O(n))
"""

class Solution:
    def maximalSquare(self, matrix: List[List[str]]) -> int:
        if not matrix: return 0
        m, n = len(matrix), len(matrix[0])
        # dp[i][j] = side   length of largest square ending at (i,j)
        dp = [[0] * n for _ in range(m)]
        max_side = 0
        
        for i in range(m):
            for j in range(n):
                if matrix[i][j] == '1':
                    # Base case: first row/col can only form 1x1 squares
                    if i == 0 or j == 0:
                        dp[i][j] = 1
                    else:
                        # Recurrence: take minimum of three neighbors + 1
                        # This ensures we can extend the square uniformly
                        dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1
                    max_side = max(max_side, dp[i][j])
        
        return max_side * max_side


def test_maximal_square():
    """Test cases for Maximal Square"""
    sol = Solution()
    
    # Test case 1: Example 1
    matrix1 = [["1","0","1","0","0"],
               ["1","0","1","1","1"],
               ["1","1","1","1","1"],
               ["1","0","0","1","0"]]
    result1 = sol.maximalSquare(matrix1)
    assert result1 == 4, f"Expected 4, got {result1}"
    print(f"✓ Test 1: Result = {result1} (2x2 square)")
    
    # Test case 2: Example 2
    matrix2 = [["0","1"],["1","0"]]
    result2 = sol.maximalSquare(matrix2)
    assert result2 == 1, f"Expected 1, got {result2}"
    print(f"✓ Test 2: Result = {result2}")
    
    # Test case 3: Single cell
    matrix3 = [["0"]]
    result3 = sol.maximalSquare(matrix3)
    assert result3 == 0, f"Expected 0, got {result3}"
    print(f"✓ Test 3: Result = {result3}")
    
    # Test case 4: All ones
    matrix4 = [["1","1"],["1","1"]]
    result4 = sol.maximalSquare(matrix4)
    assert result4 == 4, f"Expected 4, got {result4}"
    print(f"✓ Test 4: Result = {result4}")
    
    print("\nAll tests passed!")


if __name__ == "__main__":
    test_maximal_square()
    
    # Example usage
    print("\nExample usage:")
    sol = Solution()
    matrix = [["1","0","1","0","0"],
              ["1","0","1","1","1"],
              ["1","1","1","1","1"],
              ["1","0","0","1","0"]]
    result = sol.maximalSquare(matrix)
    print(f"Input matrix:")
    for row in matrix:
        print(f"  {row}")
    print(f"\nLargest square area: {result}")
# %%