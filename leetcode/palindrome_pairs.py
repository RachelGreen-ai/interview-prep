# LeetCode 336: Palindrome Pairs
#%%
"""
Problem Statement:
Given an array of unique words, find all index pairs (i, j) such that:
words[i] + words[j] is a palindrome.

Return the list of such pairs.

Example:
Input: words = ["bat", "tab", "cat"]
Output: [[0, 1], [1, 0]]

Explanation:
- "bat" + "tab" = "battab" → palindrome
- "tab" + "bat" = "tabbat" → palindrome

INTERVIEW EXPLANATION: Why Hash Map of Reversed Words?

1. **Problem Structure**: We need to find pairs where concatenation is palindrome.
   Brute force would be O(n²·k) where n = #words, k = avg word length.

2. **Why Hash Map Approach?**
   - **Key Insight**: If A + B is palindrome, then:
     * Either A's prefix is palindrome and reverse(rest of A) = B
     * Or A's suffix is palindrome and reverse(rest of A) = B
   
   - **Optimization**: Instead of checking all pairs, we:
     * Build hash map of reversed words: {reversed_word: index}
     * For each word, try all possible splits (prefix, suffix)
     * Check if prefix/suffix is palindrome and if reverse of other part exists
   
   - **Time Complexity**: 
     * O(n·k²) where n = #words, k = avg word length
     * Much better than O(n²·k) brute force
   
   - **Space Complexity**: O(n·k) for hash map

3. **Key Insight**: For word "bat" split at position i:
   - Prefix = word[:i], Suffix = word[i:]
   - If prefix is palindrome → need reversed(suffix) to exist
   - If suffix is palindrome → need reversed(prefix) to exist
   - Special case: empty prefix/suffix (word itself is palindrome or reverse exists)
"""

from typing import List


class Solution:
    """Solution for Palindrome Pairs problem"""
    
    def palindromePairs(self, words: List[str]) -> List[List[int]]:
        """
        Find all index pairs (i, j) such that words[i] + words[j] is palindrome.
        
        Args:
            words: List of unique words
            
        Returns:
            List of [i, j] pairs
        """
        def is_palindrome(s: str) -> bool:
            """Check if string is palindrome"""
            return s == s[::-1]
        
        # Build hash map of reversed words: {reversed_word: index}
        word_map = {w[::-1]: i for i, w in enumerate(words)}
        
        res = []
        
        for i, word in enumerate(words):
            # Try all possible splits (including empty prefix/suffix)
            for cut in range(len(word) + 1):
                prefix, suffix = word[:cut], word[cut:]
                
                # Case 1: prefix is palindrome → look for reversed(suffix)
                if is_palindrome(prefix) and suffix in word_map:
                    j = word_map[suffix]
                    if j != i:  # Avoid self-pair
                        res.append([j, i])
                
                # Case 2: suffix is palindrome → look for reversed(prefix)
                # Avoid duplicates when cut == len(word) (already handled in case 1)
                if cut != len(word) and is_palindrome(suffix) and prefix in word_map:
                    j = word_map[prefix]
                    if j != i:  # Avoid self-pair
                        res.append([i, j])
        
        return res


def test_palindrome_pairs():
    """Test cases for Palindrome Pairs"""
    sol = Solution()
    
    # Test case 1: Basic example
    words1 = ["bat", "tab", "cat"]
    result1 = sol.palindrome_pairs(words1)
    # Should contain [0,1] and [1,0]
    assert len(result1) == 2, f"Expected 2 pairs, got {len(result1)}"
    assert [0, 1] in result1, "Should contain [0, 1]"
    assert [1, 0] in result1, "Should contain [1, 0]"
    print(f"✓ Test 1: {result1}")
    
    # Test case 2: Empty string (palindrome with any word)
    words2 = ["a", "b", ""]
    result2 = sol.palindrome_pairs(words2)
    # "" + "a" = "a" (palindrome), "a" + "" = "a" (palindrome), etc.
    assert len(result2) >= 4, f"Expected at least 4 pairs, got {len(result2)}"
    print(f"✓ Test 2: {result2}")
    
    # Test case 3: Single character words
    words3 = ["a", "b", "c"]
    result3 = sol.palindrome_pairs(words3)
    # No palindromes possible
    assert len(result3) == 0, f"Expected 0 pairs, got {len(result3)}"
    print("✓ Test 3: No pairs (correct)")
    
    # Test case 4: Words that are palindromes themselves
    words4 = ["aba", "c"]
    result4 = sol.palindrome_pairs(words4)
    # "aba" + "c" = "abac" (not palindrome)
    # "c" + "aba" = "caba" (not palindrome)
    # But "aba" + "" = "aba" if empty string exists
    print(f"✓ Test 4: {result4}")
    
    print("\nAll tests passed!")


if __name__ == "__main__":
    test_palindrome_pairs()
    
    # Example usage
    print("\nExample usage:")
    sol = Solution()
    words = ["bat", "tab", "cat"]
    result = sol.palindrome_pairs(words)
    print(f"Input: {words}")
    print(f"Output: {result}")
    
    # Verify results
    for i, j in result:
        combined = words[i] + words[j]
        is_pal = combined == combined[::-1]
        print(f"  words[{i}] + words[{j}] = '{combined}' → {'✓ palindrome' if is_pal else '✗ not palindrome'}")
# %%

