# K Edit Distance Problem
#%%
"""
Problem Statement:
Given a dictionary (list of words) and a target string, find all words from the
dictionary that are at most k edit distance away from the target.

Edit distance is defined as the minimum number of operations (insert, delete,
replace) needed to convert one string to another.

Example:
Input: dictionary = ["abc", "abd", "abcd", "adc"], target = "ac", k = 1
Output: ["abc", "adc"]
Explanation:
- "abc" → "ac" (delete 'b') = 1 edit distance ✓
- "abd" → "ac" (delete 'b', replace 'd' with 'c') = 2 edit distance ✗
- "abcd" → "ac" (delete 'b', delete 'd') = 2 edit distance ✗
- "adc" → "ac" (delete 'd') = 1 edit distance ✓

INTERVIEW EXPLANATION: Why Trie + DP for K Edit Distance?

1. **Problem Structure**: We need to find all words in a dictionary within k
   edit distance of a target. Naive approach would compute edit distance for
   each word separately, which is O(N × m × n) where N = dictionary size.

2. **Why Trie + DP?**
   - **Key Insight**: Use Trie to share common prefixes. As we traverse the
     Trie, we maintain a DP row representing edit distance from target to
     current prefix. This allows us to prune early and share computation.
   
   - **Algorithm**:
     * Build Trie from dictionary
     * DFS through Trie, maintaining DP row at each node
     * DP row: dp[j] = edit distance from target[:j] to current prefix
     * If dp[m] > k at any point, prune this branch
     * When reaching word end, if dp[m] <= k, add to results
   
   - **Time Complexity**: 
     * Naive: O(N × m × n) where N = dict size, m = target len, n = avg word len
     * Trie+DP: O(N × m) in worst case, but much better with pruning
     * Pruning: If edit distance > k, stop exploring that branch
   
   - **Space Complexity**: O(W × L) for Trie where W = words, L = avg length

3. **Key Insight**: The Trie structure allows us to:
   - Share computation for common prefixes
   - Prune branches early when edit distance exceeds k
   - Process all words in a single traversal

4. **DP Row Update**:
   - For each character in Trie path, update DP row
   - Similar to Edit Distance (LC #72), but maintain only one row
   - curr_dp[j] = min operations to match target[:j] with current prefix
"""

from typing import List


class TrieNode:
    """Trie node for storing dictionary words"""
    def __init__(self):
        self.children = {}
        self.is_word = False


class Trie:
    """Trie data structure for dictionary"""
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word: str) -> None:
        """Insert word into Trie"""
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_word = True


class Solution:
    """Solution for K Edit Distance"""
    
    # def kDistanceWords_naive(self, dictionary: List[str], target: str, k: int) -> List[str]:
        # """
        # Naive approach: compute edit distance for each word.
        
        # Time: O(N × m × n) where N = dict size, m = target len, n = word len
        # """
        # def edit_distance(word1: str, word2: str) -> int:
        #     """Compute edit distance between two words"""
        #     m, n = len(word1), len(word2)
        #     dp = [[0] * (n + 1) for _ in range(m + 1)]
            
        #     for i in range(m + 1):
        #         dp[i][0] = i
        #     for j in range(n + 1):
        #         dp[0][j] = j
            
        #     for i in range(1, m + 1):
        #         for j in range(1, n + 1):
        #             if word1[i - 1] == word2[j - 1]:
        #                 dp[i][j] = dp[i - 1][j - 1]
        #             else:
        #                 dp[i][j] = 1 + min(
        #                     dp[i - 1][j],      # delete
        #                     dp[i][j - 1],      # insert
        #                     dp[i - 1][j - 1]   # replace
        #                 )
        #     return dp[m][n]
        
        # result = []
        # for word in dictionary:
        #     if edit_distance(word, target) <= k:
        #         result.append(word)
        # return result
    
    def kDistanceWords_optimized(self, dictionary: List[str], target: str, k: int) -> List[str]:
        """
        Optimized approach using Trie + DP.
        
        Time: O(N × m) with pruning, much better than naive
        """
        # Build Trie
        trie = Trie()
        for word in dictionary:
            trie.insert(word)
        
        result = []
        m = len(target)
        
        def dfs(node: TrieNode, prefix: str, prev_dp: List[int]) -> None:
            """
            DFS through Trie, maintaining DP row.
            
            Args:
                node: Current Trie node
                prefix: Current prefix string
                prev_dp: DP row from previous level (edit distance from target to prefix)
            """
            # Check if current prefix is a word and within k distance
            if node.is_word and prev_dp[m] <= k:
                result.append(prefix)
            
            # Explore children
            for ch, child in node.children.items():
                # Compute new DP row for this character
                curr_dp = [prev_dp[0] + 1]  # Insert ch at beginning
                
                for j in range(1, m + 1):
                    if target[j - 1] == ch:
                        # Characters match, no operation needed
                        curr_dp.append(prev_dp[j - 1])
                    else:
                        # Choose minimum of three operations
                        curr_dp.append(1 + min(
                            prev_dp[j - 1],    # Replace
                            prev_dp[j],        # Delete from target
                            curr_dp[-1]        # Insert ch
                        ))
                
                # Pruning: if minimum edit distance > k, skip this branch
                if min(curr_dp) <= k:
                    dfs(child, prefix + ch, curr_dp)
        
        # Initial DP row: edit distance from "" to target
        initial_dp = list(range(m + 1))
        dfs(trie.root, "", initial_dp)
        
        return result


