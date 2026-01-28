# LeetCode 227: Basic Calculator II
#%%
"""
Problem Statement:
Given a string s which represents an expression, evaluate this expression and return its value.

The integer division should truncate toward zero.

You may assume that the given expression is always valid. All intermediate results will be in
the range of [-2^31, 2^31 - 1].

Note: You are not allowed to use any built-in function which evaluates strings as mathematical
expressions, such as eval().

Example 1:
Input: s = "3+2*2"
Output: 7
Explanation: 3 + (2 * 2) = 3 + 4 = 7

Example 2:
Input: s = " 3/2 "
Output: 1
Explanation: 3 / 2 = 1 (truncated)

Example 3:
Input: s = " 3+5 / 2 "
Output: 5
Explanation: 3 + (5 / 2) = 3 + 2 = 5

Constraints:
- 1 <= s.length <= 3 * 10^5
- s consists of integers and operators ('+', '-', '*', '/') separated by some number of spaces.
- s represents a valid expression.
- All the integers in the expression are non-negative integers in the range [0, 2^31 - 1].
- The answer is guaranteed to fit in a 32-bit integer.

INTERVIEW EXPLANATION: Why Stack or Single-Pass for Basic Calculator II?

1. **Problem Structure**: We need to evaluate an expression with +, -, *, / operators.
   - Key challenge: Operator precedence (* and / have higher precedence than + and -)
   - We need to handle: numbers, operators, and spaces

2. **Why Stack or Single-Pass?**
   - **Stack Approach**: Process numbers and operators, defer lower precedence operations
   - **Single-Pass Approach**: Process immediately, handle precedence on-the-fly
   - Both are O(n) time, O(n) or O(1) space

3. **Key Insight - Operator Precedence**:
   - * and / have higher precedence → process immediately
   - + and - have lower precedence → defer until we see what comes next
   - We can use a stack to store deferred operations, or process in single pass

4. **Optimized Single-Pass Approach**:
   - Process numbers and operators in one pass
   - For * and /: process immediately with previous number
   - For + and -: store in result, handle sign
   - No stack needed! O(1) extra space

5. **Time Complexity**: O(n) - single pass through string
6. **Space Complexity**: O(1) for single-pass, O(n) for stack approach
"""

from typing import List


