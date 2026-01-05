# LeetCode 400: Nth Digit
#%%
"""
Problem Statement:
Given an integer n, return the nth digit of the infinite integer sequence
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, ...].

Example 1:
Input: n = 3
Output: 3

Example 2:
Input: n = 11
Output: 0
Explanation: The 11th digit of the sequence 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, ...
is a 0, which is part of the number 10.

INTERVIEW EXPLANATION: Why Mathematical Approach for Nth Digit?

1. **Problem Structure**: The sequence is grouped by number of digits:
   - 1-digit numbers: 1-9 (9 numbers, 9 digits)
   - 2-digit numbers: 10-99 (90 numbers, 180 digits)
   - 3-digit numbers: 100-999 (900 numbers, 2700 digits)
   - k-digit numbers: 9 * 10^(k-1) numbers, 9 * 10^(k-1) * k digits

2. **Why Mathematical Approach?**
   - **Pattern Recognition**: Digits are grouped by number length
   - **Direct Calculation**: Can calculate which number and which digit without
     generating the entire sequence
   - **Efficiency**: O(log n) instead of O(n)

3. **Algorithm**:
   a. Find which group (1-digit, 2-digit, etc.) contains the nth digit
   b. Calculate which number in that group contains the nth digit
   c. Calculate which digit in that number is the nth digit
   d. Return that digit

4. **Key Insights**:
   - Group by digit length: 1-digit, 2-digit, 3-digit, ...
   - Each group has 9 * 10^(k-1) * k digits
   - Subtract group sizes until we find the right group
   - Calculate the number and digit position within that group

5. **Time Complexity**: O(log n) - number of digit groups is logarithmic
   
6. **Space Complexity**: O(1)
"""


class Solution:
    """Solution for Nth Digit"""
    
    def findNthDigit(self, n: int) -> int:
        """
        Find the nth digit in the infinite sequence.
        
        Args:
            n: Position in sequence (1-indexed)
            
        Returns:
            The nth digit
        """
        # Step 1: Find which group (1-digit, 2-digit, etc.)
        digit_length = 1  # Start with 1-digit numbers
        count = 9  # Number of digits in current group
        
        while n > count:
            n -= count
            digit_length += 1
            count = 9 * (10 ** (digit_length - 1)) * digit_length
        
        # Step 2: Find which number in this group
        # First number in this group
        start_number = 10 ** (digit_length - 1)
        # Which number in the group (0-indexed)
        number_index = (n - 1) // digit_length
        # The actual number
        number = start_number + number_index
        
        # Step 3: Find which digit in this number
        # Which digit in the number (0-indexed from left)
        digit_index = (n - 1) % digit_length
        
        # Extract the digit
        return int(str(number)[digit_index])
    
    def findNthDigit_verbose(self, n: int) -> int:
        """
        More verbose version with detailed comments.
        """
        # Group 1: 1-digit numbers (1-9): 9 numbers, 9 digits
        # Group 2: 2-digit numbers (10-99): 90 numbers, 180 digits
        # Group 3: 3-digit numbers (100-999): 900 numbers, 2700 digits
        # Group k: k-digit numbers: 9 * 10^(k-1) numbers, 9 * 10^(k-1) * k digits
        
        length = 1  # Current group digit length
        count = 9  # Total digits in current group
        
        # Find which group contains the nth digit
        while n > count:
            n -= count
            length += 1
            # Calculate digits in next group
            count = 9 * (10 ** (length - 1)) * length
        
        # Now we know the nth digit is in a length-digit number
        # First number with length digits
        start = 10 ** (length - 1)
        # Which number in this group (0-indexed)
        num_index = (n - 1) // length
        # The actual number
        num = start + num_index
        
        # Which digit in this number (0-indexed from left)
        digit_pos = (n - 1) % length
        
        return int(str(num)[digit_pos])


def test_nth_digit():
    """Test cases for Nth Digit"""
    sol = Solution()
    
    # Test case 1: Example 1
    result1 = sol.findNthDigit(3)
    assert result1 == 3, f"Expected 3, got {result1}"
    print(f"✓ Test 1: n=3 -> {result1}")
    
    # Test case 2: Example 2
    result2 = sol.findNthDigit(11)
    assert result2 == 0, f"Expected 0, got {result2}"
    print(f"✓ Test 2: n=11 -> {result2}")
    
    # Test case 3: First digit
    result3 = sol.findNthDigit(1)
    assert result3 == 1, f"Expected 1, got {result3}"
    print(f"✓ Test 3: n=1 -> {result3}")
    
    # Test case 4: Last 1-digit
    result4 = sol.findNthDigit(9)
    assert result4 == 9, f"Expected 9, got {result4}"
    print(f"✓ Test 4: n=9 -> {result4}")
    
    # Test case 5: First 2-digit
    result5 = sol.findNthDigit(10)
    assert result5 == 1, f"Expected 1, got {result5}"  # First digit of 10
    print(f"✓ Test 5: n=10 -> {result5}")
    
    # Test case 6: Second digit of 10
    result6 = sol.findNthDigit(11)
    assert result6 == 0, f"Expected 0, got {result6}"  # Second digit of 10
    print(f"✓ Test 6: n=11 -> {result6}")
    
    print("\nAll tests passed!")


if __name__ == "__main__":
    test_nth_digit()
    
    # Example usage
    print("\nExample usage:")
    sol = Solution()
    
    test_ns = [3, 11, 15, 100, 1000]
    for n in test_ns:
        result = sol.findNthDigit(n)
        print(f"n={n} -> digit: {result}")
# %%

