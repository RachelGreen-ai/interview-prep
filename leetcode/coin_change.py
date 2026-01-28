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
        Bottom-up DP - NO MEMOIZATION NEEDED!
        
        WHY BOTTOM-UP DOESN'T NEED MEMOIZATION:
        ---------------------------------------
        - Start with BASE CASE: amount = 0 (0 coins needed)
        - Build UP to full solution: 0 → 1 → 2 → ... → amount
        - Solve each subproblem exactly ONCE, in order
        - No overlapping subproblems: dp[5] computed once, stored, used later
        
        ITERATIVE STRUCTURE:
        - dp[0] = 0 (base case)
        - dp[1] = min(1 + dp[0]) = 1
        - dp[2] = min(1 + dp[1], 1 + dp[0]) = 2
        - dp[3] = min(1 + dp[2], 1 + dp[1]) = 2
        - ...
        - dp[11] = min(1 + dp[10], 1 + dp[9], 1 + dp[6]) = 3
        
        KEY DIFFERENCE:
        - Top-down: Multiple paths → same subproblem → NEEDS memoization
        - Bottom-up: Single path, each amount computed once → NO memoization needed
        
        Example with amount=11, coins=[1,2,5]:
        dp[0] = 0  ← computed once
        dp[1] = 1  ← computed once (uses dp[0])
        dp[2] = 1  ← computed once (uses dp[0], dp[1])
        ...
        dp[5] = 1  ← computed once (uses dp[0], dp[3], dp[4])
        ...
        dp[11] = 3 ← computed once (uses dp[6], dp[9], dp[10])
        
        Each dp[i] is computed exactly ONCE, in order!
        
        Args:
            coins: Array of coin denominations
            amount: Target amount
            
        Returns:
            Minimum coins needed, or -1 if impossible
        """
        # DP: dp[i] = minimum coins to make amount i
        dp = [float('inf')] * (amount + 1)
        dp[0] = 0  # Base case: 0 coins for amount 0
        
        # Build solution bottom-up: solve smaller amounts first
        for i in range(1, amount + 1):
            for coin in coins:
                if coin <= i:
                    # Try using this coin: 1 coin + minimum for remaining amount
                    dp[i] = min(dp[i], 1 + dp[i - coin])
        
        return dp[amount] if dp[amount] != float('inf') else -1
    
    def coinChange_topdown(self, coins: list[int], amount: int) -> int:
        """
        Top-down DP with memoization.
        
        WHY TOP-DOWN NEEDS MEMOIZATION:
        --------------------------------
        - Start with FULL problem: amount = 11
        - Break down into SMALLER subproblems: 11 → 10, 9, 6 (trying coins 1, 2, 5)
        - Recurse DOWN: 11 → 10 → 9 → 8 → ... → 0 (base case)
        
        OVERLAPPING SUBPROBLEMS:
        - amount=5 might be computed from multiple paths:
          * 11 → 10 → 9 → 8 → 7 → 6 → 5
          * 11 → 9 → 7 → 5
          * 11 → 6 → 5
        - Without memoization: Exponential recomputation (O(2^n))
        - With @lru_cache: Each amount computed ONCE (O(amount * coins))
        
        Example call tree (without memoization):
        dfs(11)
          ├─ dfs(10)  ← amount=10 computed
          │   ├─ dfs(9)
          │   │   └─ dfs(8) → ... → dfs(5)  ← amount=5 computed
          │   └─ dfs(8) → ... → dfs(5)  ← amount=5 computed AGAIN!
          ├─ dfs(9)
          │   └─ dfs(7) → ... → dfs(5)  ← amount=5 computed AGAIN!
          └─ dfs(6)
              └─ dfs(5)  ← amount=5 computed AGAIN!
        
        With memoization: dfs(5) computed ONCE, cached, reused!
        """
        from functools import lru_cache
        
        @lru_cache(maxsize=None)  # MEMOIZATION IS ESSENTIAL!
        def dfs(remaining: int) -> int:
            # Base case: exact amount reached
            if remaining == 0:
                return 0
            # Invalid: negative amount
            if remaining < 0:
                return float('inf')
            
            # Try each coin, take minimum
            min_coins = float('inf')
            for coin in coins:
                result = dfs(remaining - coin)  # Recursive call to smaller subproblem
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


def explain_top_down_vs_bottom_up_coin_change():
    """
    Comprehensive explanation of Top-Down vs Bottom-Up for Coin Change.
    This problem PERFECTLY demonstrates why top-down needs memoization but bottom-up doesn't.
    """
    print("=" * 70)
    print("TOP-DOWN vs BOTTOM-UP: Coin Change Example")
    print("=" * 70)
    
    coins = [1, 2, 5]
    amount = 11
    
    print(f"\nProblem: coins={coins}, amount={amount}")
    print(f"Answer: 3 coins (5 + 5 + 1)")
    
    print("\n" + "=" * 70)
    print("1. TOP-DOWN DFS (with memoization)")
    print("=" * 70)
    print("\nDirection: Full problem → Base case")
    print("  Start: amount = 11 (full problem)")
    print("  Break down: 11 → try coins → 10, 9, 6 (smaller subproblems)")
    print("  Recurse: 11 → 10 → 9 → 8 → ... → 0 (base case)")
    print("  Base case: amount = 0 (0 coins needed)")
    
    print("\nCall Tree (showing overlapping subproblems):")
    print("  dfs(11)")
    print("    ├─ dfs(10)  [amount=10 computed]")
    print("    │   ├─ dfs(9)")
    print("    │   │   └─ ... → dfs(5)  [amount=5 computed]")
    print("    │   └─ ... → dfs(5)  [amount=5 computed AGAIN!]")
    print("    ├─ dfs(9)")
    print("    │   └─ ... → dfs(5)  [amount=5 computed AGAIN!]")
    print("    └─ dfs(6)")
    print("        └─ dfs(5)  [amount=5 computed AGAIN!]")
    
    print("\nWHY MEMOIZATION IS NEEDED:")
    print("  ✗ Without memoization: amount=5 computed 4+ times → O(2^n) time!")
    print("  ✓ With @lru_cache: amount=5 computed ONCE, cached, reused → O(amount*coins)")
    print("  → Memoization prevents exponential recomputation")
    
    print("\n" + "=" * 70)
    print("2. BOTTOM-UP DP (no memoization needed)")
    print("=" * 70)
    print("\nDirection: Base case → Full problem")
    print("  Start: amount = 0 (base case, 0 coins)")
    print("  Build up: 0 → 1 → 2 → 3 → ... → 11 (full solution)")
    print("  Each amount computed exactly ONCE, in order")
    
    print("\nDP Table Construction:")
    print("  dp[0] = 0  ← Base case (computed once)")
    print("  dp[1] = 1  ← Uses dp[0] (computed once)")
    print("  dp[2] = 1  ← Uses dp[0], dp[1] (computed once)")
    print("  dp[3] = 2  ← Uses dp[1], dp[2] (computed once)")
    print("  dp[4] = 2  ← Uses dp[2], dp[3] (computed once)")
    print("  dp[5] = 1  ← Uses dp[0], dp[3], dp[4] (computed ONCE)")
    print("  ...")
    print("  dp[11] = 3 ← Uses dp[6], dp[9], dp[10] (computed once)")
    
    print("\nWHY NO MEMOIZATION NEEDED:")
    print("  ✓ Each dp[i] computed exactly ONCE, in order")
    print("  ✓ No overlapping subproblems (we iterate sequentially)")
    print("  ✓ dp[i] depends only on previously computed values")
    print("  ✓ DP table stores results, but no cache lookup needed")
    print("  → Natural structure avoids recomputation")
    
    print("\n" + "=" * 70)
    print("3. SIDE-BY-SIDE COMPARISON")
    print("=" * 70)
    print("\n┌─────────────────────┬──────────────────────┬──────────────────────┐")
    print("│ Aspect              │ Top-Down DFS         │ Bottom-Up DP         │")
    print("├─────────────────────┼──────────────────────┼──────────────────────┤")
    print("│ Direction           │ 11 → 10 → ... → 0   │ 0 → 1 → ... → 11   │")
    print("│ Structure           │ Recursive            │ Iterative            │")
    print("│ Starting Point     │ Full problem (11)    │ Base case (0)        │")
    print("│ Subproblems         │ Can overlap          │ Solved once          │")
    print("│ Memoization         │ NEEDED ✓             │ NOT NEEDED ✗         │")
    print("│ Storage             │ Cache + Stack        │ DP table only        │")
    print("│ Time (with memo)    │ O(amount × coins)   │ O(amount × coins)    │")
    print("│ Time (without memo) │ O(2^amount) ✗        │ O(amount × coins) ✓  │")
    print("│ Space               │ O(amount) cache      │ O(amount) DP table   │")
    print("│ Natural fit         │ Recursive thinking   │ Iterative thinking   │")
    print("└─────────────────────┴──────────────────────┴──────────────────────┘")
    
    print("\n" + "=" * 70)
    print("4. KEY INSIGHT")
    print("=" * 70)
    print("\nTop-Down:")
    print("  - Natural recursive thinking: 'To solve amount=11, try each coin...'")
    print("  - Multiple paths can reach same subproblem (amount=5)")
    print("  - MEMOIZATION IS ESSENTIAL to avoid exponential time")
    print("\nBottom-Up:")
    print("  - Natural iterative thinking: 'Start from 0, build up to 11...'")
    print("  - Each subproblem solved exactly once, in order")
    print("  - NO MEMOIZATION NEEDED - structure prevents recomputation")
    print("\nBoth are correct! Choose based on:")
    print("  - Top-Down: Easier to think recursively, but needs memoization")
    print("  - Bottom-Up: More structured, naturally efficient, no memoization")


def compare_implementations():
    """Compare top-down and bottom-up implementations"""
    print("=" * 70)
    print("COMPARING IMPLEMENTATIONS")
    print("=" * 70)
    
    sol = Solution()
    test_cases = [
        ([1, 2, 5], 11),
        ([2], 3),
        ([1], 0),
        ([1, 3, 4], 6),
    ]
    
    for coins, amount in test_cases:
        result_bottom_up = sol.coinChange(coins, amount)
        result_top_down = sol.coinChange_topdown(coins, amount)
        
        print(f"\ncoins={coins}, amount={amount}")
        print(f"  Bottom-Up: {result_bottom_up}")
        print(f"  Top-Down:  {result_top_down}")
        print(f"  Match: {'✓' if result_bottom_up == result_top_down else '✗'}")
        assert result_bottom_up == result_top_down, "Results don't match!"
    
    print("\n✓ Both implementations produce identical results!")


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
    
    # Compare implementations
    print("\n")
    compare_implementations()
    
    # Detailed explanation
    print("\n")
    explain_top_down_vs_bottom_up_coin_change()
# %%

