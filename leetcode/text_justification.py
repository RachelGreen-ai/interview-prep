# LeetCode 68: Text Justification
#%%
"""
Problem Statement:
Given an array of words and a maximum width maxWidth, format the text such that
each line has exactly maxWidth characters and is fully (left and right) justified.

Rules:
1. Pack as many words as possible in a line
2. Use spaces ' ' to fill up to maxWidth
3. Extra spaces are distributed evenly, left to right if not divisible
4. Last line: left-justified, no extra spacing between words

Example:
Input:
words = ["This", "is", "an", "example", "of", "text", "justification."]
maxWidth = 16

Output:
[
   "This    is    an",
   "example  of text",
   "justification.  "
]

INTERVIEW EXPLANATION: Why Greedy Line Packing?

1. **Problem Structure**: We need to pack words into lines of fixed width,
   maximizing words per line while distributing spaces evenly.

2. **Why Greedy Approach?**
   - **Optimal Packing**: For each line, we want to pack as many words as possible.
     This is optimal because we can't rearrange words - they must stay in order.
   
   - **Space Distribution**: Once we know which words fit, we distribute spaces
     evenly. Leftmost gaps get extra spaces if not evenly divisible.
   
   - **Time Complexity**: O(n) where n = total number of words
     * Single pass through words
     * Each word processed once
   
   - **Space Complexity**: O(n) for output array

3. **Key Steps**:
   - Greedy packing: Add words until next word won't fit
   - Space calculation: total_spaces = maxWidth - sum(word_lengths)
   - Distribution: space_between = total_spaces // (num_words - 1)
   - Extra spaces: extra = total_spaces % (num_words - 1) → give to leftmost gaps
   - Last line: Special case - left-justified with single spaces

4. **Edge Cases**:
   - Single word in line: left-justified
   - Last line: left-justified
   - Words longer than maxWidth: (usually not in problem, but handle gracefully)
"""

from typing import List


class Solution:
    """Solution for Text Justification"""
    
    def fullJustify(self, words: List[str], maxWidth: int) -> List[str]:
        """
        Format text with full justification.
        
        Args:
            words: List of words to format
            maxWidth: Maximum width of each line
            
        Returns:
            List of justified lines
        """
        res = []
        i = 0
        n = len(words)
        
        while i < n:
            # Step 1: Determine how many words fit in the line
            line_len = len(words[i])
            j = i + 1
            
            while j < n and line_len + 1 + len(words[j]) <= maxWidth:
                line_len += 1 + len(words[j])  # +1 for space
                j += 1
            
            # words[i:j] fit in the line
            line_words = words[i:j]
            num_words = j - i
            line = ""
            
            # Step 2: Last line or single-word line → left-justified
            if j == n or num_words == 1:
                line = ' '.join(line_words)
                line += ' ' * (maxWidth - len(line))
            else:
                # Step 3: Distribute spaces evenly
                total_spaces = maxWidth - sum(len(word) for word in line_words)
                space_between = total_spaces // (num_words - 1)
                extra_spaces = total_spaces % (num_words - 1)
                
                # Build line with distributed spaces
                for k in range(num_words - 1):
                    line += line_words[k]
                    # Add base spaces + 1 extra if this gap gets extra space
                    line += ' ' * (space_between + (1 if k < extra_spaces else 0))
                line += line_words[-1]  # last word
            
            res.append(line)
            i = j
        
        return res


def test_text_justification():
    """Test cases for Text Justification"""
    sol = Solution()
    
    # Test case 1: Basic example
    words1 = ["This", "is", "an", "example", "of", "text", "justification."]
    result1 = sol.fullJustify(words1, 16)
    assert len(result1) == 3, f"Expected 3 lines, got {len(result1)}"
    assert all(len(line) == 16 for line in result1), "All lines should be length 16"
    print("✓ Test 1: Basic justification")
    for line in result1:
        print(f"  '{line}'")
    
    # Test case 2: Single word per line
    words2 = ["a", "b", "c"]
    result2 = sol.fullJustify(words2, 1)
    assert len(result2) == 3, f"Expected 3 lines, got {len(result2)}"
    print("✓ Test 2: Single word per line")
    
    # Test case 3: Last line left-justified
    words3 = ["What", "must", "be", "acknowledgment", "shall", "be"]
    result3 = sol.fullJustify(words3, 16)
    # Last line should be left-justified
    last_line = result3[-1]
    assert last_line.startswith("shall be"), "Last line should be left-justified"
    print("✓ Test 3: Last line left-justified")
    
    # Test case 4: Edge case - empty words
    words4 = [""]
    result4 = sol.fullJustify(words4, 2)
    assert len(result4) == 1, "Should handle empty word"
    assert len(result4[0]) == 2, "Line should be padded to maxWidth"
    print("✓ Test 4: Edge case handled")
    
    print("\nAll tests passed!")


if __name__ == "__main__":
    test_text_justification()
    
    # Example usage
    print("\nExample usage:")
    sol = Solution()
    words = ["This", "is", "an", "example", "of", "text", "justification."]
    result = sol.fullJustify(words, 16)
    
    print("Input:")
    print(f"  words = {words}")
    print(f"  maxWidth = 16\n")
    print("Output:")
    for i, line in enumerate(result, 1):
        print(f"  Line {i}: '{line}' (length: {len(line)})")
# %%

