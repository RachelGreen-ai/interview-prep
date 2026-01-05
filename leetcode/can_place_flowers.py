# LeetCode 605: Can Place Flowers
#%%
"""
Problem Statement:
You have a long flowerbed in which some of the plots are planted, and some are not.
However, flowers cannot be planted in adjacent plots.

Given an integer array flowerbed containing 0's and 1's, where 0 means empty and 1 means
not empty, and an integer n, return true if n new flowers can be planted in the flowerbed
without violating the no-adjacent-flowers rule and false otherwise.

Example 1:
Input: flowerbed = [1,0,0,0,1], n = 1
Output: true

Example 2:
Input: flowerbed = [1,0,0,0,1], n = 2
Output: false

INTERVIEW EXPLANATION: Why Greedy for Can Place Flowers?

1. **Problem Structure**: We need to place as many flowers as possible following the rule:
   no two flowers can be adjacent. This is a greedy problem where we place flowers
   as early as possible.

2. **Why Greedy?**
   - **Local Optimal**: If we can place a flower at position i, we should (greedy choice)
   - **No Future Dependencies**: Placing a flower early doesn't prevent better solutions
   - **Simple Rule**: Check if current position and neighbors are empty, then place

3. **Algorithm**:
   a. Iterate through flowerbed
   b. For each position i:
      - Check if flowerbed[i] is 0 (empty)
      - Check if left neighbor (i-1) is empty or doesn't exist
      - Check if right neighbor (i+1) is empty or doesn't exist
      - If all conditions met, place flower (set to 1) and decrement n
   c. Return true if n <= 0 (placed all required flowers)

4. **Key Insights**:
   - Greedy: place flower as early as possible
   - Check boundaries (first and last positions)
   - After placing, we can skip next position (it's adjacent)

5. **Time Complexity**: O(n) where n is length of flowerbed
   
6. **Space Complexity**: O(1) - modifying input array in place
"""


class Solution:
    """Solution for Can Place Flowers"""
    
    def canPlaceFlowers(self, flowerbed: list[int], n: int) -> bool:
        """
        Check if n flowers can be placed without adjacent rule violation.
        
        Args:
            flowerbed: Array of 0s and 1s (0 = empty, 1 = planted)
            n: Number of flowers to place
            
        Returns:
            True if n flowers can be placed, False otherwise
        """
        if n == 0:
            return True
        
        count = 0
        length = len(flowerbed)
        
        for i in range(length):
            # Check if current position is empty
            if flowerbed[i] == 0:
                # Check left neighbor
                left_empty = (i == 0) or (flowerbed[i - 1] == 0)
                # Check right neighbor
                right_empty = (i == length - 1) or (flowerbed[i + 1] == 0)
                
                # If both neighbors are empty, we can place a flower
                if left_empty and right_empty:
                    flowerbed[i] = 1
                    count += 1
                    if count >= n:
                        return True
        
        return count >= n
    
    def canPlaceFlowers_optimized(self, flowerbed: list[int], n: int) -> bool:
        """
        Optimized version that skips positions after placing.
        """
        if n == 0:
            return True
        
        count = 0
        i = 0
        length = len(flowerbed)
        
        while i < length:
            if flowerbed[i] == 0:
                # Check if we can place here
                prev_empty = (i == 0) or (flowerbed[i - 1] == 0)
                next_empty = (i == length - 1) or (flowerbed[i + 1] == 0)
                
                if prev_empty and next_empty:
                    flowerbed[i] = 1
                    count += 1
                    if count >= n:
                        return True
                    i += 2  # Skip next position (adjacent)
                else:
                    i += 1
            else:
                i += 2  # Skip next position if current is planted
        
        return count >= n


def test_can_place_flowers():
    """Test cases for Can Place Flowers"""
    sol = Solution()
    
    # Test case 1: Example 1
    flowerbed1 = [1,0,0,0,1]
    result1 = sol.canPlaceFlowers(flowerbed1[:], 1)
    assert result1 == True, f"Expected True, got {result1}"
    print(f"✓ Test 1: flowerbed={[1,0,0,0,1]}, n=1")
    print(f"  Result: {result1}")
    
    # Test case 2: Example 2
    flowerbed2 = [1,0,0,0,1]
    result2 = sol.canPlaceFlowers(flowerbed2[:], 2)
    assert result2 == False, f"Expected False, got {result2}"
    print(f"✓ Test 2: flowerbed={[1,0,0,0,1]}, n=2")
    print(f"  Result: {result2}")
    
    # Test case 3: Empty flowerbed
    flowerbed3 = [0,0,0]
    result3 = sol.canPlaceFlowers(flowerbed3[:], 2)
    assert result3 == True, f"Expected True, got {result3}"
    print(f"✓ Test 3: All empty, n=2")
    print(f"  Result: {result3}")
    
    # Test case 4: No flowers needed
    flowerbed4 = [1,0,1]
    result4 = sol.canPlaceFlowers(flowerbed4[:], 0)
    assert result4 == True, f"Expected True, got {result4}"
    print(f"✓ Test 4: n=0")
    print(f"  Result: {result4}")
    
    # Test case 5: Single position
    flowerbed5 = [0]
    result5 = sol.canPlaceFlowers(flowerbed5[:], 1)
    assert result5 == True, f"Expected True, got {result5}"
    print(f"✓ Test 5: Single empty position")
    print(f"  Result: {result5}")
    
    print("\nAll tests passed!")


if __name__ == "__main__":
    test_can_place_flowers()
    
    # Example usage
    print("\nExample usage:")
    sol = Solution()
    
    flowerbed = [1,0,0,0,1]
    n = 1
    result = sol.canPlaceFlowers(flowerbed[:], n)
    print(f"Flowerbed: {flowerbed}")
    print(f"Can place {n} flowers: {result}")
# %%

