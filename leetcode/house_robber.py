# LeetCode 198: House Robber
#%%
"""
Problem Statement:
You are a professional robber planning to rob houses along a street. Each house
has a certain amount of money stashed. The only constraint stopping you from
robbing each of them is that adjacent houses have security systems connected and
it will automatically contact the police if two adjacent houses were broken
into on the same night.

Given an integer array nums representing the amount of money of each house,
return the maximum amount of money you can rob tonight without alerting the police.

Example 1:
Input: nums = [1,2,3,1]
Output: 4
Explanation: Rob house 1 (money = 1) and then rob house 3 (money = 3).
Total amount you can rob = 1 + 3 = 4.

Example 2:
Input: nums = [2,7,9,3,1]
Output: 12
Explanation: Rob house 1 (money = 2), rob house 3 (money = 9) and rob house 5 (money = 1).
Total amount you can rob = 2 + 9 + 1 = 12.

INTERVIEW EXPLANATION: Why Dynamic Programming for House Robber?

1. **Problem Structure**: At each house i, we have two choices:
   - Rob house i → cannot rob house i-1, so profit = nums[i] + dp[i-2]
   - Skip house i → can rob house i-1, so profit = dp[i-1]
   
   We want to maximize profit, so: dp[i] = max(dp[i-1], dp[i-2] + nums[i])

2. **Why DP?**
   - **Optimal Substructure**: The maximum profit up to house i depends on
     optimal solutions for houses i-1 and i-2. We can build up the solution
     from smaller subproblems.
   
   - **Overlapping Subproblems**: When computing dp[i], we reuse dp[i-1] and
     dp[i-2] which were computed earlier. DP avoids recomputation.
   
   - **Time Complexity**: O(n) - single pass through houses
   - **Space Complexity**: O(1) - can optimize to use only two variables

3. **Key Insight**: We don't need to store the entire dp array. Since we only
   need dp[i-1] and dp[i-2], we can use two variables (prev1, prev2) to
   achieve O(1) space complexity.

4. **Base Cases**:
   - dp[0] = nums[0] (only one house)
   - dp[1] = max(nums[0], nums[1]) (two houses - rob the better one)
"""

from typing import List


class Solution:
    """Solution for House Robber problem"""
    
    def rob(self, nums: List[int]) -> int:
        """
        Find maximum amount of money that can be robbed.
        
        Args:
            nums: List of money in each house
            
        Returns:
            Maximum amount that can be robbed
        """
        if not nums:
            return 0
        if len(nums) == 1:
            return nums[0]
        
        # Base cases
        prev2 = nums[0]  # dp[i-2]
        prev1 = max(nums[0], nums[1])  # dp[i-1]
        
        # Build up solution
        for i in range(2, len(nums)):
            # At house i: max(rob it, skip it)
            curr = max(prev1, prev2 + nums[i])
            prev2, prev1 = prev1, curr
        
        return prev1


def test_house_robber():
    """Test cases for House Robber"""
    sol = Solution()
    
    # Test case 1: Example 1
    nums1 = [1, 2, 3, 1]
    result1 = sol.rob(nums1)
    assert result1 == 4, f"Expected 4, got {result1}"
    print(f"✓ Test 1: {nums1} → {result1}")
    
    # Test case 2: Example 2
    nums2 = [2, 7, 9, 3, 1]
    result2 = sol.rob(nums2)
    assert result2 == 12, f"Expected 12, got {result2}"
    print(f"✓ Test 2: {nums2} → {result2}")
    
    # Test case 3: Single house
    nums3 = [5]
    result3 = sol.rob(nums3)
    assert result3 == 5, f"Expected 5, got {result3}"
    print(f"✓ Test 3: {nums3} → {result3}")
    
    # Test case 4: Two houses
    nums4 = [2, 1]
    result4 = sol.rob(nums4)
    assert result4 == 2, f"Expected 2, got {result4}"
    print(f"✓ Test 4: {nums4} → {result4}")
    
    # Test case 5: All houses
    nums5 = [1, 3, 1, 3, 1]
    result5 = sol.rob(nums5)
    assert result5 == 6, f"Expected 6, got {result5}"  # Rob houses 1, 3, 5
    print(f"✓ Test 5: {nums5} → {result5}")
    
    # Test case 6: Empty list
    nums6 = []
    result6 = sol.rob(nums6)
    assert result6 == 0, f"Expected 0, got {result6}"
    print("✓ Test 6: Empty list → 0")
    
    print("\nAll tests passed!")


if __name__ == "__main__":
    test_house_robber()
    
    # Example usage
    print("\nExample usage:")
    sol = Solution()
    nums = [2, 7, 9, 3, 1]
    result = sol.rob(nums)
    print(f"Input: {nums}")
    print(f"Maximum amount: {result}")
    print("Explanation: Rob houses at indices 0, 2, 4 → 2 + 9 + 1 = 12")
# %%