class Solution:
    """Solution for Basic Calculator II"""
    
    def calculate(self, s: str) -> int:
        """
        Optimized single-pass solution without stack.
        
        KEY INSIGHT:
        ------------
        We process the expression left to right, handling operator precedence:
        - * and /: Process immediately (high precedence)
        - + and -: Defer by accumulating in result (low precedence)
        
        Algorithm:
        1. Track: current number, previous number, result, current operator
        2. When we see a number: build it digit by digit
        3. When we see an operator or reach end:
           - If previous operator was * or /: process immediately
           - If previous operator was + or -: accumulate in result
        4. Update operator and reset number
        
        Example: "3+2*2"
        - Read '3': num = 3
        - See '+': prev_op = '+', result = 3, num = 0
        - Read '2': num = 2
        - See '*': prev_op = '*', process: num = 2*2 = 4
        - End: result = 3 + 4 = 7
        
        Args:
            s: Expression string
            
        Returns:
            Evaluated result
        """
        if not s:
            return 0
        
        # Remove all spaces for easier processing
        s = s.replace(" ", "")
        
        # Initialize variables
        result = 0  # Final result (accumulates + and - operations)
        current_num = 0  # Current number being built
        prev_num = 0  # Previous number (for * and / operations)
        operator = '+'  # Current operator
        
        i = 0
        n = len(s)
        
        while i < n:
            char = s[i]
            
            # Build number digit by digit
            if char.isdigit():
                current_num = current_num * 10 + int(char)
                i += 1
                continue
            
            # Process PREVIOUS operator when we see a new operator
            if operator == '+':
                result += prev_num
                prev_num = current_num
            elif operator == '-':
                result += prev_num
                prev_num = -current_num
            elif operator == '*':
                prev_num = prev_num * current_num
            elif operator == '/':
                prev_num = int(prev_num / current_num)
            
            # Update operator and reset current number
            operator = char
            current_num = 0
            i += 1
        
        # Process last operator with last number
        if operator == '+':
            result += prev_num + current_num
        elif operator == '-':
            result += prev_num - current_num
        elif operator == '*':
            result += prev_num * current_num
        elif operator == '/':
            result += int(prev_num / current_num)
        else:
            # No operator (single number) - shouldn't happen with valid input
            result += current_num
        
        return result
    
    def calculate_stack(self, s: str) -> int:
        """
        Stack-based solution (alternative approach).
        
        Algorithm:
        1. Use stack to store numbers
        2. Process * and / immediately (pop from stack, compute, push result)
        3. For + and -, push number (with sign) to stack
        4. At end, sum all numbers in stack
        
        Time: O(n), Space: O(n)
        """
        if not s:
            return 0
        
        s = s.replace(" ", "")
        stack = []
        num = 0
        operator = '+'
        
        for i, char in enumerate(s):
            if char.isdigit():
                num = num * 10 + int(char)
            
            if not char.isdigit() or i == len(s) - 1:
                if operator == '+':
                    stack.append(num)
                elif operator == '-':
                    stack.append(-num)
                elif operator == '*':
                    stack.append(stack.pop() * num)
                elif operator == '/':
                    stack.append(int(stack.pop() / num))
                
                operator = char
                num = 0
        
        return sum(stack)
    
    def calculate_optimized(self, s: str) -> int:
        """
        Most optimized single-pass solution with detailed step-by-step processing.
        
        OPTIMIZATION TECHNIQUES:
        ------------------------
        1. Single pass: Process in one iteration
        2. No stack: O(1) extra space (only variables)
        3. Immediate processing: Handle * and / as we see them
        4. Deferred accumulation: Handle + and - at the end
        
        ALGORITHM EXPLANATION:
        ----------------------
        Key variables:
        - result: Running sum of all + and - operations (final answer)
        - prev_num: Last number that might be multiplied/divided
        - current_num: Current number being built from digits
        - operator: Last operator seen
        
        Strategy:
        - When we see + or -: Add prev_num to result, set prev_num = current_num (or -current_num)
        - When we see * or /: Process immediately: prev_num = prev_num * current_num (or /)
        - At end: Add final prev_num to result
        """
        if not s:
            return 0
        
        s = s.replace(" ", "")
        result = 0
        prev_num = 0
        current_num = 0
        operator = '+'
        
        for i, char in enumerate(s):
            if char.isdigit():
                current_num = current_num * 10 + int(char)
            
            # Process PREVIOUS operator when we see a new operator or reach end
            if not char.isdigit() or i == len(s) - 1:
                # Process the operator we saw BEFORE this character
                if operator == '+':
                    result += prev_num
                    prev_num = current_num
                elif operator == '-':
                    result += prev_num
                    prev_num = -current_num
                elif operator == '*':
                    prev_num = prev_num * current_num
                elif operator == '/':
                    prev_num = int(prev_num / current_num)
                
                # Update operator for next iteration (only if not at end)
                if i < len(s) - 1:
                    operator = char
                current_num = 0
        
        # Add the final prev_num to result
        result += prev_num
        
        return result


