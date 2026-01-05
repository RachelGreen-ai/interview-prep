# LeetCode 72: Edit Distance
#%%
"""
Problem Statement:
Given two strings word1 and word2, return the minimum number of operations
required to convert word1 to word2.

You have the following three operations permitted on a word:
- Insert a character
- Delete a character
- Replace a character

Example 1:
Input: word1 = "horse", word2 = "ros"
Output: 3
Explanation:
horse -> rorse (replace 'h' with 'r')
rorse -> rose (remove 'r')
rose -> ros (remove 'e')

Example 2:
Input: word1 = "intention", word2 = "execution"
Output: 5
Explanation:
intention -> inention (remove 't')
inention -> enention (replace 'i' with 'e')
enention -> exention (replace 'n' with 'x')
exention -> exection (replace 'n' with 'c')
exection -> execution (insert 'u')

INTERVIEW EXPLANATION: Why Dynamic Programming for Edit Distance?

1. **Problem Structure**: We need to find minimum operations to transform
   word1 into word2. At each position, we have choices:
   - If characters match → no operation needed
   - If characters differ → choose best of insert/delete/replace

2. **Why DP?**
   - **Optimal Substructure**: The minimum edit distance between word1[:i]
     and word2[:j] depends on optimal solutions for smaller subproblems:
     * dp[i-1][j-1] (replace/match)
     * dp[i-1][j] (delete from word1)
     * dp[i][j-1] (insert into word1)
   
   - **Overlapping Subproblems**: Many subproblems are computed multiple times.
     DP avoids recomputation by storing results.
   
   - **Time Complexity**: O(m * n) where m = len(word1), n = len(word2)
   - **Space Complexity**: O(m * n) for DP table, can optimize to O(min(m, n))

3. **Key Insight**: 
   - dp[i][j] = minimum edit distance between word1[:i] and word2[:j]
   - If word1[i-1] == word2[j-1]: dp[i][j] = dp[i-1][j-1] (no operation)
   - Else: dp[i][j] = 1 + min(
       dp[i-1][j],      # delete from word1
       dp[i][j-1],      # insert into word1
       dp[i-1][j-1]     # replace
     )

4. **Base Cases**:
   - dp[0][j] = j (insert j characters)
   - dp[i][0] = i (delete i characters)
"""

from typing import List


class Solution:
    """Solution for Edit Distance problem"""
    
    def minDistance(self, word1: str, word2: str) -> int:
        """
        Find minimum edit distance between two strings.
        
        Args:
            word1: First string
            word2: Second string
            
        Returns:
            Minimum number of operations to convert word1 to word2
        """
        m, n = len(word1), len(word2)
        
        # dp[i][j] = min edit distance between word1[:i] and word2[:j]
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        # Base cases: converting empty string
        for i in range(m + 1):
            dp[i][0] = i  # Delete i characters
        for j in range(n + 1):
            dp[0][j] = j  # Insert j characters
        
        # Fill DP table
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if word1[i - 1] == word2[j - 1]:
                    # Characters match, no operation needed
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    # Choose minimum of three operations
                    dp[i][j] = 1 + min(
                        dp[i - 1][j],      # Delete from word1
                        dp[i][j - 1],      # Insert into word1
                        dp[i - 1][j - 1]    # Replace
                    )
        
        return dp[m][n]
    
    def minDistance_optimized(self, word1: str, word2: str) -> int:
        """
        Space-optimized version using O(min(m, n)) space.
        
        Args:
            word1: First string
            word2: Second string
            
        Returns:
            Minimum number of operations to convert word1 to word2
        """
        m, n = len(word1), len(word2)
        
        # Use shorter string for space optimization
        if m < n:
            word1, word2 = word2, word1
            m, n = n, m
        
        # Only keep previous row
        prev = list(range(n + 1))
        
        for i in range(1, m + 1):
            curr = [i]  # First column
            for j in range(1, n + 1):
                if word1[i - 1] == word2[j - 1]:
                    curr.append(prev[j - 1])
                else:
                    curr.append(1 + min(prev[j], curr[j - 1], prev[j - 1]))
            prev = curr
        
        return prev[n]


def test_edit_distance():
    """Test cases for Edit Distance"""
    sol = Solution()
    
    # Test case 1: Example 1
    word1_1, word2_1 = "horse", "ros"
    result1 = sol.minDistance(word1_1, word2_1)
    assert result1 == 3, f"Expected 3, got {result1}"
    print(f"✓ Test 1: '{word1_1}' -> '{word2_1}' = {result1}")
    
    # Test case 2: Example 2
    word1_2, word2_2 = "intention", "execution"
    result2 = sol.minDistance(word1_2, word2_2)
    assert result2 == 5, f"Expected 5, got {result2}"
    print(f"✓ Test 2: '{word1_2}' -> '{word2_2}' = {result2}")
    
    # Test case 3: Same strings
    word1_3, word2_3 = "abc", "abc"
    result3 = sol.minDistance(word1_3, word2_3)
    assert result3 == 0, f"Expected 0, got {result3}"
    print(f"✓ Test 3: '{word1_3}' -> '{word2_3}' = {result3}")
    
    # Test case 4: One empty string
    word1_4, word2_4 = "", "abc"
    result4 = sol.minDistance(word1_4, word2_4)
    assert result4 == 3, f"Expected 3, got {result4}"
    print(f"✓ Test 4: '{word1_4}' -> '{word2_4}' = {result4}")
    
    # Test case 5: Both empty
    word1_5, word2_5 = "", ""
    result5 = sol.minDistance(word1_5, word2_5)
    assert result5 == 0, f"Expected 0, got {result5}"
    print(f"✓ Test 5: '{word1_5}' -> '{word2_5}' = {result5}")
    
    # Test optimized version
    result1_opt = sol.minDistance_optimized(word1_1, word2_1)
    assert result1_opt == result1, "Optimized version should match"
    print("✓ Optimized version matches")
    
    print("\nAll tests passed!")


if __name__ == "__main__":
    test_edit_distance()
    
    # Example usage
    print("\nExample usage:")
    sol = Solution()
    word1, word2 = "horse", "ros"
    result = sol.minDistance(word1, word2)
    print(f"Input: word1 = '{word1}', word2 = '{word2}'")
    print(f"Output: {result}")
    print("Explanation:")
    print("  horse -> rorse (replace 'h' with 'r')")
    print("  rorse -> rose (remove 'r')")
    print("  rose -> ros (remove 'e')")
# %%

