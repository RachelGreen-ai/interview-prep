# LeetCode 713: Subarray Product Less Than K
#%%
"""
Problem Statement:
Given an array of integers nums and an integer k, return the number of contiguous subarrays
where the product of all the elements in the subarray is strictly less than k.

Example 1:
Input: nums = [10,5,2,6], k = 100
Output: 8
Explanation: The 8 subarrays that have product less than 100 are:
[10], [5], [2], [6], [10,5], [5,2], [2,6], [5,2,6]
Note that [10,5,2] is not included as the product is 100 which is not strictly less than k.

Example 2:
Input: nums = [1,2,3], k = 0
Output: 0

INTERVIEW EXPLANATION: Why Sliding Window for Subarray Product Less Than K?

1. **Problem Structure**: We need to count all contiguous subarrays with product < k.
   This is similar to "subarray sum" problems but with multiplication.

2. **Why Sliding Window?**
   - **Monotonic Property**: If product of [i...j] < k, then all subarrays ending at j
     and starting from i or later also have product < k
   - **Expand Right**: Add elements to window (multiply)
   - **Shrink Left**: Remove elements when product >= k (divide)
   - **Count Subarrays**: For each valid window [left...right], count all subarrays ending at right

3. **Algorithm**:
   a. Use two pointers: left and right
   b. Expand right: multiply product by nums[right]
   c. Shrink left: while product >= k, divide by nums[left] and move left
   d. Count: For window [left...right], there are (right - left + 1) subarrays ending at right
   e. All these subarrays have product < k

4. **Key Insights**:
   - For each right position, find the leftmost left such that product < k
   - All subarrays [left...right], [left+1...right], ..., [right...right] are valid
   - Count = right - left + 1 for each right position
   - Handle k <= 1 edge case (no valid subarrays if k <= 1 and all nums >= 1)

5. **Time Complexity**: O(n) - each element visited at most twice (by left and right pointers)
   
6. **Space Complexity**: O(1) - only using variables
"""


class Solution:
    """Solution for Subarray Product Less Than K"""
    
    def numSubarrayProductLessThanK(self, nums: list[int], k: int) -> int:
        """
        Count subarrays with product less than k.
        
        Args:
            nums: Array of positive integers
            k: Threshold value
            
        Returns:
            Number of contiguous subarrays with product < k
        """
        if k <= 1:
            return 0
        
        count = 0
        product = 1
        left = 0
        
        for right in range(len(nums)):
            # Expand window: multiply by nums[right]
            product *= nums[right]
            
            # Shrink window: while product >= k, remove left element
            while product >= k:
                product //= nums[left]
                left += 1
            
            # Count all subarrays ending at right
            # Subarrays: [left...right], [left+1...right], ..., [right...right]
            count += right - left + 1
        
        return count
    
    def numSubarrayProductLessThanK_verbose(self, nums: list[int], k: int) -> int:
        """
        More verbose version with detailed comments.
        """
        if k <= 1:
            # If k <= 1, no subarray can have product < k (assuming positive integers)
            return 0
        
        count = 0
        product = 1
        left = 0
        
        for right in range(len(nums)):
            # Add nums[right] to current window
            product *= nums[right]
            
            # Shrink window from left until product < k
            while left <= right and product >= k:
                product //= nums[left]
                left += 1
            
            # At this point, all subarrays ending at right and starting from left
            # have product < k. There are (right - left + 1) such subarrays.
            count += right - left + 1
        
        return count
    
    def numSubarrayProductLessThanK_bruteforce(self, nums: list[int], k: int) -> int:
        """
        Brute force approach for comparison (O(n^2)).
        """
        count = 0
        n = len(nums)
        
        for i in range(n):
            product = 1
            for j in range(i, n):
                product *= nums[j]
                if product < k:
                    count += 1
                else:
                    break  # Since all nums are positive, product only increases
        
        return count


def test_subarray_product_less_than_k():
    """Test cases for Subarray Product Less Than K"""
    sol = Solution()
    
    # Test case 1: Example 1
    nums1 = [10,5,2,6]
    k1 = 100
    result1 = sol.numSubarrayProductLessThanK(nums1, k1)
    assert result1 == 8, f"Expected 8, got {result1}"
    print(f"✓ Test 1: nums={nums1}, k={k1}")
    print(f"  Result: {result1} subarrays")
    
    # Test case 2: Example 2
    nums2 = [1,2,3]
    k2 = 0
    result2 = sol.numSubarrayProductLessThanK(nums2, k2)
    assert result2 == 0, f"Expected 0, got {result2}"
    print(f"✓ Test 2: nums={nums2}, k={k2}")
    print(f"  Result: {result2} subarrays")
    
    # Test case 3: All elements less than k
    nums3 = [1,2,3,4]
    k3 = 100
    result3 = sol.numSubarrayProductLessThanK(nums3, k3)
    # All possible subarrays: 4 + 3 + 2 + 1 = 10
    assert result3 == 10, f"Expected 10, got {result3}"
    print(f"✓ Test 3: All elements < k")
    print(f"  Result: {result3} subarrays")
    
    # Test case 4: Single element
    nums4 = [5]
    k4 = 10
    result4 = sol.numSubarrayProductLessThanK(nums4, k4)
    assert result4 == 1, f"Expected 1, got {result4}"
    print(f"✓ Test 4: Single element")
    print(f"  Result: {result4} subarrays")
    
    # Test case 5: k = 1
    nums5 = [1,2,3]
    k5 = 1
    result5 = sol.numSubarrayProductLessThanK(nums5, k5)
    assert result5 == 0, f"Expected 0, got {result5}"
    print(f"✓ Test 5: k = 1")
    print(f"  Result: {result5} subarrays")
    
    print("\nAll tests passed!")


if __name__ == "__main__":
    test_subarray_product_less_than_k()
    
    # Example usage
    print("\nExample usage:")
    sol = Solution()
    
    nums = [10,5,2,6]
    k = 100
    result = sol.numSubarrayProductLessThanK(nums, k)
    print(f"Array: {nums}")
    print(f"k = {k}")
    print(f"Number of subarrays with product < {k}: {result}")
# %%

