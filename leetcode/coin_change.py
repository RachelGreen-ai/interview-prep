# LeetCode 322: Coin Change
#%%
"""
Problem Statement:
You are given an integer array coins representing coins of different denominations and an
integer amount representing a total amount of money.

Return the fewest number of coins that you need to make up that amount. If that amount of
money cannot be made up by any combination of the coins, return -1.

You may assume that you have an infinite number of each kind of coin.

Example 1:
Input: coins = [1,2,5], amount = 11
Output: 3
Explanation: 11 = 5 + 5 + 1

Example 2:
Input: coins = [2], amount = 3
Output: -1

Example 3:
Input: coins = [1], amount = 0
Output: 0

INTERVIEW EXPLANATION: Why Dynamic Programming for Coin Change?

1. **Problem Structure**: We need to find minimum number of coins to make amount.
   This is an optimization problem with overlapping subproblems.

2. **Why Dynamic Programming?**
   - **Optimal Substructure**: Minimum coins for amount = 1 + min(coins for amount - coin)
   - **Overlapping Subproblems**: Same sub-amounts computed multiple times
   - **Bottom-Up**: Build solution from 0 to amount
   - **Memoization**: Cache results for each amount

3. **Algorithm**:
   a. dp[i] = minimum coins needed to make amount i
   b. Initialize: dp[0] = 0, dp[i] = infinity for i > 0
   c. For each amount from 1 to target:
      - For each coin:
        - If coin <= amount:
          - dp[amount] = min(dp[amount], 1 + dp[amount - coin])
   d. Return dp[amount] if it's not infinity, else -1

4. **Key Insights**:
   - Bottom-up DP: solve smaller amounts first
   - Try each coin and take minimum
   - Initialize with infinity to represent "impossible"

5. **Time Complexity**: O(amount * len(coins))
   
6. **Space Complexity**: O(amount) for DP array
"""


class Solution:
    """Solution for Coin Change"""
    
    def coinChange(self, coins: list[int], amount: int) -> int:
        """
        Find fewest number of coins to make amount.
        
        Args:
            coins: Array of coin denominations
            amount: Target amount
            
        Returns:
            Minimum coins needed, or -1 if impossible
        """
        # DP: dp[i] = minimum coins to make amount i
        dp = [float('inf')] * (amount + 1)
        dp[0] = 0  # Base case: 0 coins for amount 0
        
        # Build solution bottom-up
        for i in range(1, amount + 1):
            for coin in coins:
                if coin <= i:
                    dp[i] = min(dp[i], 1 + dp[i - coin])
        
        return dp[amount] if dp[amount] != float('inf') else -1
    
    def coinChange_topdown(self, coins: list[int], amount: int) -> int:
        """
        Top-down DP with memoization.
        """
        from functools import lru_cache
        
        @lru_cache(maxsize=None)
        def dfs(remaining: int) -> int:
            if remaining == 0:
                return 0
            if remaining < 0:
                return float('inf')
            
            min_coins = float('inf')
            for coin in coins:
                result = dfs(remaining - coin)
                min_coins = min(min_coins, 1 + result)
            
            return min_coins
        
        result = dfs(amount)
        return result if result != float('inf') else -1
    
    def coinChange_optimized(self, coins: list[int], amount: int) -> int:
        """
        Optimized version with early termination.
        """
        dp = [float('inf')] * (amount + 1)
        dp[0] = 0
        
        # Sort coins for potential optimization
        coins.sort()
        
        for i in range(1, amount + 1):
            for coin in coins:
                if coin > i:
                    break  # Coins are sorted, can break early
                dp[i] = min(dp[i], 1 + dp[i - coin])
        
        return dp[amount] if dp[amount] != float('inf') else -1


def test_coin_change():
    """Test cases for Coin Change"""
    sol = Solution()
    
    # Test case 1: Example 1
    coins1 = [1,2,5]
    amount1 = 11
    result1 = sol.coinChange(coins1, amount1)
    assert result1 == 3, f"Expected 3, got {result1}"
    print(f"✓ Test 1: coins={coins1}, amount={amount1} -> {result1}")
    
    # Test case 2: Example 2
    coins2 = [2]
    amount2 = 3
    result2 = sol.coinChange(coins2, amount2)
    assert result2 == -1, f"Expected -1, got {result2}"
    print(f"✓ Test 2: coins={coins2}, amount={amount2} -> {result2}")
    
    # Test case 3: Example 3
    coins3 = [1]
    amount3 = 0
    result3 = sol.coinChange(coins3, amount3)
    assert result3 == 0, f"Expected 0, got {result3}"
    print(f"✓ Test 3: coins={coins3}, amount={amount3} -> {result3}")
    
    # Test case 4: Single coin
    coins4 = [1]
    amount4 = 2
    result4 = sol.coinChange(coins4, amount4)
    assert result4 == 2, f"Expected 2, got {result4}"
    print(f"✓ Test 4: Single coin")
    print(f"  Result: {result4}")
    
    # Test case 5: Large amount
    coins5 = [1,3,4]
    amount5 = 6
    result5 = sol.coinChange(coins5, amount5)
    assert result5 == 2, f"Expected 2, got {result5}"  # 3 + 3
    print(f"✓ Test 5: coins={coins5}, amount={amount5} -> {result5}")
    
    print("\nAll tests passed!")


if __name__ == "__main__":
    test_coin_change()
    
    # Example usage
    print("\nExample usage:")
    sol = Solution()
    
    coins = [1,2,5]
    amount = 11
    result = sol.coinChange(coins, amount)
    print(f"Coins: {coins}")
    print(f"Amount: {amount}")
    print(f"Minimum coins needed: {result}")
# %%

