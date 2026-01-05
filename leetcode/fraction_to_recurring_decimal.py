# LeetCode 166: Fraction to Recurring Decimal
#%%
"""
Problem Statement:
Given two integers representing the numerator and denominator of a fraction,
return the fraction in string format.

If the fractional part is repeating, enclose the repeating part in parentheses.

If multiple answers are possible, return any of them.

It is guaranteed that the length of the answer string is less than 10^4 for all given inputs.

Example 1:
Input: numerator = 1, denominator = 2
Output: "0.5"

Example 2:
Input: numerator = 2, denominator = 1
Output: "2"

Example 3:
Input: numerator = 4, denominator = 333
Output: "0.(012)"

INTERVIEW EXPLANATION: Why HashMap for Fraction to Recurring Decimal?

1. **Problem Structure**: We need to:
   - Handle integer part (before decimal)
   - Handle fractional part (after decimal)
   - Detect repeating patterns in fractional part

2. **Why HashMap?**
   - **Detect Repeats**: When we see the same remainder again, we've found a repeating cycle
   - **Track Positions**: Store remainder -> position in result string
   - **Insert Parentheses**: When repeat detected, insert '(' at stored position

3. **Algorithm**:
   a. Handle sign (negative result)
   b. Calculate integer part: numerator // denominator
   c. Calculate remainder
   d. If remainder == 0, return integer part as string
   e. Start fractional part: add decimal point
   f. While remainder != 0:
      - If remainder seen before, we found repeat -> insert '(' and return
      - Store remainder -> current position
      - Multiply remainder by 10, divide by denominator
      - Append quotient to result
      - Update remainder

4. **Key Insights**:
   - Use long division algorithm
   - Track remainders to detect cycles
   - Handle edge cases: negative numbers, zero, integer results
   - Position tracking for inserting parentheses

5. **Time Complexity**: O(denominator) - worst case when cycle length is denominator
   
6. **Space Complexity**: O(denominator) for remainder map
"""


class Solution:
    """Solution for Fraction to Recurring Decimal"""
    
    def fractionToDecimal(self, numerator: int, denominator: int) -> str:
        """
        Convert fraction to decimal string with repeating notation.
        
        Args:
            numerator: Numerator of fraction
            denominator: Denominator of fraction
            
        Returns:
            Decimal string representation
        """
        # Handle zero case
        if numerator == 0:
            return "0"
        
        # Handle sign
        sign = ""
        if (numerator < 0) != (denominator < 0):
            sign = "-"
        
        numerator = abs(numerator)
        denominator = abs(denominator)
        
        # Integer part
        integer_part = numerator // denominator
        remainder = numerator % denominator
        
        # If no fractional part
        if remainder == 0:
            return sign + str(integer_part)
        
        # Fractional part
        result = sign + str(integer_part) + "."
        remainder_map = {}  # remainder -> position in result
        
        while remainder != 0:
            # Check if we've seen this remainder before (repeating)
            if remainder in remainder_map:
                # Insert '(' at the position where this remainder first appeared
                pos = remainder_map[remainder]
                result = result[:pos] + "(" + result[pos:] + ")"
                break
            
            # Store current remainder position
            remainder_map[remainder] = len(result)
            
            # Long division: multiply remainder by 10
            remainder *= 10
            quotient = remainder // denominator
            result += str(quotient)
            remainder = remainder % denominator
        
        return result
    
    def fractionToDecimal_verbose(self, numerator: int, denominator: int) -> str:
        """
        More verbose version with detailed comments.
        """
        if numerator == 0:
            return "0"
        
        # Determine sign
        negative = (numerator < 0) != (denominator < 0)
        numerator = abs(numerator)
        denominator = abs(denominator)
        
        # Calculate integer part
        integer = numerator // denominator
        remainder = numerator % denominator
        
        if remainder == 0:
            return ("-" if negative else "") + str(integer)
        
        # Build result string
        result = ("-" if negative else "") + str(integer) + "."
        seen_remainders = {}  # Map remainder to index where it first appeared
        
        while remainder:
            # Check for repeating pattern
            if remainder in seen_remainders:
                # Found repeat: insert parentheses
                repeat_start = seen_remainders[remainder]
                return result[:repeat_start] + "(" + result[repeat_start:] + ")"
            
            # Record this remainder's position
            seen_remainders[remainder] = len(result)
            
            # Perform one step of long division
            remainder *= 10
            digit = remainder // denominator
            result += str(digit)
            remainder = remainder % denominator
        
        return result


def test_fraction_to_decimal():
    """Test cases for Fraction to Recurring Decimal"""
    sol = Solution()
    
    # Test case 1: Example 1
    result1 = sol.fractionToDecimal(1, 2)
    assert result1 == "0.5", f"Expected '0.5', got '{result1}'"
    print(f"✓ Test 1: 1/2 = {result1}")
    
    # Test case 2: Example 2
    result2 = sol.fractionToDecimal(2, 1)
    assert result2 == "2", f"Expected '2', got '{result2}'"
    print(f"✓ Test 2: 2/1 = {result2}")
    
    # Test case 3: Example 3
    result3 = sol.fractionToDecimal(4, 333)
    assert result3 == "0.(012)", f"Expected '0.(012)', got '{result3}'"
    print(f"✓ Test 3: 4/333 = {result3}")
    
    # Test case 4: Negative
    result4 = sol.fractionToDecimal(-1, 2)
    assert result4 == "-0.5", f"Expected '-0.5', got '{result4}'"
    print(f"✓ Test 4: -1/2 = {result4}")
    
    # Test case 5: Repeating
    result5 = sol.fractionToDecimal(1, 3)
    assert result5 == "0.(3)", f"Expected '0.(3)', got '{result5}'"
    print(f"✓ Test 5: 1/3 = {result5}")
    
    # Test case 6: Zero
    result6 = sol.fractionToDecimal(0, 3)
    assert result6 == "0", f"Expected '0', got '{result6}'"
    print(f"✓ Test 6: 0/3 = {result6}")
    
    print("\nAll tests passed!")


if __name__ == "__main__":
    test_fraction_to_decimal()
    
    # Example usage
    print("\nExample usage:")
    sol = Solution()
    
    test_cases = [(1, 2), (2, 1), (4, 333), (1, 3), (-1, 2)]
    for num, den in test_cases:
        result = sol.fractionToDecimal(num, den)
        print(f"{num}/{den} = {result}")
# %%

