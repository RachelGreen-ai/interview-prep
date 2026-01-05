# LeetCode 202: Happy Number
#%%
"""
Problem Statement:
Write an algorithm to determine if a number n is happy.

A happy number is a number defined by the following process:
- Starting with any positive integer, replace the number by the sum of the
  squares of its digits.
- Repeat the process until the number equals 1 (where it will stay), or it
  loops endlessly in a cycle which does not include 1.
- Those numbers for which this process ends in 1 are happy.

Return true if n is a happy number, and false if not.

Example 1:
Input: n = 19
Output: true
Explanation:
1² + 9² = 1 + 81 = 82
8² + 2² = 64 + 4 = 68
6² + 8² = 36 + 64 = 100
1² + 0² + 0² = 1 (happy!)

Example 2:
Input: n = 2
Output: false
Explanation: Enters a cycle that doesn't include 1.

INTERVIEW EXPLANATION: Why Cycle Detection for Happy Number?

1. **Problem Structure**: We repeatedly apply a transformation (sum of squares
   of digits) until we either:
   - Reach 1 (happy number)
   - Enter a cycle (not happy)

2. **Why Cycle Detection?**
   - **Key Insight**: If a number is not happy, it will eventually enter a cycle.
     We need to detect this cycle to avoid infinite loops.
   
   - **Approach 1: HashSet**
     * Track all numbers we've seen
     * If we see a number again → cycle detected → not happy
     * Time: O(log n) per iteration, O(log n) iterations → O(log² n)
     * Space: O(log n) for the set
   
   - **Approach 2: Floyd's Cycle Detection (Two Pointers)**
     * Use slow and fast pointers (like linked list cycle detection)
     * Slow moves one step, fast moves two steps
     * If they meet → cycle detected
     * Time: O(log n), Space: O(1) - no extra space needed!
   
   - **Mathematical Insight**: All numbers eventually either reach 1 or enter
     the cycle: 4 → 16 → 37 → 58 → 89 → 145 → 42 → 20 → 4

3. **Key Insight**: This is essentially a cycle detection problem in a
   sequence. We can use the same techniques as detecting cycles in linked lists.
"""

from typing import Set


class Solution:
    """Solution for Happy Number"""
    
    def get_next(self, n: int) -> int:
        """
        Get next number by summing squares of digits.
        
        Args:
            n: Current number
            
        Returns:
            Sum of squares of digits
        """
        total = 0
        while n > 0:
            digit = n % 10
            total += digit * digit
            n //= 10
        return total
    
    def isHappy_hashset(self, n: int) -> bool:
        """
        Solution using HashSet to detect cycles.
        
        Args:
            n: Number to check
            
        Returns:
            True if happy number, False otherwise
        """
        seen: Set[int] = set()
        
        while n != 1 and n not in seen:
            seen.add(n)
            n = self.get_next(n)
        
        return n == 1
    
    def isHappy_floyd(self, n: int) -> bool:
        """
        Solution using Floyd's cycle detection (two pointers).
        More space-efficient: O(1) space instead of O(log n).
        
        Args:
            n: Number to check
            
        Returns:
            True if happy number, False otherwise
        """
        slow = n
        fast = self.get_next(n)
        
        # Detect cycle
        while fast != 1 and slow != fast:
            slow = self.get_next(slow)
            fast = self.get_next(self.get_next(fast))
        
        return fast == 1


def test_happy_number():
    """Test cases for Happy Number"""
    sol = Solution()
    
    # Test case 1: Example 1
    n1 = 19
    result1_h = sol.isHappy_hashset(n1)
    result1_f = sol.isHappy_floyd(n1)
    assert result1_h == True, f"HashSet: Expected True, got {result1_h}"
    assert result1_f == True, f"Floyd: Expected True, got {result1_f}"
    print(f"✓ Test 1: {n1} is happy")
    
    # Test case 2: Example 2
    n2 = 2
    result2_h = sol.isHappy_hashset(n2)
    result2_f = sol.isHappy_floyd(n2)
    assert result2_h == False, f"HashSet: Expected False, got {result2_h}"
    assert result2_f == False, f"Floyd: Expected False, got {result2_f}"
    print(f"✓ Test 2: {n2} is not happy")
    
    # Test case 3: Number 1
    n3 = 1
    result3_h = sol.isHappy_hashset(n3)
    result3_f = sol.isHappy_floyd(n3)
    assert result3_h == True, f"HashSet: Expected True, got {result3_h}"
    assert result3_f == True, f"Floyd: Expected True, got {result3_f}"
    print(f"✓ Test 3: {n3} is happy")
    
    # Test case 4: Number 7 (happy)
    n4 = 7
    result4_h = sol.isHappy_hashset(n4)
    result4_f = sol.isHappy_floyd(n4)
    assert result4_h == True, f"HashSet: Expected True, got {result4_h}"
    assert result4_f == True, f"Floyd: Expected True, got {result4_f}"
    print(f"✓ Test 4: {n4} is happy")
    
    print("\nAll tests passed!")


if __name__ == "__main__":
    test_happy_number()
    
    # Example usage
    print("\nExample usage:")
    sol = Solution()
    test_nums = [19, 2, 1, 7]
    for n in test_nums:
        result = sol.isHappy_floyd(n)
        print(f"{n}: {'Happy ✓' if result else 'Not Happy ✗'}")
    
    print("\nDemonstrating cycle for n=2:")
    n = 2
    seen = []
    for _ in range(10):
        seen.append(n)
        n = sol.get_next(n)
        if n == 1:
            break
    print(f"Sequence: {' → '.join(map(str, seen))}")
# %%

