# LeetCode 638: Shopping Offers
#%%
"""
Problem Statement:
In LeetCode Store, there are n items to sell. Each item has a price. However, there are some
special offers, and a special offer consists of one or more different kinds of items with
a sale price.

You are given an integer array price where price[i] is the price of the ith item, and an
integer array needs where needs[i] is the number of pieces of the ith item you want to buy.

You are also given an array special where special[i] is of size n + 1 where special[i][j]
is the number of pieces of the jth item in the ith offer and the last integer is the price
of the ith offer.

Return the lowest price you have to pay for exactly certain items as given, where you could
make optimal use of the special offers. You are not allowed to buy more items than you want,
even if that would lower the overall price.

Example 1:
Input: price = [2,5], special = [[3,0,5],[1,2,10]], needs = [3,2]
Output: 14
Explanation: There are two kinds of items, A and B. Their prices are $2 and $5 respectively.
In special offer 1, you can pay $5 for 3A and 0B
In special offer 2, you can pay $10 for 1A and 2B.
You need to buy 3A and 2B, so you may pay $10 for 1A and 2B (special offer 2), and $4 for 2A.

Example 2:
Input: price = [2,3,4], special = [[1,1,0,4],[1,2,1,9]], needs = [1,2,1]
Output: 11
Explanation: The price of A is $2, and $3 for B, $4 for C.
You may pay $4 for 1A and 1B, and $9 for 1A, 2B and 1C.
You need to buy 1A, 2B, and 1C, so you may pay $4 for 1A and 1B (special offer 1), and $3 for 1B, and $4 for 1C.
You cannot add more items, though buying only 1A and 1B would be cheaper.

INTERVIEW EXPLANATION: Why DFS/Backtracking with Memoization for Shopping Offers?

1. **Problem Structure**: We need to find the minimum cost to buy exactly the needed items,
   using special offers or regular prices. This is a combinatorial optimization problem.

2. **Why DFS with Memoization?**
   - **Decision Tree**: For each offer, decide whether to use it or not
   - **State Space**: Current needs vector represents the state
   - **Overlapping Subproblems**: Same needs vector can be reached multiple ways
   - **Memoization**: Cache results for each needs state to avoid recomputation

3. **Algorithm**:
   a. Base case: If all needs are 0, cost is 0
   b. Calculate cost without any offers (buy all at regular price)
   c. For each special offer:
      - Check if offer is valid (doesn't exceed needs)
      - Apply offer: subtract offer items from needs
      - Recursively solve for remaining needs
      - Add offer price to recursive result
   d. Return minimum of all options

4. **Key Insights**:
   - Try all combinations of special offers
   - Use memoization to cache results for each needs state
   - Filter out bad offers (more expensive than regular price)
   - Early pruning: if offer exceeds needs, skip it

5. **Time Complexity**: O(2^m * n) where m is number of offers, n is number of items
   - In worst case, try all combinations of offers
   - Memoization reduces redundant computations
   
6. **Space Complexity**: O(n * product(needs)) for memoization
"""

from functools import lru_cache