def visualize_stack_solution():
    """
    Detailed step-by-step visualization of stack-based solution for "3+5/2".
    Shows how the stack evolves at each step.
    """
    print("=" * 70)
    print("STACK-BASED SOLUTION: Step-by-Step Visualization")
    print("=" * 70)
    
    s = "3+5/2"
    print(f"\nExpression: '{s}'")
    print(f"Expected Result: 5 (3 + (5/2) = 3 + 2 = 5)")
    
    # Remove spaces
    s = s.replace(" ", "")
    print(f"\nAfter removing spaces: '{s}'")
    
    # Initialize
    stack = []
    num = 0
    operator = '+'
    
    print(f"\n{'='*70}")
    print("INITIALIZATION")
    print(f"{'='*70}")
    print(f"  stack = {stack}")
    print(f"  num = {num}")
    print(f"  operator = '{operator}'")
    
    step = 1
    for i, char in enumerate(s):
        print(f"\n{'='*70}")
        print(f"STEP {step}: Processing character '{char}' at index {i}")
        print(f"{'='*70}")
        
        if char.isdigit():
            old_num = num
            num = num * 10 + int(char)
            print(f"\n  Character '{char}' is a DIGIT")
            print(f"  Build number: num = {old_num} * 10 + {int(char)} = {num}")
            
            # Check if this is the last character
            if i == len(s) - 1:
                print(f"  → This is the LAST character, need to process operator '{operator}'")
            else:
                print(f"  → Continue reading number...")
                step += 1
                continue
        
        # Process operator (or end of string)
        print(f"\n  Character '{char}' is an OPERATOR (or end of string)")
        print(f"  Previous operator was: '{operator}'")
        print(f"  Current number built: num = {num}")
        print(f"  Current stack state: {stack}")
        
        print(f"\n  Processing operator '{operator}' with num={num}:")
        
        if operator == '+':
            print(f"    Operator is '+' → Low precedence, push num to stack")
            print(f"    stack.append({num})")
            stack.append(num)
            print(f"    → Stack after push: {stack}")
            
        elif operator == '-':
            print(f"    Operator is '-' → Low precedence, push -num to stack")
            print(f"    stack.append(-{num}) = stack.append({-num})")
            stack.append(-num)
            print(f"    → Stack after push: {stack}")
            
        elif operator == '*':
            print(f"    Operator is '*' → High precedence, process immediately!")
            top = stack[-1] if stack else 0
            print(f"    Pop from stack: top = stack.pop() = {top}")
            result = top * num
            print(f"    Compute: {top} * {num} = {result}")
            stack.pop()
            stack.append(result)
            print(f"    Push result: stack.append({result})")
            print(f"    → Stack after operation: {stack}")
            
        elif operator == '/':
            print(f"    Operator is '/' → High precedence, process immediately!")
            top = stack[-1] if stack else 0
            print(f"    Pop from stack: top = stack.pop() = {top}")
            result = int(top / num)
            print(f"    Compute: int({top} / {num}) = int({top/num}) = {result}")
            stack.pop()
            stack.append(result)
            print(f"    Push result: stack.append({result})")
            print(f"    → Stack after operation: {stack}")
        
        # Update for next iteration
        if not char.isdigit():
            operator = char
            print(f"\n  Update operator = '{operator}' for next iteration")
        num = 0
        print(f"  Reset num = 0")
        
        print(f"\n  State after step {step}:")
        print(f"    stack = {stack}")
        print(f"    num = {num}")
        print(f"    operator = '{operator}'")
        
        step += 1
    
    # Final result
    print(f"\n{'='*70}")
    print("FINAL STEP: Sum all numbers in stack")
    print(f"{'='*70}")
    print(f"  stack = {stack}")
    print(f"  result = sum(stack) = {sum(stack)}")
    print(f"\n  ✓ Final Answer: {sum(stack)}")
    print(f"  ✓ Expected: 5")
    print(f"  ✓ Match: {'✓' if sum(stack) == 5 else '✗'}")


