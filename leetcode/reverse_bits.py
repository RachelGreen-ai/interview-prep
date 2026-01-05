# LeetCode 190: Reverse Bits
#%%
"""
Problem Statement:
Reverse bits of a given 32 bits unsigned integer.

Note:
- Note that in some languages, such as Java, there is no unsigned integer type.
  In this case, both input and output will be given as signed integer types and
  should not affect your implementation, as the internal binary representation
  of the integer is the same whether it is signed or unsigned.
- In Java, the compiler represents the signed integers using 2's complement notation.

Example 1:
Input: n = 00000010100101000001111010011100
Output: 964176192 (00111001011110000010100101000000)
Explanation: The input binary string 00000010100101000001111010011100
represents the unsigned integer 43261596, so return 964176192 which its binary
representation is 00111001011110000010100101000000.

Example 2:
Input: n = 11111111111111111111111111111101
Output: 3221225471 (10111111111111111111111111111111)

INTERVIEW EXPLANATION: Why Bit Manipulation for Reverse Bits?

1. **Problem Structure**: We need to reverse the bits of a 32-bit integer.
   This is a classic bit manipulation problem.

2. **Why Bit Manipulation?**
   - **Key Operations**:
     * Extract bit: (n >> i) & 1
     * Set bit: result |= (1 << (31 - i))
     * Shift operations: >> (right shift), << (left shift)
   
   - **Approach 1: Iterative**
     * Extract each bit from right to left
     * Place it in reversed position (left to right)
     * Time: O(32) = O(1), Space: O(1)
   
   - **Approach 2: Divide and Conquer (Advanced)**
     * Swap halves recursively
     * More efficient for larger bit widths
     * Time: O(log 32) = O(1), Space: O(1)

3. **Key Insight**: For a 32-bit number:
   - Bit at position i should move to position (31 - i)
   - We can extract bits one by one and place them in reversed positions

4. **Bit Manipulation Tricks**:
   - n & 1: Get least significant bit
   - n >> 1: Shift right (divide by 2)
   - result << 1: Shift left (multiply by 2)
   - result | bit: Set a bit
"""


class Solution:
    """Solution for Reverse Bits"""
    
    def reverseBits_iterative(self, n: int) -> int:
        """
        Reverse bits using iterative approach.
        
        Args:
            n: 32-bit unsigned integer
            
        Returns:
            Integer with reversed bits
        """
        result = 0
        for i in range(32):
            # Extract bit at position i
            bit = (n >> i) & 1
            # Place it at position (31 - i)
            result |= (bit << (31 - i))
        return result
    
    def reverseBits_optimized(self, n: int) -> int:
        """
        Optimized version: build result by shifting.
        
        Args:
            n: 32-bit unsigned integer
            
        Returns:
            Integer with reversed bits
        """
        result = 0
        for i in range(32):
            result <<= 1  # Shift result left
            result |= n & 1  # Add least significant bit of n
            n >>= 1  # Shift n right
        return result
    
    def reverseBits_divide_conquer(self, n: int) -> int:
        """
        Advanced: Divide and conquer approach.
        Swap halves recursively (more efficient for larger bit widths).
        
        Args:
            n: 32-bit unsigned integer
            
        Returns:
            Integer with reversed bits
        """
        # Swap 16-bit halves
        n = ((n & 0xFFFF0000) >> 16) | ((n & 0x0000FFFF) << 16)
        # Swap 8-bit halves
        n = ((n & 0xFF00FF00) >> 8) | ((n & 0x00FF00FF) << 8)
        # Swap 4-bit halves
        n = ((n & 0xF0F0F0F0) >> 4) | ((n & 0x0F0F0F0F) << 4)
        # Swap 2-bit halves
        n = ((n & 0xCCCCCCCC) >> 2) | ((n & 0x33333333) << 2)
        # Swap 1-bit halves
        n = ((n & 0xAAAAAAAA) >> 1) | ((n & 0x55555555) << 1)
        return n


def test_reverse_bits():
    """Test cases for Reverse Bits"""
    sol = Solution()
    
    # Test case 1: Example 1
    n1 = 0b00000010100101000001111010011100
    result1_i = sol.reverseBits_iterative(n1)
    result1_o = sol.reverseBits_optimized(n1)
    result1_d = sol.reverseBits_divide_conquer(n1)
    expected1 = 964176192
    assert result1_i == expected1, f"Iterative: Expected {expected1}, got {result1_i}"
    assert result1_o == expected1, f"Optimized: Expected {expected1}, got {result1_o}"
    assert result1_d == expected1, f"Divide-Conquer: Expected {expected1}, got {result1_d}"
    print(f"✓ Test 1: All methods return {expected1}")
    
    # Test case 2: Example 2
    n2 = 0b11111111111111111111111111111101
    result2_i = sol.reverseBits_iterative(n2)
    result2_o = sol.reverseBits_optimized(n2)
    result2_d = sol.reverseBits_divide_conquer(n2)
    expected2 = 3221225471
    assert result2_i == expected2, f"Iterative: Expected {expected2}, got {result2_i}"
    assert result2_o == expected2, f"Optimized: Expected {expected2}, got {result2_o}"
    assert result2_d == expected2, f"Divide-Conquer: Expected {expected2}, got {result2_d}"
    print(f"✓ Test 2: All methods return {expected2}")
    
    # Test case 3: All zeros
    n3 = 0
    result3 = sol.reverseBits_iterative(n3)
    assert result3 == 0, f"Expected 0, got {result3}"
    print("✓ Test 3: All zeros → 0")
    
    # Test case 4: All ones
    n4 = 0xFFFFFFFF
    result4 = sol.reverseBits_iterative(n4)
    assert result4 == 0xFFFFFFFF, f"Expected all ones, got {result4}"
    print("✓ Test 4: All ones → all ones")
    
    print("\nAll tests passed!")


if __name__ == "__main__":
    test_reverse_bits()
    
    # Example usage
    print("\nExample usage:")
    sol = Solution()
    n = 0b00000010100101000001111010011100
    result = sol.reverseBits_iterative(n)
    print(f"Input:  {n:032b} (decimal: {n})")
    print(f"Output: {result:032b} (decimal: {result})")
    print(f"\nBinary representation reversed!")
# %%

