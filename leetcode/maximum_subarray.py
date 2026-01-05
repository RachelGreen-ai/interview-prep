# LeetCode 53: Maximum Subarray
#%%
"""
Problem Statement:
Given an integer array nums, find the contiguous subarray (containing at least one number)
which has the largest sum and return its sum.

A subarray is a contiguous part of an array.

Example 1:
Input: nums = [-2,1,-3,4,-1,2,1,-5,4]
Output: 6
Explanation: [4,-1,2,1] has the largest sum = 6.

Example 2:
Input: nums = [1]
Output: 1

Example 3:
Input: nums = [5,4,-1,7,8]
Output: 23

INTERVIEW EXPLANATION: Why Kadane's Algorithm for Maximum Subarray?

1. **Problem Structure**: We need to find the maximum sum of any contiguous subarray.
   This is a classic dynamic programming problem that can be solved efficiently.

2. **Why Kadane's Algorithm?**
   - **Optimal Substructure**: Maximum sum ending at i = max(nums[i], max_sum_ending_at_i-1 + nums[i])
   - **Greedy Choice**: Either start new subarray at i, or extend previous subarray
   - **Space Optimization**: Only need to track current max, not full DP array
   - **Single Pass**: O(n) time, O(1) space

3. **Algorithm** (Kadane's Algorithm):
   a. Initialize: current_sum = nums[0], max_sum = nums[0]
   b. For each element from index 1:
      - current_sum = max(nums[i], current_sum + nums[i])
      - max_sum = max(max_sum, current_sum)
   c. Return max_sum

4. **Key Insights**:
   - If current_sum becomes negative, it's better to start fresh (set to 0 or nums[i])
   - Track both current maximum and global maximum
   - At each step, decide: extend previous subarray or start new one

5. **Time Complexity**: O(n) - single pass through array
   
6. **Space Complexity**: O(1) - only using variables
"""


class Solution:
    """Solution for Maximum Subarray"""
    
    def maxSubArray(self, nums: list[int]) -> int:
        """
        Find maximum sum of contiguous subarray.
        
        Args:
            nums: Array of integers
            
        Returns:
            Maximum sum of contiguous subarray
        """
        if not nums:
            return 0
        
        # Kadane's algorithm
        current_sum = nums[0]
        max_sum = nums[0]
        
        for i in range(1, len(nums)):
            # Either extend previous subarray or start new one
            current_sum = max(nums[i], current_sum + nums[i])
            max_sum = max(max_sum, current_sum)
        
        return max_sum
    
    def maxSubArray_dp(self, nums: list[int]) -> int:
        """
        DP version (more explicit, same time/space).
        """
        if not nums:
            return 0
        
        n = len(nums)
        # dp[i] = maximum sum of subarray ending at index i
        dp = [0] * n
        dp[0] = nums[0]
        max_sum = nums[0]
        
        for i in range(1, n):
            # Either extend previous subarray or start new
            dp[i] = max(nums[i], dp[i-1] + nums[i])
            max_sum = max(max_sum, dp[i])
        
        return max_sum
    
    def maxSubArray_divide_conquer(self, nums: list[int]) -> int:
        """
        Divide and conquer approach (O(n log n)).
        """
        def max_crossing_sum(left: int, mid: int, right: int) -> int:
            # Maximum sum crossing the middle
            left_sum = float('-inf')
            current = 0
            for i in range(mid, left - 1, -1):
                current += nums[i]
                left_sum = max(left_sum, current)
            
            right_sum = float('-inf')
            current = 0
            for i in range(mid + 1, right + 1):
                current += nums[i]
                right_sum = max(right_sum, current)
            
            return left_sum + right_sum
        
        def max_subarray_rec(left: int, right: int) -> int:
            if left == right:
                return nums[left]
            
            mid = (left + right) // 2
            
            # Maximum in left half
            left_max = max_subarray_rec(left, mid)
            # Maximum in right half
            right_max = max_subarray_rec(mid + 1, right)
            # Maximum crossing middle
            cross_max = max_crossing_sum(left, mid, right)
            
            return max(left_max, right_max, cross_max)
        
        return max_subarray_rec(0, len(nums) - 1)


def test_maximum_subarray():
    """Test cases for Maximum Subarray"""
    sol = Solution()
    
    # Test case 1: Example 1
    nums1 = [-2,1,-3,4,-1,2,1,-5,4]
    result1 = sol.maxSubArray(nums1)
    assert result1 == 6, f"Expected 6, got {result1}"
    print(f"✓ Test 1: nums={nums1}")
    print(f"  Result: {result1}")
    
    # Test case 2: Example 2
    nums2 = [1]
    result2 = sol.maxSubArray(nums2)
    assert result2 == 1, f"Expected 1, got {result2}"
    print(f"✓ Test 2: nums={nums2}")
    print(f"  Result: {result2}")
    
    # Test case 3: Example 3
    nums3 = [5,4,-1,7,8]
    result3 = sol.maxSubArray(nums3)
    assert result3 == 23, f"Expected 23, got {result3}"
    print(f"✓ Test 3: nums={nums3}")
    print(f"  Result: {result3}")
    
    # Test case 4: All negative
    nums4 = [-1,-2,-3]
    result4 = sol.maxSubArray(nums4)
    assert result4 == -1, f"Expected -1, got {result4}"
    print(f"✓ Test 4: All negative")
    print(f"  Result: {result4}")
    
    # Test case 5: All positive
    nums5 = [1,2,3,4]
    result5 = sol.maxSubArray(nums5)
    assert result5 == 10, f"Expected 10, got {result5}"
    print(f"✓ Test 5: All positive")
    print(f"  Result: {result5}")
    
    print("\nAll tests passed!")


if __name__ == "__main__":
    test_maximum_subarray()
    
    # Example usage
    print("\nExample usage:")
    sol = Solution()
    
    nums = [-2,1,-3,4,-1,2,1,-5,4]
    result = sol.maxSubArray(nums)
    print(f"Array: {nums}")
    print(f"Maximum subarray sum: {result}")
    print(f"Subarray: [4,-1,2,1]")
# %%