def visualize_stack_solution_detailed():
    """
    Even more detailed visualization with ASCII art showing stack operations.
    """
    print("=" * 70)
    print("DETAILED STACK VISUALIZATION: '3+5/2'")
    print("=" * 70)
    
    s = "3+5/2"
    s = s.replace(" ", "")
    
    stack = []
    num = 0
    operator = '+'
    
    print(f"\nExpression: '{s}'")
    print(f"Algorithm: Process * and / immediately, defer + and - to end")
    print(f"\n{'='*70}\n")
    
    steps = [
        ("Read '3'", "num = 3", "stack = []", "operator = '+'"),
        ("See '+'", "Process '+': push 3", "stack = [3]", "operator = '+'"),
        ("Read '5'", "num = 5", "stack = [3]", "operator = '+'"),
        ("See '/'", "Process '+': push 5", "stack = [3, 5]", "operator = '/'"),
        ("Read '2'", "num = 2", "stack = [3, 5]", "operator = '/'"),
        ("End", "Process '/': pop 5, 5/2=2, push 2", "stack = [3, 2]", "Sum = 5"),
    ]
    
    for i, (action, detail, stack_state, extra) in enumerate(steps, 1):
        print(f"Step {i}: {action}")
        print(f"  {detail}")
        print(f"  {stack_state}")
        if extra:
            print(f"  {extra}")
        print()
    
    print(f"{'='*70}")
    print("VISUAL STACK OPERATIONS:")
    print(f"{'='*70}\n")
    
    # Step-by-step with visual stack
    print("Initial State:")
    print("  Stack: []")
    print("  num = 0, operator = '+'\n")
    
    print("Step 1: Read '3'")
    num = 3
    print(f"  num = {num}")
    print("  Stack: []\n")
    
    print("Step 2: See operator '+'")
    print("  Process operator '+' with num=3:")
    print("  → Push 3 to stack (low precedence, defer)")
    stack = [3]
    print(f"  Stack: {stack}")
    print("        ┌───┐")
    print("        │ 3 │ ← top")
    print("        └───┘\n")
    operator = '+'
    
    print("Step 3: Read '5'")
    num = 5
    print(f"  num = {num}")
    print(f"  Stack: {stack}")
    print("        ┌───┐")
    print("        │ 3 │")
    print("        └───┘\n")
    
    print("Step 4: See operator '/'")
    print("  Process operator '+' with num=5:")
    print("  → Push 5 to stack (low precedence, defer)")
    stack = [3, 5]
    print(f"  Stack: {stack}")
    print("        ┌───┐")
    print("        │ 5 │ ← top")
    print("        ├───┤")
    print("        │ 3 │")
    print("        └───┘\n")
    operator = '/'
    
    print("Step 5: Read '2'")
    num = 2
    print(f"  num = {num}")
    print(f"  Stack: {stack}")
    print("        ┌───┐")
    print("        │ 5 │ ← top")
    print("        ├───┤")
    print("        │ 3 │")
    print("        └───┘\n")
    
    print("Step 6: End of string")
    print("  Process operator '/' with num=2:")
    print("  → High precedence, process immediately!")
    print("  → Pop 5 from stack")
    print("  → Compute: int(5 / 2) = 2")
    print("  → Push 2 back to stack")
    top = stack.pop()
    result = int(top / num)
    stack.append(result)
    print(f"  Stack: {stack}")
    print("        ┌───┐")
    print("        │ 2 │ ← top (5/2 = 2)")
    print("        ├───┤")
    print("        │ 3 │")
    print("        └───┘\n")
    
    print("Final: Sum all numbers in stack")
    final_result = sum(stack)
    print(f"  result = sum({stack}) = {final_result}")
    print(f"\n  ✓ Answer: {final_result}")
    print(f"  ✓ Expected: 5")
    print(f"  ✓ Match: {'✓' if final_result == 5 else '✗'}")
    
    print(f"\n{'='*70}")
    print("KEY INSIGHTS:")
    print(f"{'='*70}")
    print("1. Stack stores numbers that will be added/subtracted at the end")
    print("2. When we see * or /: Pop top, compute, push result (immediate)")
    print("3. When we see + or -: Push number to stack (defer)")
    print("4. At end: Sum all numbers in stack")
    print("5. This handles operator precedence correctly!")


