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
        Space-optimized version using O(min(m, n)) space instead of O(m * n).
        
        KEY INSIGHT - ROLLING ARRAY TECHNIQUE:
        -------------------------------------
        When computing dp[i][j], we only need:
        - dp[i-1][j]   (previous row, same column)
        - dp[i][j-1]   (current row, previous column)
        - dp[i-1][j-1] (previous row, previous column)
        
        We DON'T need the entire 2D table! We only need:
        - Previous row (prev)
        - Current row being built (curr)
        
        Visual:
        Full 2D table:          Optimized (rolling):
        ┌─┬─┬─┬─┐              ┌─┬─┬─┬─┐
        │0│1│2│3│  ← prev      │0│1│2│3│  ← prev (previous row)
        ├─┼─┼─┼─┤              └─┴─┴─┴─┘
        │1│?│?│?│  ← curr      ┌─┬─┬─┬─┐
        ├─┼─┼─┼─┤              │1│?│?│?│  ← curr (current row)
        │2│?│?│?│              └─┴─┴─┴─┘
        └─┴─┴─┴─┘              (only 2 rows at a time!)
        
        After computing curr, we discard old prev and use curr as new prev.
        
        Args:
            word1: First string
            word2: Second string
            
        Returns:
            Minimum number of operations to convert word1 to word2
        """
        m, n = len(word1), len(word2)
        
        # OPTIMIZATION: Use shorter string for columns to minimize space
        # If word1 is shorter, swap them (doesn't change the answer)
        if m < n:
            word1, word2 = word2, word1
            m, n = n, m
        
        # Initialize previous row: dp[0][j] = j (insert j characters)
        # This represents the base case: converting "" to word2[:j]
        prev = list(range(n + 1))
        # prev[j] = edit distance from "" to word2[:j] = j insertions
        
        # Process each row (each character of word1)
        for i in range(1, m + 1):
            # Initialize current row: dp[i][0] = i (delete i characters)
            # This represents converting word1[:i] to "" = i deletions
            curr = [i]
            
            # Fill current row
            for j in range(1, n + 1):
                if word1[i - 1] == word2[j - 1]:
                    # Characters match: no operation needed
                    # dp[i][j] = dp[i-1][j-1]
                    curr.append(prev[j - 1])
                else:
                    # Characters differ: choose minimum of three operations
                    # dp[i][j] = 1 + min(
                    #     dp[i-1][j],      # delete from word1 → prev[j]
                    #     dp[i][j-1],      # insert into word1 → curr[j-1]
                    #     dp[i-1][j-1]     # replace → prev[j-1]
                    # )
                    curr.append(1 + min(
                        prev[j],        # delete: previous row, same column
                        curr[j - 1],    # insert: current row, previous column
                        prev[j - 1]     # replace: previous row, previous column
                    ))
            
            # Move to next row: current becomes previous
            prev = curr
        
        # Final answer: dp[m][n] is in prev[n]
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


def visualize_space_optimization():
    """
    Comprehensive visualization of space optimization for Edit Distance.
    Shows step-by-step how rolling array technique works.
    """
    print("=" * 70)
    print("SPACE OPTIMIZATION: Edit Distance")
    print("=" * 70)
    
    word1, word2 = "horse", "ros"
    m, n = len(word1), len(word2)
    
    print(f"\nExample: word1 = '{word1}' (length {m}), word2 = '{word2}' (length {n})")
    print(f"Full 2D table: O({m} × {n}) = O({m*n}) space")
    print(f"Optimized: O(min({m}, {n})) = O({min(m, n)}) space")
    print(f"Space saved: {m*n} → {min(m, n)} = {m*n - min(m, n)} cells!")
    
    print("\n" + "=" * 70)
    print("1. FULL 2D TABLE APPROACH")
    print("=" * 70)
    print("\nDP Table Structure:")
    print("   Columns represent word2: '' 'r' 'o' 's'")
    print("   Rows represent word1: '' 'h' 'o' 'r' 's' 'e'")
    print("\n   Full table (6 × 4 = 24 cells):")
    print("        ''  'r'  'o'  's'")
    print("   ''   0    1    2    3")
    print("   'h'  1    ?    ?    ?")
    print("   'o'  2    ?    ?    ?")
    print("   'r'  3    ?    ?    ?")
    print("   's'  4    ?    ?    ?")
    print("   'e'  5    ?    ?    ?")
    print("\n   To compute dp[i][j], we need:")
    print("   - dp[i-1][j]   (cell above)")
    print("   - dp[i][j-1]   (cell to the left)")
    print("   - dp[i-1][j-1] (cell diagonally above-left)")
    
    print("\n" + "=" * 70)
    print("2. SPACE-OPTIMIZED APPROACH (Rolling Array)")
    print("=" * 70)
    print("\nKEY INSIGHT:")
    print("   We only need TWO ROWS at a time:")
    print("   - Previous row (prev): dp[i-1][*]")
    print("   - Current row (curr):  dp[i][*]")
    print("\n   After computing curr, we discard old prev and reuse curr as new prev!")
    
    print("\n" + "=" * 70)
    print("3. STEP-BY-STEP VISUALIZATION")
    print("=" * 70)
    
    # Simulate the algorithm
    prev = list(range(n + 1))
    print(f"\nInitialization:")
    print(f"  prev = {prev}  (base case: converting '' to word2[:j])")
    print(f"  This represents: dp[0][j] = j (insert j characters)")
    
    for i in range(1, m + 1):
        char = word1[i - 1]
        curr = [i]
        print(f"\n--- Processing row {i}: word1[{i-1}] = '{char}' ---")
        print(f"  Initialize curr[0] = {i}  (base case: converting word1[:{i}] to '' = {i} deletions)")
        
        for j in range(1, n + 1):
            char2 = word2[j - 1]
            if char == char2:
                val = prev[j - 1]
                curr.append(val)
                print(f"  j={j}: '{char}' == '{char2}' → curr[{j}] = prev[{j-1}] = {val} (match, no operation)")
            else:
                delete = prev[j]
                insert = curr[j - 1]
                replace = prev[j - 1]
                val = 1 + min(delete, insert, replace)
                curr.append(val)
                print(f"  j={j}: '{char}' != '{char2}' → curr[{j}] = 1 + min(delete={delete}, insert={insert}, replace={replace}) = {val}")
        
        print(f"\n  Row {i} complete: curr = {curr}")
        print(f"  prev = {prev}  (old row, will be discarded)")
        print(f"  curr = {curr}  (new row, becomes next prev)")
        prev = curr
    
    print(f"\n--- Final Answer ---")
    print(f"  prev[{n}] = {prev[n]}  (minimum edit distance)")
    
    print("\n" + "=" * 70)
    print("4. MEMORY COMPARISON")
    print("=" * 70)
    print("\nFull 2D Table:")
    print(f"  - Stores: {m + 1} rows × {n + 1} columns = {(m+1) * (n+1)} cells")
    print(f"  - Space: O({m} × {n}) = O({m*n})")
    print(f"  - Memory: ~{(m+1) * (n+1) * 8} bytes (assuming 8 bytes per int)")
    
    print("\nOptimized (Rolling Array):")
    print(f"  - Stores: 2 rows × {n + 1} columns = {2 * (n+1)} cells")
    print(f"  - Space: O(min({m}, {n})) = O({min(m, n)})")
    print(f"  - Memory: ~{2 * (n+1) * 8} bytes")
    print(f"  - Space saved: {(m+1) * (n+1) - 2 * (n+1)} = {(m+1) * (n+1) - 2 * (n+1)} cells!")
    
    print("\n" + "=" * 70)
    print("5. WHY IT WORKS")
    print("=" * 70)
    print("\nDependency Analysis:")
    print("   To compute dp[i][j], we need:")
    print("   ┌─────────┬─────────┬─────────┐")
    print("   │         │ prev[j-1]│ prev[j] │")
    print("   ├─────────┼─────────┼─────────┤")
    print("   │curr[j-1]│ curr[j] │         │")
    print("   └─────────┴─────────┴─────────┘")
    print("\n   Notice:")
    print("   ✓ We only need values from previous row (prev)")
    print("   ✓ We only need values from current row we're building (curr)")
    print("   ✗ We DON'T need rows i-2, i-3, ... (can discard!)")
    print("   ✗ We DON'T need columns j+1, j+2, ... (not computed yet!)")
    
    print("\nRolling Process:")
    print("   1. Start with prev = base case row (dp[0][*])")
    print("   2. For each row i:")
    print("      a. Build curr using prev")
    print("      b. Discard old prev (no longer needed)")
    print("      c. Set prev = curr (for next iteration)")
    print("   3. After processing all rows, answer is in prev[n]")
    
    print("\n" + "=" * 70)
    print("6. KEY TAKEAWAYS")
    print("=" * 70)
    print("\n✓ Space optimization reduces O(m×n) → O(min(m,n))")
    print("✓ Time complexity remains O(m×n) (no change)")
    print("✓ Works because we only need 2 rows at a time")
    print("✓ Can optimize further by using shorter string for columns")
    print("✓ Same algorithm, just smarter memory usage!")


def compare_approaches():
    """Compare full 2D table vs space-optimized approach"""
    print("=" * 70)
    print("COMPARING APPROACHES")
    print("=" * 70)
    
    sol = Solution()
    test_cases = [
        ("horse", "ros"),
        ("intention", "execution"),
        ("abc", "abc"),
        ("", "abc"),
        ("kitten", "sitting"),
    ]
    
    for word1, word2 in test_cases:
        result_full = sol.minDistance(word1, word2)
        result_opt = sol.minDistance_optimized(word1, word2)
        
        m, n = len(word1), len(word2)
        space_full = (m + 1) * (n + 1)
        space_opt = 2 * (min(m, n) + 1)
        
        print(f"\nword1='{word1}' (len={m}), word2='{word2}' (len={n})")
        print(f"  Full 2D:    {result_full} (space: {space_full} cells)")
        print(f"  Optimized:  {result_opt} (space: {space_opt} cells)")
        print(f"  Match: {'✓' if result_full == result_opt else '✗'}")
        print(f"  Space saved: {space_full - space_opt} cells ({100 * (space_full - space_opt) / space_full:.1f}%)")
        assert result_full == result_opt, "Results should match!"
    
    print("\n" + "=" * 70)
    print("✓ Both approaches produce identical results!")
    print("=" * 70)


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
    
    # Compare approaches
    print("\n")
    compare_approaches()
    
    # Detailed visualization
    print("\n")
    visualize_space_optimization()
# %%