def test_k_edit_distance():
    """Test cases for K Edit Distance"""
    sol = Solution()
    
    # Test case 1: Basic example
    dictionary1 = ["abc", "abd", "abcd", "adc"]
    target1, k1 = "ac", 1
    # result1_n = sol.kDistanceWords_naive(dictionary1, target1, k1)
    result1_o = sol.kDistanceWords_optimized(dictionary1, target1, k1)
    expected1 = ["abc", "adc"]
    # assert set(result1_n) == set(expected1), f"Naive: Expected {expected1}, got {result1_n}"
    assert set(result1_o) == set(expected1), f"Optimized: Expected {expected1}, got {result1_o}"
    print(f"✓ Test 1: {result1_o}")
    
    # Test case 2: k = 0 (exact match)
    dictionary2 = ["hello", "world", "hello"]
    target2, k2 = "hello", 0
    result2 = sol.kDistanceWords_optimized(dictionary2, target2, k2)
    assert result2 == ["hello"], f"Expected ['hello'], got {result2}"
    print(f"✓ Test 2: Exact match")
    
    # Test case 3: k = 2
    dictionary3 = ["cat", "bat", "rat", "car", "bar"]
    target3, k3 = "cat", 2
    result3 = sol.kDistanceWords_optimized(dictionary3, target3, k3)
    # "cat" (0), "bat" (1), "rat" (1), "car" (1), "bar" (2)
    assert "cat" in result3, "Should include exact match"
    assert "bat" in result3, "Should include distance 1"
    print(f"✓ Test 3: k=2, found {len(result3)} words")
    
    # Test case 4: Empty dictionary
    dictionary4 = []
    target4, k4 = "test", 1
    result4 = sol.kDistanceWords_optimized(dictionary4, target4, k4)
    assert result4 == [], f"Expected [], got {result4}"
    print("✓ Test 4: Empty dictionary")
    
    print("\nAll tests passed!")


#%% STEP-BY-STEP DP VISUALIZATION

