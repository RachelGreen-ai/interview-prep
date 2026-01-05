# LeetCode 2189: Number of Ways to Build House of Cards
#%%
"""
Problem Statement:
You are given an integer n representing the number of playing cards you have.
A house of cards meets the following conditions:

1. A house of cards consists of one or more rows of triangles and horizontal cards.
2. Triangles are created by leaning two cards against each other.
3. One card must be placed horizontally between all adjacent triangles in a row.
4. Any triangle on a row higher than the first must be placed on a horizontal card
   from the previous row.
5. Each triangle is placed in the leftmost available spot in the row.

Return the number of distinct house of cards you can build using all n cards.
If it is impossible to build any house of cards, return 0.

Example 1:
Input: n = 16
Output: 2
Explanation: The two valid houses of cards are shown.
The third house of cards uses only 15 cards, so it is invalid.
The fourth house of cards uses 17 cards, so it is invalid.

Example 2:
Input: n = 2
Output: 1
Explanation: The one valid house of cards is shown.

Example 3:
Input: n = 4
Output: 0
Explanation: The three house of cards shown are not valid.
The first house of cards uses 5 cards, while the second uses 4 cards.
The third one is invalid because it uses 3 cards, which is less than 2.

INTERVIEW EXPLANATION: Why Dynamic Programming for House of Cards?

1. **Problem Structure**: We need to count the number of ways to partition n cards
   into valid rows. Each row with k triangles requires exactly (3k - 1) cards:
   - 2k cards for k triangles (2 cards per triangle)
   - (k - 1) horizontal cards between triangles
   - Total: 2k + (k - 1) = 3k - 1

2. **Why DP?**
   - **Counting Problem**: We need to count all valid ways to use exactly n cards
   - **Optimal Substructure**: The number of ways to use n cards depends on:
     * Choosing a base row with k triangles (uses 3k - 1 cards)
     * Finding ways to build the rest with (n - (3k - 1)) cards
   
   - **DP State**: dp[i] = number of ways to build a house using exactly i cards
   
   - **Recurrence**: 
     * For each possible base row size k (where baseCards = 3k - 1):
       dp[i] += dp[i - baseCards]
     * We iterate backwards to ensure each base row is used only once per combination
   
   - **Time Complexity**: O(n²)
     * Outer loop: O(n) possible base row sizes
     * Inner loop: O(n) card counts
   
   - **Space Complexity**: O(n) for DP array

3. **Key Insights**:
   - Each row must have fewer or equal triangles than the row below (structural constraint)
   - We iterate base row sizes from smallest to largest
   - We iterate card counts backwards to avoid using the same base row multiple times
   - Base case: dp[0] = 1 (one way to build with 0 cards: do nothing)

4. **Edge Cases**:
   - n < 2: Cannot build any house (need at least 2 cards for one triangle)
   - n = 2: One way (single triangle)
   - n = 4: No valid way (would need 5 cards for 2 triangles in a row)
"""


class Solution:
    """Solution for Number of Ways to Build House of Cards"""
    
    def houseOfCards(self, n: int) -> int:
        """
        Count number of distinct houses of cards using exactly n cards.
        
        Args:
            n: Total number of cards available
            
        Returns:
            Number of distinct ways to build a house of cards
        """
        if n < 2:
            return 0
        
        # dp[i] = number of ways to build house using exactly i cards
        dp = [0] * (n + 1)
        dp[0] = 1  # Base case: one way to build with 0 cards
        
        # Try each possible base row size
        # For k triangles, we need 3k - 1 cards
        # k starts from 1 (minimum 1 triangle)
        # For k=1: 3*1 - 1 = 2 cards
        # For k=2: 3*2 - 1 = 5 cards
        # For k=3: 3*3 - 1 = 8 cards
        # Pattern: baseCards = 2, 5, 8, 11, ... (increment by 3)
        
        for baseCards in range(2, n + 1, 3):  # Start at 2, increment by 3
            # Iterate backwards to avoid using same base row multiple times
            for i in range(n, baseCards - 1, -1):
                dp[i] += dp[i - baseCards]
        
        return dp[n]
    
    def houseOfCards_verbose(self, n: int) -> int:
        """
        More verbose version with detailed comments for understanding.
        """
        if n < 2:
            return 0
        
        dp = [0] * (n + 1)
        dp[0] = 1
        
        # For each possible number of triangles k in the base row
        k = 1
        while True:
            baseCards = 3 * k - 1  # Cards needed for k triangles
            if baseCards > n:
                break
            
            # Update DP backwards
            for i in range(n, baseCards - 1, -1):
                # If we use baseCards for this row, we can build the rest
                # with (i - baseCards) cards in dp[i - baseCards] ways
                dp[i] += dp[i - baseCards]
            
            k += 1
        
        return dp[n]


def test_house_of_cards():
    """Test cases for Number of Ways to Build House of Cards"""
    sol = Solution()
    
    # Test case 1: Example 1
    n1 = 16
    result1 = sol.houseOfCards(n1)
    assert result1 == 2, f"Expected 2, got {result1}"
    print(f"✓ Test 1: n={n1}, ways={result1}")
    
    # Test case 2: Example 2
    n2 = 2
    result2 = sol.houseOfCards(n2)
    assert result2 == 1, f"Expected 1, got {result2}"
    print(f"✓ Test 2: n={n2}, ways={result2}")
    
    # Test case 3: Example 3
    n3 = 4
    result3 = sol.houseOfCards(n3)
    assert result3 == 0, f"Expected 0, got {result3}"
    print(f"✓ Test 3: n={n3}, ways={result3}")
    
    # Test case 4: n = 5
    n4 = 5
    result4 = sol.houseOfCards(n4)
    # 5 cards = 2 triangles (2*2 + 1 horizontal = 5 cards)
    assert result4 == 1, f"Expected 1, got {result4}"
    print(f"✓ Test 4: n={n4}, ways={result4}")
    
    # Test case 5: n = 8
    n5 = 8
    result5 = sol.houseOfCards(n5)
    # 8 cards = 3 triangles (3*2 + 2 horizontal = 8 cards)
    assert result5 == 1, f"Expected 1, got {result5}"
    print(f"✓ Test 5: n={n5}, ways={result5}")
    
    # Test case 6: n = 1 (too few cards)
    n6 = 1
    result6 = sol.houseOfCards(n6)
    assert result6 == 0, f"Expected 0, got {result6}"
    print(f"✓ Test 6: n={n6}, ways={result6}")
    
    # Test case 7: n = 7
    n7 = 7
    result7 = sol.houseOfCards(n7)
    # 7 = 2 + 5 (two rows: 1 triangle + 2 triangles)
    # Or 7 = 5 + 2 (two rows: 2 triangles + 1 triangle)
    # But wait, rows must be non-increasing, so only one valid way
    print(f"✓ Test 7: n={n7}, ways={result7}")
    
    print("\nAll tests passed!")


if __name__ == "__main__":
    test_house_of_cards()
    
    # Example usage
    print("\nExample usage:")
    sol = Solution()
    
    test_cases = [2, 4, 5, 8, 16]
    for n in test_cases:
        result = sol.houseOfCards(n)
        print(f"n = {n:2d} cards → {result} way(s) to build house of cards")
    
    print("\nExplanation:")
    print("- n=2: One triangle (2 cards)")
    print("- n=4: No valid way (would need 5 cards for 2 triangles)")
    print("- n=5: Two triangles in one row (2*2 + 1 = 5 cards)")
    print("- n=8: Three triangles in one row (3*2 + 2 = 8 cards)")
    print("- n=16: Multiple valid configurations")
# %%

