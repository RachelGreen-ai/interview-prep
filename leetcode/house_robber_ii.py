# LeetCode 213: House Robber II
#%%
"""
Problem Statement:
You are a professional robber planning to rob houses along a street. Each house
has a certain amount of money stashed. All houses at this place are arranged
in a circle. That means the first house is the neighbor of the last one.

The constraint is the same: adjacent houses have security systems connected and
it will automatically contact the police if two adjacent houses were broken into
on the same night.

Given an integer array nums representing the amount of money of each house,
return the maximum amount of money you can rob tonight without alerting the police.

Example 1:
Input: nums = [2,3,2]
Output: 3
Explanation: You cannot rob house 1 (money = 2) and then rob house 3 (money = 2),
because they are adjacent. Rob house 2 (money = 3).

Example 2:
Input: nums = [1,2,3,1]
Output: 4
Explanation: Rob house 1 (money = 1) and then rob house 3 (money = 3).
Total amount you can rob = 1 + 3 = 4.

INTERVIEW EXPLANATION: Why Two Linear Problems?

1. **Problem Structure**: The circular constraint means:
   - If we rob house 0, we cannot rob house n-1 (last house)
   - If we rob house n-1, we cannot rob house 0 (first house)
   - We can break the circle by considering two cases

2. **Why Two Linear Problems?**
   - **Key Insight**: The circular problem reduces to two linear House Robber
     problems (like House Robber I):
     * Case 1: Rob houses from index 0 to n-2 (exclude last house)
     * Case 2: Rob houses from index 1 to n-1 (exclude first house)
   
   - **Why This Works**: By excluding one end, we break the circle and can use
     the linear solution. We take the maximum of both cases.
   
   - **Time Complexity**: O(n) - solve two linear problems
   - **Space Complexity**: O(1) - reuse the O(1) space solution from House Robber I

3. **Edge Cases**:
   - Single house: return nums[0]
   - Two houses: return max(nums[0], nums[1])
   - Three or more: solve two linear subproblems

4. **Key Insight**: The circular constraint only affects the first and last
   houses. By solving two linear subproblems (excluding each end), we cover
   all possible optimal solutions.
"""

from typing import List


class Solution:
    """Solution for House Robber II (Circular)"""
    
    def rob_linear(self, nums: List[int]) -> int:
        """
        Helper: Solve linear House Robber problem (House Robber I).
        
        Args:
            nums: List of money in each house (linear, not circular)
            
        Returns:
            Maximum amount that can be robbed
        """
        if not nums:
            return 0
        if len(nums) == 1:
            return nums[0]
        
        prev2 = nums[0]
        prev1 = max(nums[0], nums[1])
        
        for i in range(2, len(nums)):
            curr = max(prev1, prev2 + nums[i])
            prev2, prev1 = prev1, curr
        
        return prev1
    
    def rob(self, nums: List[int]) -> int:
        """
        Find maximum amount of money that can be robbed (circular street).
        
        Args:
            nums: List of money in each house (arranged in circle)
            
        Returns:
            Maximum amount that can be robbed
        """
        if not nums:
            return 0
        if len(nums) == 1:
            return nums[0]
        if len(nums) == 2:
            return max(nums[0], nums[1])
        
        # Case 1: Rob houses 0 to n-2 (exclude last house)
        case1 = self.rob_linear(nums[:-1])
        
        # Case 2: Rob houses 1 to n-1 (exclude first house)
        case2 = self.rob_linear(nums[1:])
        
        return max(case1, case2)


def test_house_robber_ii():
    """Test cases for House Robber II"""
    sol = Solution()
    
    # Test case 1: Example 1
    nums1 = [2, 3, 2]
    result1 = sol.rob(nums1)
    assert result1 == 3, f"Expected 3, got {result1}"
    print(f"✓ Test 1: {nums1} → {result1}")
    
    # Test case 2: Example 2
    nums2 = [1, 2, 3, 1]
    result2 = sol.rob(nums2)
    assert result2 == 4, f"Expected 4, got {result2}"
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
    
    # Test case 5: All same value
    nums5 = [1, 1, 1, 1]
    result5 = sol.rob(nums5)
    assert result5 == 2, f"Expected 2, got {result5}"  # Rob two non-adjacent
    print(f"✓ Test 5: {nums5} → {result5}")
    
    # Test case 6: Empty list
    nums6 = []
    result6 = sol.rob(nums6)
    assert result6 == 0, f"Expected 0, got {result6}"
    print("✓ Test 6: Empty list → 0")
    
    print("\nAll tests passed!")


if __name__ == "__main__":
    test_house_robber_ii()
    
    # Example usage
    print("\nExample usage:")
    sol = Solution()
    nums = [2, 3, 2]
    result = sol.rob(nums)
    print(f"Input: {nums} (circular)")
    print(f"Maximum amount: {result}")
    print("Explanation:")
    print("  Case 1 (exclude last): [2, 3] → max = 3")
    print("  Case 2 (exclude first): [3, 2] → max = 3")
    print("  Result: max(3, 3) = 3")
# %%