def explain_step_by_step():
    """
    Detailed step-by-step explanation of the optimized solution.
    """
    print("=" * 70)
    print("STEP-BY-STEP: Optimized Basic Calculator II")
    print("=" * 70)
    
    examples = [
        ("3+2*2", 7),
        (" 3/2 ", 1),
        (" 3+5 / 2 ", 5),
        ("1+2*3-4/2", 5),
    ]
    
    for expr, expected in examples:
        print(f"\n{'='*70}")
        print(f"Example: s = '{expr}'")
        print(f"Expected: {expected}")
        print(f"{'='*70}")
        
        s = expr.replace(" ", "")
        result = 0
        prev_num = 0
        current_num = 0
        operator = '+'
        
        print(f"\nInitialization:")
        print(f"  result = {result}")
        print(f"  prev_num = {prev_num}")
        print(f"  current_num = {current_num}")
        print(f"  operator = '{operator}'")
        
        step = 1
        for i, char in enumerate(s):
            print(f"\n--- Step {step}: Processing character '{char}' at index {i} ---")
            
            if char.isdigit():
                old_num = current_num
                current_num = current_num * 10 + int(char)
                print(f"  Character is digit → Build number")
                print(f"  current_num = {old_num} * 10 + {int(char)} = {current_num}")
                
                # If not at end, continue reading
                if i < len(s) - 1:
                    print(f"  Continue reading number...")
                    step += 1
                    continue
                else:
                    # At end of string, need to process
                    print(f"  End of string reached, process last operator")
            
            # Process operator (or end of string)
            if not char.isdigit():
                print(f"  Character is operator '{char}'")
            print(f"  Previous operator was: '{operator}'")
            print(f"  Processing with prev_num={prev_num}, current_num={current_num}")
            
            if operator == '+':
                old_result = result
                result += prev_num
                old_prev = prev_num
                prev_num = current_num
                print(f"  Operator '+' → Low precedence, defer")
                print(f"  result = {old_result} + {old_prev} = {result}")
                print(f"  prev_num = {current_num} (will add later)")
            elif operator == '-':
                old_result = result
                result += prev_num
                old_prev = prev_num
                prev_num = -current_num
                print(f"  Operator '-' → Low precedence, defer")
                print(f"  result = {old_result} + {old_prev} = {result}")
                print(f"  prev_num = -{current_num} = {prev_num} (will subtract later)")
            elif operator == '*':
                old_prev = prev_num
                prev_num = prev_num * current_num
                print(f"  Operator '*' → High precedence, process immediately!")
                print(f"  prev_num = {old_prev} * {current_num} = {prev_num}")
            elif operator == '/':
                old_prev = prev_num
                prev_num = int(prev_num / current_num)
                print(f"  Operator '/' → High precedence, process immediately!")
                print(f"  prev_num = int({old_prev} / {current_num}) = {prev_num}")
            
            # Update operator only if not at end (if at end, char is last digit)
            if i < len(s) - 1:
                operator = char
                current_num = 0
                print(f"  Update operator = '{operator}', reset current_num = 0")
            else:
                # At end, don't update operator (it's the last digit)
                current_num = 0
                print(f"  End of string, keep operator = '{operator}'")
            
            step += 1
        
        # Final processing
        print(f"\n--- Final Step: End of string ---")
        print(f"  result = {result}")
        print(f"  prev_num = {prev_num}")
        print(f"  current_num = {current_num}")
        print(f"  operator = '{operator}'")
        print(f"  Add prev_num to result: result = {result} + {prev_num} = {result + prev_num}")
        final_result = result + prev_num
        print(f"\n  ✓ Final Answer: {final_result}")
        print(f"  ✓ Expected: {expected}")
        print(f"  ✓ Match: {'✓' if final_result == expected else '✗'}")


