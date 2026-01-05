# LeetCode 220: Contains Duplicate III
#%%
"""
Problem Statement:
Given an integer array nums and two integers k and t, return true if there are
two distinct indices i and j such that:
- abs(nums[i] - nums[j]) <= t
- abs(i - j) <= k

Example 1:
Input: nums = [1,2,3,1], k = 3, t = 0
Output: true
Explanation: nums[0] = 1 and nums[3] = 1, abs(0-3) = 3 <= k, abs(1-1) = 0 <= t

Example 2:
Input: nums = [1,0,1,1], k = 1, t = 2
Output: true

Example 3:
Input: nums = [1,5,9,1,5,9], k = 2, t = 3
Output: false

INTERVIEW EXPLANATION: Why Bucket Approach for Contains Duplicate III?

1. **Problem Structure**: We need to find two numbers within index distance k
   and value distance t. Naive approach would be O(n*k) which is too slow.

2. **Why Bucket Approach?**
   - **Key Insight**: Group numbers into buckets of size (t+1). If two numbers
     are in the same bucket or adjacent buckets, they might satisfy the condition.
   
   - **Bucket Mapping**: For number v, bucket = v // (t+1)
     * Numbers in same bucket: guaranteed |v1 - v2| <= t
     * Numbers in adjacent buckets: need to check |v1 - v2| <= t
   
   - **Sliding Window**: Maintain a window of size k using the bucket map.
     Remove numbers outside the window to keep O(k) space.
   
   - **Time Complexity**: O(n) - single pass through array
   - **Space Complexity**: O(min(n, k)) - bucket map size

3. **Key Insight**: Instead of comparing each number with k previous numbers,
   we use buckets to quickly find candidates that might satisfy the condition.
"""

from typing import List


class Solution:
    """Solution for Contains Duplicate III"""
    
    def containsNearbyAlmostDuplicate(self, nums: List[int], k: int, t: int) -> bool:
        """
        Check if there are two distinct indices i, j such that:
        - abs(nums[i] - nums[j]) <= t
        - abs(i - j) <= k
        
        Args:
            nums: Array of integers
            k: Maximum index difference
            t: Maximum value difference
            
        Returns:
            True if such pair exists, False otherwise
        """
        if t < 0:
            return False
        
        buckets = {}
        width = t + 1
        
        for i, v in enumerate(nums):
            bucket = v // width
            
            # Check same bucket
            if bucket in buckets:
                return True
            
            # Check adjacent buckets
            if bucket + 1 in buckets and abs(v - buckets[bucket + 1]) <= t:
                return True
            if bucket - 1 in buckets and abs(v - buckets[bucket - 1]) <= t:
                return True
            
            # Add current number to bucket
            buckets[bucket] = v
            
            # Remove number outside window (maintain window of size k)
            if i >= k:
                del buckets[nums[i - k] // width]
        
        return False


def test_contains_duplicate_iii():
    """Test cases for Contains Duplicate III"""
    sol = Solution()
    
    # Test case 1: Example 1
    nums1, k1, t1 = [1, 2, 3, 1], 3, 0
    result1 = sol.containsNearbyAlmostDuplicate(nums1, k1, t1)
    assert result1 == True, f"Expected True, got {result1}"
    print(f"✓ Test 1: {nums1}, k={k1}, t={t1} → {result1}")
    
    # Test case 2: Example 2
    nums2, k2, t2 = [1, 0, 1, 1], 1, 2
    result2 = sol.containsNearbyAlmostDuplicate(nums2, k2, t2)
    assert result2 == True, f"Expected True, got {result2}"
    print(f"✓ Test 2: {nums2}, k={k2}, t={t2} → {result2}")
    
    # Test case 3: Example 3
    nums3, k3, t3 = [1, 5, 9, 1, 5, 9], 2, 3
    result3 = sol.containsNearbyAlmostDuplicate(nums3, k3, t3)
    assert result3 == False, f"Expected False, got {result3}"
    print(f"✓ Test 3: {nums3}, k={k3}, t={t3} → {result3}")
    
    # Test case 4: Negative t
    nums4, k4, t4 = [1, 2, 3], 1, -1
    result4 = sol.containsNearbyAlmostDuplicate(nums4, k4, t4)
    assert result4 == False, f"Expected False, got {result4}"
    print(f"✓ Test 4: Negative t handled correctly")
    
    print("\nAll tests passed!")


if __name__ == "__main__":
    test_contains_duplicate_iii()
    
    # Example usage
    print("\nExample usage:")
    sol = Solution()
    nums, k, t = [1, 2, 3, 1], 3, 0
    result = sol.containsNearbyAlmostDuplicate(nums, k, t)
    print(f"Input: nums = {nums}, k = {k}, t = {t}")
    print(f"Output: {result}")
    print("Explanation: nums[0] = 1 and nums[3] = 1, abs(0-3) = 3 <= k, abs(1-1) = 0 <= t")
# %%
