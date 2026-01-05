# CSV Parser Problem
#%%
"""
Problem Statement:
Convert CSV-formatted strings to a custom format with pipe (|) delimiters.

Input: A CSV-formatted string with:
- Commas as field separators
- Quotes around fields when necessary (e.g., fields containing commas or quotes)
- Escaped double quotes inside quotes ("")

Output: A string where:
- Delimiter is | instead of ,
- Quotes around fields are removed
- Escaped quotes ("" inside quotes) become single quotes (")

Example:
Input:
John,Smith,john.smith@gmail.com,Los Angeles,1
Jane,Roberts,janer@msn.com,"San Francisco, CA",0
"Alexandra ""Alex""",Menendez,alex.menendez@gmail.com,Miami,1

Output:
John|Smith|john.smith@gmail.com|Los Angeles|1
Jane|Roberts|janer@msn.com|San Francisco, CA|0
Alexandra "Alex"|Menendez|alex.menendez@gmail.com|Miami|1

INTERVIEW EXPLANATION: Why Use Python's csv Module?

1. **Problem Structure**: CSV parsing is complex because:
   - Fields can contain commas (need quotes)
   - Fields can contain quotes (need escaping)
   - Quotes can be escaped as ""
   - Edge cases are numerous

2. **Why Use Built-in csv Module?**
   - **Complexity**: Manual parsing is error-prone and handles many edge cases
   - **Reliability**: Python's csv.reader handles all CSV edge cases correctly:
     * Commas inside quoted fields
     * Escaped quotes ("")
     * Multi-line fields
     * Various quote styles
   
   - **Time Complexity**: O(n) where n = input length
   - **Space Complexity**: O(n) for storing parsed data

3. **Key Insight**: Don't reinvent the wheel! CSV parsing has many edge cases
   that are easy to miss. Using the standard library shows:
   - Awareness of available tools
   - Understanding of when to use libraries vs. manual parsing
   - Production-ready thinking

4. **Alternative (Manual Parsing)**:
   - State machine approach
   - Track quote state (inside/outside quotes)
   - Handle escaped quotes
   - More complex and error-prone
"""

import csv
from io import StringIO
from typing import List


class Solution:
    """Solution for CSV Parser"""
    
    def csv_to_pipe_delimited(self, csv_text: str) -> str:
        """
        Convert CSV text to pipe-delimited format.
        Uses Python's csv module for reliable parsing.
        
        Args:
            csv_text: CSV-formatted string
            
        Returns:
            Pipe-delimited string
        """
        f = StringIO(csv_text)
        reader = csv.reader(f)
        
        result = []
        for row in reader:
            # Join fields with |, quotes are automatically handled by csv.reader
            result.append('|'.join(row))
        
        return '\n'.join(result)
    
    def csv_to_pipe_delimited_manual(self, csv_text: str) -> str:
        """
        Manual parsing approach (for educational purposes).
        More complex but shows understanding of parsing logic.
        
        Args:
            csv_text: CSV-formatted string
            
        Returns:
            Pipe-delimited string
        """
        lines = csv_text.strip().split('\n')
        result = []
        
        for line in lines:
            fields = []
            current_field = []
            in_quotes = False
            i = 0
            
            while i < len(line):
                ch = line[i]
                
                if ch == '"':
                    if in_quotes and i + 1 < len(line) and line[i + 1] == '"':
                        # Escaped quote: ""
                        current_field.append('"')
                        i += 2
                    else:
                        # Toggle quote state
                        in_quotes = not in_quotes
                        i += 1
                elif ch == ',' and not in_quotes:
                    # Field separator
                    fields.append(''.join(current_field))
                    current_field = []
                    i += 1
                else:
                    current_field.append(ch)
                    i += 1
            
            # Add last field
            fields.append(''.join(current_field))
            result.append('|'.join(fields))
        
        return '\n'.join(result)


def test_csv_parser():
    """Test cases for CSV Parser"""
    sol = Solution()
    
    # Test case 1: Basic example
    csv_input1 = """John,Smith,john.smith@gmail.com,Los Angeles,1
Jane,Roberts,janer@msn.com,"San Francisco, CA",0
"Alexandra ""Alex""",Menendez,alex.menendez@gmail.com,Miami,1"""
    
    result1 = sol.csv_to_pipe_delimited(csv_input1)
    expected1 = """John|Smith|john.smith@gmail.com|Los Angeles|1
Jane|Roberts|janer@msn.com|San Francisco, CA|0
Alexandra "Alex"|Menendez|alex.menendez@gmail.com|Miami|1"""
    
    assert result1 == expected1, f"Expected:\n{expected1}\nGot:\n{result1}"
    print("✓ Test 1: Basic CSV parsing")
    
    # Test case 2: Simple case (no quotes)
    csv_input2 = "a,b,c"
    result2 = sol.csv_to_pipe_delimited(csv_input2)
    assert result2 == "a|b|c", f"Expected 'a|b|c', got '{result2}'"
    print("✓ Test 2: Simple case")
    
    # Test case 3: Escaped quotes
    csv_input3 = '"Hello ""World""",test'
    result3 = sol.csv_to_pipe_delimited(csv_input3)
    assert result3 == 'Hello "World"|test', f"Expected 'Hello \"World\"|test', got '{result3}'"
    print("✓ Test 3: Escaped quotes")
    
    # Test case 4: Commas in quoted field
    csv_input4 = 'Name,"City, State",Age'
    result4 = sol.csv_to_pipe_delimited(csv_input4)
    assert result4 == 'Name|City, State|Age', f"Expected 'Name|City, State|Age', got '{result4}'"
    print("✓ Test 4: Commas in quoted field")
    
    # Test manual parser
    result1_manual = sol.csv_to_pipe_delimited_manual(csv_input1)
    assert result1_manual == expected1, "Manual parser should match"
    print("✓ Test 5: Manual parser matches")
    
    print("\nAll tests passed!")


if __name__ == "__main__":
    test_csv_parser()
    
    # Example usage
    print("\nExample usage:")
    sol = Solution()
    csv_input = """John,Smith,john.smith@gmail.com,Los Angeles,1
Jane,Roberts,janer@msn.com,"San Francisco, CA",0
"Alexandra ""Alex""",Menendez,alex.menendez@gmail.com,Miami,1"""
    
    print("Input CSV:")
    print(csv_input)
    print("\nOutput (pipe-delimited):")
    result = sol.csv_to_pipe_delimited(csv_input)
    print(result)
# %%