def compare_approaches():
    """Compare different approaches to the problem"""
    print("=" * 70)
    print("COMPARING APPROACHES")
    print("=" * 70)
    
    sol = Solution()
    test_cases = [
        ("3+2*2", 7),
        (" 3/2 ", 1),
        (" 3+5 / 2 ", 5),
        ("1+2*3-4/2", 5),
        ("10", 10),
        ("1-1+1", 1),
    ]
    
    print("\n┌─────────────────────┬──────────┬──────────┬──────────┐")
    print("│ Test Case           │ Stack    │ Optimized│ Expected │")
    print("├─────────────────────┼──────────┼──────────┼──────────┤")
    
    for expr, expected in test_cases:
        result_stack = sol.calculate_stack(expr)
        result_opt = sol.calculate_optimized(expr)
        
        match_stack = "✓" if result_stack == expected else "✗"
        match_opt = "✓" if result_opt == expected else "✗"
        
        print(f"│ {expr:19} │ {result_stack:8} │ {result_opt:8} │ {expected:8} │")
        assert result_stack == expected and result_opt == expected, \
            f"Mismatch for {expr}: stack={result_stack}, opt={result_opt}, expected={expected}"
    
    print("└─────────────────────┴──────────┴──────────┴──────────┘")
    
    print("\n" + "=" * 70)
    print("COMPLEXITY COMPARISON")
    print("=" * 70)
    print("\nStack Approach:")
    print("  Time: O(n) - single pass")
    print("  Space: O(n) - stack stores numbers")
    print("\nOptimized Approach:")
    print("  Time: O(n) - single pass")
    print("  Space: O(1) - only variables (result, prev_num, current_num)")
    print("\n✓ Both produce identical results!")
    print("✓ Optimized uses O(1) space vs O(n) for stack")


def test_basic_calculator_ii():
    """Test cases for Basic Calculator II"""
    sol = Solution()
    
    # Test case 1: Example 1
    s1 = "3+2*2"
    result1 = sol.calculate_optimized(s1)
    assert result1 == 7, f"Expected 7, got {result1}"
    print(f"✓ Test 1: '{s1}' = {result1}")
    
    # Test case 2: Example 2
    s2 = " 3/2 "
    result2 = sol.calculate_optimized(s2)
    assert result2 == 1, f"Expected 1, got {result2}"
    print(f"✓ Test 2: '{s2}' = {result2}")
    
    # Test case 3: Example 3
    s3 = " 3+5 / 2 "
    result3 = sol.calculate_optimized(s3)
    assert result3 == 5, f"Expected 5, got {result3}"
    print(f"✓ Test 3: '{s3}' = {result3}")
    
    # Test case 4: Complex expression
    s4 = "1+2*3-4/2"
    result4 = sol.calculate_optimized(s4)
    assert result4 == 5, f"Expected 5, got {result4}"
    print(f"✓ Test 4: '{s4}' = {result4}")
    
    # Test case 5: Single number
    s5 = "10"
    result5 = sol.calculate_optimized(s5)
    assert result5 == 10, f"Expected 10, got {result5}"
    print(f"✓ Test 5: '{s5}' = {result5}")
    
    # Test case 6: Multiple additions
    s6 = "1-1+1"
    result6 = sol.calculate_optimized(s6)
    assert result6 == 1, f"Expected 1, got {result6}"
    print(f"✓ Test 6: '{s6}' = {result6}")
    
    print("\nAll tests passed!")


if __name__ == "__main__":
    test_basic_calculator_ii()
    
    # Compare approaches
    print("\n")
    compare_approaches()
    
    # Stack-based solution visualization for "3+5/2"
    print("\n")
    visualize_stack_solution()
    
    print("\n")
    visualize_stack_solution_detailed()
    
    # Detailed step-by-step explanation (optimized solution)
    print("\n")
    explain_step_by_step()
    
    # Example usage
    print("\n" + "=" * 70)
    print("EXAMPLE USAGE")
    print("=" * 70)
    sol = Solution()
    expr = "3+2*2"
    result = sol.calculate_optimized(expr)
    print(f"\nExpression: '{expr}'")
    print(f"Result: {result}")
    print("Explanation: 3 + (2 * 2) = 3 + 4 = 7")
# %%