def visualize_dp_update():
    """
    Detailed step-by-step visualization of DP update in kDistanceWords_optimized.
    
    This function shows exactly how the DP array evolves as we traverse the Trie.
    """
    print("=" * 80)
    print("STEP-BY-STEP DP VISUALIZATION")
    print("=" * 80)
    
    target = "ac"
    m = len(target)
    
    print(f"\nTarget: '{target}' (length = {m})")
    print(f"DP array indices: 0 to {m}")
    print(f"  dp[0] = edit distance from prefix '' to target[:0] = ''")
    print(f"  dp[1] = edit distance from prefix to target[:1] = 'a'")
    print(f"  dp[2] = edit distance from prefix to target[:2] = 'ac'")
    print(f"  dp[m] = dp[{m}] = edit distance from prefix to full target '{target}'")
    
    print("\n" + "=" * 80)
    print("STEP 1: Initial DP State (at root, prefix = '')")
    print("=" * 80)
    initial_dp = list(range(m + 1))
    print(f"Initial DP: {initial_dp}")
    print("\nExplanation:")
    print("  dp[0] = 0: '' to '' = 0 operations")
    print("  dp[1] = 1: '' to 'a' = 1 insert")
    print("  dp[2] = 2: '' to 'ac' = 2 inserts")
    print("\nVisual representation:")
    print("  Prefix: ''")
    print("  Target: 'a' 'c'")
    print("  DP:    [0] [1] [2]")
    print("           ↑   ↑   ↑")
    print("         ''  'a' 'ac'")
    
    print("\n" + "=" * 80)
    print("STEP 2: Processing character 'a' (prefix becomes 'a')")
    print("=" * 80)
    prev_dp = initial_dp.copy()
    ch = 'a'
    print(f"Previous DP: {prev_dp}")
    print(f"Current character: '{ch}'")
    print(f"Target[{0}] = '{target[0]}'")
    print(f"Match? {ch == target[0]}")
    
    # Build new DP row
    curr_dp = [prev_dp[0] + 1]  # j=0 case: insert ch
    print(f"\nBuilding curr_dp:")
    print(f"  curr_dp[0] = prev_dp[0] + 1 = {prev_dp[0]} + 1 = {curr_dp[0]} (insert '{ch}')")
    
    for j in range(1, m + 1):
        if target[j - 1] == ch:
            curr_dp.append(prev_dp[j - 1])
            print(f"  curr_dp[{j}] = prev_dp[{j-1}] = {prev_dp[j-1]} (match, no operation)")
        else:
            replace = prev_dp[j - 1]
            delete = prev_dp[j]
            insert = curr_dp[-1]
            min_val = min(replace, delete, insert)
            curr_dp.append(1 + min_val)
            print(f"  curr_dp[{j}] = 1 + min(")
            print(f"    replace: prev_dp[{j-1}] = {replace},")
            print(f"    delete:  prev_dp[{j}] = {delete},")
            print(f"    insert:  curr_dp[{j-1}] = {insert}")
            print(f"  ) = 1 + {min_val} = {curr_dp[j]}")
    
    print(f"\nNew DP: {curr_dp}")
    print("\nVisual representation:")
    print("  Prefix: 'a'")
    print("  Target: 'a' 'c'")
    print("  DP:    [1] [0] [1]")
    print("           ↑   ↑   ↑")
    print("         ''  'a' 'ac'")
    print("\nExplanation:")
    print("  dp[0] = 1: 'a' to '' = 1 delete")
    print("  dp[1] = 0: 'a' to 'a' = 0 operations (match!)")
    print("  dp[2] = 1: 'a' to 'ac' = 1 insert ('c')")
    
    print("\n" + "=" * 80)
    print("STEP 3: Processing character 'b' (prefix becomes 'ab')")
    print("=" * 80)
    prev_dp = curr_dp.copy()
    ch = 'b'
    print(f"Previous DP: {prev_dp}")
    print(f"Current character: '{ch}'")
    
    curr_dp = [prev_dp[0] + 1]
    print(f"\nBuilding curr_dp:")
    print(f"  curr_dp[0] = prev_dp[0] + 1 = {prev_dp[0]} + 1 = {curr_dp[0]} (insert '{ch}')")
    
    for j in range(1, m + 1):
        if target[j - 1] == ch:
            curr_dp.append(prev_dp[j - 1])
            print(f"  curr_dp[{j}] = prev_dp[{j-1}] = {prev_dp[j-1]} (match)")
        else:
            replace = prev_dp[j - 1]
            delete = prev_dp[j]
            insert = curr_dp[-1]
            min_val = min(replace, delete, insert)
            curr_dp.append(1 + min_val)
            print(f"  curr_dp[{j}] = 1 + min(")
            print(f"    replace: prev_dp[{j-1}] = {replace},")
            print(f"    delete:  prev_dp[{j}] = {delete},")
            print(f"    insert:  curr_dp[{j-1}] = {insert}")
            print(f"  ) = 1 + {min_val} = {curr_dp[j]}")
    
    print(f"\nNew DP: {curr_dp}")
    print("\nVisual representation:")
    print("  Prefix: 'ab'")
    print("  Target: 'a' 'c'")
    print(f"  DP:    [{curr_dp[0]}] [{curr_dp[1]}] [{curr_dp[2]}]")
    print("           ↑   ↑   ↑")
    print("         ''  'a' 'ac'")
    print("\nExplanation:")
    print(f"  dp[0] = {curr_dp[0]}: 'ab' to '' = {curr_dp[0]} deletes")
    print(f"  dp[1] = {curr_dp[1]}: 'ab' to 'a' = {curr_dp[1]} delete ('b')")
    print(f"  dp[2] = {curr_dp[2]}: 'ab' to 'ac' = min(")
    print(f"    replace: prev_dp[1] = {prev_dp[1]} (match 'a', replace 'b'→'c'),")
    print(f"    delete:  prev_dp[2] = {prev_dp[2]} (match 'ab' to 'ac', delete 'b'),")
    print(f"    insert:  curr_dp[1] = {curr_dp[1]} (match 'ab' to 'a', insert 'c')")
    print(f"  ) + 1 = {curr_dp[2]}")
    
    print("\n" + "=" * 80)
    print("STEP 4: Processing character 'c' (prefix becomes 'abc')")
    print("=" * 80)
    prev_dp = curr_dp.copy()
    ch = 'c'
    print(f"Previous DP: {prev_dp}")
    print(f"Current character: '{ch}'")
    print(f"Target[{1}] = '{target[1]}'")
    print(f"Match? {ch == target[1]}")
    
    curr_dp = [prev_dp[0] + 1]
    print(f"\nBuilding curr_dp:")
    print(f"  curr_dp[0] = prev_dp[0] + 1 = {prev_dp[0]} + 1 = {curr_dp[0]} (insert '{ch}')")
    
    for j in range(1, m + 1):
        if target[j - 1] == ch:
            curr_dp.append(prev_dp[j - 1])
            print(f"  curr_dp[{j}] = prev_dp[{j-1}] = {prev_dp[j-1]} (match, no operation)")
        else:
            replace = prev_dp[j - 1]
            delete = prev_dp[j]
            insert = curr_dp[-1]
            min_val = min(replace, delete, insert)
            curr_dp.append(1 + min_val)
            print(f"  curr_dp[{j}] = 1 + min(")
            print(f"    replace: prev_dp[{j-1}] = {replace},")
            print(f"    delete:  prev_dp[{j}] = {delete},")
            print(f"    insert:  curr_dp[{j-1}] = {insert}")
            print(f"  ) = 1 + {min_val} = {curr_dp[j]}")
    
    print(f"\nNew DP: {curr_dp}")
    print("\nVisual representation:")
    print("  Prefix: 'abc'")
    print("  Target: 'a' 'c'")
    print("  DP:    [3] [2] [1]")
    print("           ↑   ↑   ↑")
    print("         ''  'a' 'ac'")
    print("\nExplanation:")
    print("  dp[0] = 3: 'abc' to '' = 3 deletes")
    print("  dp[1] = 2: 'abc' to 'a' = 2 deletes ('b', 'c')")
    print("  dp[2] = 1: 'abc' to 'ac' = 1 delete ('b') ✓")
    print("\n  Since dp[2] = 1 <= k=1, 'abc' is a valid word!")