class Solution:
    """Solution for Shopping Offers"""
    
    def shoppingOffers(self, price: list[int], special: list[list[int]], needs: list[int]) -> int:
        """
        Find minimum cost to buy exactly the needed items.
        
        Args:
            price: Regular price for each item
            special: List of special offers [item1, item2, ..., price]
            needs: Required quantity for each item
            
        Returns:
            Minimum cost to buy all needed items
        """
        n = len(price)
        
        # Filter out bad offers (more expensive than regular price)
        valid_special = []
        for offer in special:
            # Check if offer is actually beneficial
            regular_cost = sum(offer[i] * price[i] for i in range(n))
            if offer[-1] < regular_cost:
                valid_special.append(offer)
        
        @lru_cache(maxsize=None)
        def dfs(current_needs: tuple) -> int:
            """
            Find minimum cost for current needs.
            
            Args:
                current_needs: Tuple of remaining needs
                
            Returns:
                Minimum cost
            """
            # Base case: all needs satisfied
            if all(need == 0 for need in current_needs):
                return 0
            
            # Calculate cost without any offers
            cost = sum(current_needs[i] * price[i] for i in range(n))
            
            # Try each special offer
            for offer in valid_special:
                # Check if offer is valid (doesn't exceed needs)
                new_needs = list(current_needs)
                valid = True
                
                for i in range(n):
                    if offer[i] > new_needs[i]:
                        valid = False
                        break
                    new_needs[i] -= offer[i]
                
                if valid:
                    # Apply offer and recurse
                    new_cost = offer[-1] + dfs(tuple(new_needs))
                    cost = min(cost, new_cost)
            
            return cost
        
        return dfs(tuple(needs))
    
    def shoppingOffers_optimized(self, price: list[int], special: list[list[int]], needs: list[int]) -> int:
        """
        Optimized version with better pruning.
        """
        n = len(price)
        
        # Filter and sort offers
        valid_special = []
        for offer in special:
            regular_cost = sum(offer[i] * price[i] for i in range(n))
            if offer[-1] < regular_cost:
                valid_special.append(offer)
        
        memo = {}
        
        def dfs(current_needs: tuple) -> int:
            if current_needs in memo:
                return memo[current_needs]
            
            # Base case
            if all(need == 0 for need in current_needs):
                return 0
            
            # Cost without offers
            cost = sum(current_needs[i] * price[i] for i in range(n))
            
            # Try each offer
            for offer in valid_special:
                new_needs = []
                valid = True
                
                for i in range(n):
                    if offer[i] > current_needs[i]:
                        valid = False
                        break
                    new_needs.append(current_needs[i] - offer[i])
                
                if valid:
                    cost = min(cost, offer[-1] + dfs(tuple(new_needs)))
            
            memo[current_needs] = cost
            return cost
        
        return dfs(tuple(needs))


def test_shopping_offers():
    """Test cases for Shopping Offers"""
    sol = Solution()
    
    # Test case 1: Example 1
    price1 = [2,5]
    special1 = [[3,0,5],[1,2,10]]
    needs1 = [3,2]
    result1 = sol.shoppingOffers(price1, special1, needs1)
    assert result1 == 14, f"Expected 14, got {result1}"
    print(f"✓ Test 1: price={price1}, needs={needs1}")
    print(f"  Result: ${result1}")
    
    # Test case 2: Example 2
    price2 = [2,3,4]
    special2 = [[1,1,0,4],[1,2,1,9]]
    needs2 = [1,2,1]
    result2 = sol.shoppingOffers(price2, special2, needs2)
    assert result2 == 11, f"Expected 11, got {result2}"
    print(f"✓ Test 2: price={price2}, needs={needs2}")
    print(f"  Result: ${result2}")
    
    # Test case 3: No special offers
    price3 = [2,3]
    special3 = []
    needs3 = [1,1]
    result3 = sol.shoppingOffers(price3, special3, needs3)
    assert result3 == 5, f"Expected 5, got {result3}"
    print(f"✓ Test 3: No special offers")
    print(f"  Result: ${result3}")
    
    # Test case 4: Special offer is worse
    price4 = [2,3]
    special4 = [[1,1,10]]  # More expensive than regular
    needs4 = [1,1]
    result4 = sol.shoppingOffers(price4, special4, needs4)
    assert result4 == 5, f"Expected 5, got {result4}"
    print(f"✓ Test 4: Bad special offer filtered out")
    print(f"  Result: ${result4}")
    
    print("\nAll tests passed!")


if __name__ == "__main__":
    test_shopping_offers()
    
    # Example usage
    print("\nExample usage:")
    sol = Solution()
    
    price = [2,5]
    special = [[3,0,5],[1,2,10]]
    needs = [3,2]
    result = sol.shoppingOffers(price, special, needs)
    print(f"Prices: {price}")
    print(f"Needs: {needs}")
    print(f"Minimum cost: ${result}")
# %%