def visualize_dp_matrix_comparison():
    """
    Compare the 1D DP approach with the full 2D matrix to show why we only need one row.
    """
    print("\n" + "=" * 80)
    print("WHY ONLY ONE ROW? (1D vs 2D DP Comparison)")
    print("=" * 80)
    
    target = "ac"
    prefix = "abc"
    
    print(f"\nFull 2D DP Matrix (Edit Distance from prefix to target):")
    print(f"  Prefix: '{prefix}'")
    print(f"  Target: '{target}'")
    print("\n  Matrix dp[i][j] = edit distance from prefix[:i] to target[:j]")
    print("\n      ''  'a'  'ac'")
    print("  ''  [0] [1]  [2]")
    print("  'a' [1] [0]  [1]")
    print("  'ab'[2] [1]  [2]")
    print("  'abc'[3] [2]  [1]")
    
    print("\n  Key observation: We only need the LAST ROW!")
    print("  As we traverse Trie, we're building the prefix character by character.")
    print("  We only care about: prefix (full) to target[:j] for all j")
    print("  So we maintain just one row: dp[j] = edit distance from current prefix to target[:j]")
    
    print("\n" + "=" * 80)
    print("DP UPDATE FORMULA BREAKDOWN")
    print("=" * 80)
    
    print("\nFor each character ch in Trie path:")
    print("  prev_dp[j] = edit distance from OLD prefix to target[:j]")
    print("  curr_dp[j] = edit distance from NEW prefix (old + ch) to target[:j]")
    
    print("\nTo compute curr_dp[j], we have 3 options:")
    print("  1. REPLACE: prev_dp[j-1] + (0 if match, 1 if mismatch)")
    print("     - Match old prefix to target[:j-1], then match/replace ch with target[j-1]")
    print("  2. DELETE: prev_dp[j] + 1")
    print("     - Match old prefix to target[:j], then delete ch from prefix")
    print("  3. INSERT: curr_dp[j-1] + 1")
    print("     - Match new prefix to target[:j-1], then insert target[j-1]")
    
    print("\nSpecial case: curr_dp[0]")
    print("  curr_dp[0] = prev_dp[0] + 1")
    print("  Explanation: To match new prefix to '', we need to delete ch")
    print("  (or equivalently: insert ch into '' to get new prefix)")

def trace_example_word():
    """
    Trace through a complete example: finding "abc" in dictionary with target="ac", k=1
    """
    print("\n" + "=" * 80)
    print("COMPLETE EXAMPLE TRACE: Finding 'abc'")
    print("=" * 80)
    
    target = "ac"
    word = "abc"
    k = 1
    
    print(f"\nTarget: '{target}'")
    print(f"Word: '{word}'")
    print(f"k = {k}")
    print(f"\nTracing through Trie path: '' → 'a' → 'ab' → 'abc'")
    
    # Simulate the DP updates
    m = len(target)
    
    # Step 0: Root
    dp = list(range(m + 1))
    print(f"\n[Root] prefix = ''")
    print(f"  DP: {dp}")
    print(f"  dp[{m}] = {dp[m]} (distance from '' to '{target}')")
    
    # Step 1: 'a'
    prev_dp = dp
    dp = [prev_dp[0] + 1]
    for j in range(1, m + 1):
        if target[j-1] == 'a':
            dp.append(prev_dp[j-1])
        else:
            dp.append(1 + min(prev_dp[j-1], prev_dp[j], dp[-1]))
    print(f"\n['a'] prefix = 'a'")
    print(f"  DP: {dp}")
    print(f"  dp[{m}] = {dp[m]} (distance from 'a' to '{target}')")
    print(f"  Match? 'a' == target[0] → dp[1] = prev_dp[0] = 0")
    
    # Step 2: 'b'
    prev_dp = dp
    dp = [prev_dp[0] + 1]
    for j in range(1, m + 1):
        if target[j-1] == 'b':
            dp.append(prev_dp[j-1])
        else:
            dp.append(1 + min(prev_dp[j-1], prev_dp[j], dp[-1]))
    print(f"\n['ab'] prefix = 'ab'")
    print(f"  DP: {dp}")
    print(f"  dp[{m}] = {dp[m]} (distance from 'ab' to '{target}')")
    print(f"  Match? 'b' == target[1]? No → use min of operations")
    
    # Step 3: 'c'
    prev_dp = dp
    dp = [prev_dp[0] + 1]
    for j in range(1, m + 1):
        if target[j-1] == 'c':
            dp.append(prev_dp[j-1])
        else:
            dp.append(1 + min(prev_dp[j-1], prev_dp[j], dp[-1]))
    print(f"\n['abc'] prefix = 'abc' (WORD END)")
    print(f"  DP: {dp}")
    print(f"  dp[{m}] = {dp[m]} (distance from 'abc' to '{target}')")
    print(f"  Match? 'c' == target[1]? Yes → dp[2] = prev_dp[1] = 1")
    print(f"\n  Result: dp[{m}] = {dp[m]} <= k = {k} → 'abc' is valid! ✓")

if __name__ == "__main__":
    test_k_edit_distance()
    
    # Example usage
    print("\nExample usage:")
    sol = Solution()
    dictionary = ["abc", "abd", "abcd", "adc"]
    target = "ac"
    k = 1
    
    print(f"Dictionary: {dictionary}")
    print(f"Target: '{target}', k = {k}")
    result = sol.kDistanceWords_optimized(dictionary, target, k)
    print(f"Words within {k} edit distance: {result}")
    
    # Run visualizations
    print("\n" + "=" * 80)
    visualize_dp_update()
    visualize_dp_matrix_comparison()
    trace_example_word()

# %%
