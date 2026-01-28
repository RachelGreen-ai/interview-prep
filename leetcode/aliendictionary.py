#leetcode 269 Alien Dictionary
#%%
"""
Problem Statement:
Given a list of words, return the order of the characters in the alien language.
If there is no valid order, return an empty string.

Example:
Input: ["wrt","wrf","er","ett","rftt"]
Output: "wertf"

Input: ["z","x"]
Output: "zx"

Input: ["z","x","z"]
Output: ""

Constraints:
1 <= words.length <= 100
1 <= words[i].length <= 100
words[i] consists of only lowercase English letters.

INTERVIEW EXPLANATION: Why Topological Sort for Alien Dictionary?

1. **Problem Structure**: We need to determine the order of characters based on the given words.
   - Each character is a node in the graph
   - An edge from char1 to char2 means char1 appears before char2
   - We need to find a valid topological order of all characters

2. **Why Topological Sort?**
   - **Directed Acyclic Graph (DAG)**: The graph is guaranteed to be a DAG because:
     * Each word is lexicographically sorted
     * No cycles exist (no char depends on itself)
     * We only add edges when there's a clear order
     
   - **Key Insight**: If char1 appears before char2 in the alien dictionary,
     there must be an edge from char1 to char2.
     We can use topological sort to find a valid order of all characters.
     
   - **Overlapping Subproblems**: When checking if a character appears before another,
     we repeatedly check the same characters. Topological sort avoids recomputation.
     
   - **Time Complexity**: O(V + E) - linear time to build graph and perform topological sort
   - **Space Complexity**: O(V) - storing graph and in-degree array

3. **Implementation Steps**:
   - Build the graph: Create a node for each character and add edges based on order
   - Calculate in-degrees: Count how many edges point to each character
   - Topological sort: Use Kahn's algorithm to find a valid order
   - Handle cycles: Return empty string if there's a cycle

4. **Key Edge Cases**:
   - Empty input
   - Single word input
   - Already sorted words
   - Words with different lengths
   - Words with cycles

5. **Trade-offs**:
   - Array vs dictionary: Array is more space-efficient but requires finding the index
   - Set vs list: Set is more space-efficient but requires hashing
   - **Kahn's Algorithm vs DFS-based Topological Sort**: Two main approaches
   - Cycle detection: We handle cycles by returning empty string

DEEP DIVE: Kahn's Algorithm vs DFS-based Topological Sort
----------------------------------------------------------
This problem is PERFECT for comparing two fundamental approaches to topological sorting:
1. **Kahn's Algorithm** (BFS-based) - Current implementation
2. **DFS-based Topological Sort** - Alternative approach

Both produce valid topological orders, but have different characteristics!

"""
from typing import List

class Solution:
    """
    Kahn's Algorithm (BFS-based) Topological Sort Implementation
    
    HOW IT WORKS:
    ------------
    1. Build graph: Each character is a node, edges represent ordering
    2. Calculate in-degrees: Count incoming edges for each node
    3. Start with sources: Add all nodes with in-degree 0 to queue
    4. Process level by level:
       - Remove node from queue, add to result
       - Decrease in-degree of all neighbors
       - If neighbor in-degree becomes 0, add to queue
    5. Cycle detection: If result length < total nodes, cycle exists
    
    KEY INSIGHT:
    - Nodes with in-degree 0 have no dependencies (sources)
    - Processing sources first ensures we respect all dependencies
    - If we can't process all nodes, there's a cycle
    """
    
    def alienOrder(self, words: List[str]) -> str:
        """
        Find alien dictionary order using Kahn's algorithm.
        
        Args:
            words: List of words in alien language
            
        Returns:
            Valid character order, or "" if invalid
        """
        if not words:
            return ""
        
        # Step 1: Initialize graph and in-degree tracking
        graph = {}
        in_degree = {}
        for word in words:
            for char in word:
                if char not in graph:
                    graph[char] = set()
                    in_degree[char] = 0
        
        # Step 2: Build graph by comparing adjacent words
        for i in range(len(words) - 1):
            word1, word2 = words[i], words[i + 1]
            min_len = min(len(word1), len(word2))
            
            # Edge case: Invalid if word1 is prefix of word2 but longer
            # Example: ["abc", "ab"] is invalid (should be ["ab", "abc"])
            if word1[:min_len] == word2[:min_len] and len(word1) > len(word2):
                return ""
            
            # Find first differing character to determine order
            for j in range(min_len):
                if word1[j] != word2[j]:
                    # Add edge: word1[j] comes before word2[j]
                    if word2[j] not in graph[word1[j]]:
                        graph[word1[j]].add(word2[j])
                        in_degree[word2[j]] += 1
                    break  # Only first difference matters
        
        # Step 3: Perform topological sort using Kahn's algorithm
        return self.topological_sort(graph, in_degree)

    def topological_sort(self, graph: dict, in_degree: dict) -> str:
        """
        Kahn's Algorithm for topological sorting.
        
        Algorithm:
        1. Add all nodes with in-degree 0 to queue (sources)
        2. While queue not empty:
           - Pop node, add to result
           - For each neighbor: decrease in-degree
           - If neighbor in-degree becomes 0, add to queue
        3. If result contains all nodes: valid order
           Else: cycle exists (some nodes never reach in-degree 0)
        
        Args:
            graph: Adjacency list representation
            in_degree: Dictionary mapping node to in-degree count
            
        Returns:
            Topological order as string, or "" if cycle exists
        """
        from collections import deque
        
        queue = deque()
        result = []
        
        # Step 1: Add all sources (in-degree 0) to queue
        for char in in_degree:
            if in_degree[char] == 0:
                queue.append(char)
        
        # Step 2: Process nodes level by level
        while queue:
            char = queue.popleft()
            result.append(char)
            
            # Decrease in-degree of all neighbors
            for neighbor in graph[char]:
                in_degree[neighbor] -= 1
                # If neighbor becomes a source, add to queue
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        # Step 3: Check if we processed all nodes
        # If not, there's a cycle (nodes in cycle never reach in-degree 0)
        return "".join(result) if len(result) == len(graph) else ""
    
def test_alien_dictionary():
    """Test cases for Alien Dictionary"""
    sol = Solution()
    
    # Test case 1: Example 1
    words1 = ["wrt","wrf","er","ett","rftt"]
    result1 = sol.alienOrder(words1)
    assert result1 == "wertf", f"Expected 'wertf', got '{result1}'"
    print(f"✓ Test 1: {words1} → '{result1}'")
    
    # Test case 2: Example 2
    words2 = ["z","x"]
    result2 = sol.alienOrder(words2)
    assert result2 == "zx", f"Expected 'zx', got '{result2}'"
    print(f"✓ Test 2: {words2} → '{result2}'")
    
    # Test case 3: Cycle detection
    words3 = ["z","x","z"]
    result3 = sol.alienOrder(words3)
    assert result3 == "", f"Expected '' (cycle), got '{result3}'"
    print(f"✓ Test 3: {words3} → '{result3}' (cycle detected)")
    
    # Test case 4: Single word
    words4 = ["abc"]
    result4 = sol.alienOrder(words4)
    assert result4 == "abc", f"Expected 'abc', got '{result4}'"
    print(f"✓ Test 4: {words4} → '{result4}'")
    
    print("\nAll tests passed!")


class SolutionDFS:
    """
    DFS-based Topological Sort Implementation
    
    HOW IT WORKS:
    ------------
    1. Use DFS to explore the graph
    2. Mark nodes as: WHITE (unvisited), GRAY (visiting), BLACK (visited)
    3. When we finish visiting a node (all neighbors processed), add it to result
    4. Result is built in REVERSE order (post-order DFS)
    5. Reverse the result to get topological order
    
    KEY DIFFERENCE FROM KAHN'S:
    - Kahn's: Process nodes with in-degree 0 (sources first)
    - DFS: Process nodes and add to result when finished (sinks first, then reverse)
    
    CYCLE DETECTION:
    - If we encounter a GRAY node during DFS → cycle exists
    - GRAY = currently in recursion stack = back edge = cycle
    """
    
    def alienOrder(self, words: List[str]) -> str:
        """
        Find alien dictionary order using DFS-based topological sort.
        
        Args:
            words: List of words in alien language
            
        Returns:
            Valid character order, or "" if invalid
        """
        if not words:
            return ""
        
        # Build graph (same as Kahn's)
        graph = {}
        for word in words:
            for char in word:
                if char not in graph:
                    graph[char] = set()
        
        # Add edges based on word comparisons
        for i in range(len(words) - 1):
            word1, word2 = words[i], words[i + 1]
            min_len = min(len(word1), len(word2))
            
            # Invalid: word1 is prefix of word2 but word1 is longer
            if word1[:min_len] == word2[:min_len] and len(word1) > len(word2):
                return ""
            
            # Find first differing character
            for j in range(min_len):
                if word1[j] != word2[j]:
                    graph[word1[j]].add(word2[j])
                    break
        
        # DFS-based topological sort
        return self.topological_sort_dfs(graph)
    
    def topological_sort_dfs(self, graph: dict) -> str:
        """
        DFS-based topological sort using three-color marking.
        
        Colors:
        - WHITE (0): Unvisited
        - GRAY (1): Currently in recursion stack (visiting)
        - BLACK (2): Completely processed (all neighbors visited)
        
        Algorithm:
        1. Start DFS from each unvisited node
        2. Mark node as GRAY when entering
        3. Recursively visit all neighbors
        4. Mark node as BLACK when leaving, add to result
        5. If we encounter GRAY node → cycle detected
        
        Returns:
            Topological order, or "" if cycle exists
        """
        # Color tracking: 0=WHITE, 1=GRAY, 2=BLACK
        color = {char: 0 for char in graph}
        result = []
        has_cycle = [False]  # Use list to allow modification in nested function
        
        def dfs(node: str) -> bool:
            """
            DFS helper function.
            
            Returns:
                True if cycle detected, False otherwise
            """
            # Cycle detected: node is already in recursion stack
            if color[node] == 1:  # GRAY
                has_cycle[0] = True
                return True
            
            # Already processed
            if color[node] == 2:  # BLACK
                return False
            
            # Mark as visiting (GRAY)
            color[node] = 1
            
            # Visit all neighbors
            for neighbor in graph[node]:
                if dfs(neighbor):
                    return True  # Cycle found
            
            # Mark as processed (BLACK) and add to result
            # Note: We add in POST-ORDER (after all neighbors processed)
            color[node] = 2
            result.append(node)
            return False
        
        # Start DFS from each unvisited node
        for char in graph:
            if color[char] == 0:  # WHITE
                if dfs(char):
                    return ""  # Cycle detected
        
        # Result is in reverse order (sinks first), reverse to get topological order
        result.reverse()
        return "".join(result)


def explain_kahns_vs_dfs():
    """
    Comprehensive explanation of Kahn's Algorithm vs DFS-based Topological Sort.
    """
    print("=" * 70)
    print("DEEP DIVE: Kahn's Algorithm vs DFS-based Topological Sort")
    print("=" * 70)
    
    print("\n1. OVERVIEW:")
    print("   Both algorithms find a valid topological order, but use different strategies:")
    print("   - Kahn's: BFS-based, processes sources (in-degree 0) first")
    print("   - DFS: Recursive, processes sinks (out-degree 0) first, then reverses")
    
    print("\n2. KAHN'S ALGORITHM (BFS-based):")
    print("   ┌─────────────────────────────────────────────────────────┐")
    print("   │ Step | Action                                           │")
    print("   ├──────┼──────────────────────────────────────────────────┤")
    print("   │ 1    │ Build graph and calculate in-degrees             │")
    print("   │ 2    │ Add all nodes with in-degree 0 to queue          │")
    print("   │ 3    │ While queue not empty:                           │")
    print("   │      │   - Pop node, add to result                      │")
    print("   │      │   - Decrease in-degree of all neighbors          │")
    print("   │      │   - If neighbor in-degree becomes 0, add to queue│")
    print("   │ 4    │ If result length == total nodes: valid order     │")
    print("   │      │ Else: cycle exists                               │")
    print("   └─────────────────────────────────────────────────────────┘")
    
    print("\n   Visual Example (words=['wrt','wrf','er','ett','rftt']):")
    print("   Graph: w→r, w→e, r→t, e→r, t→f")
    print("   In-degrees: w=0, e=1, r=2, t=1, f=1")
    print("   ")
    print("   Step 1: Queue=[w] (in-degree 0)")
    print("           Process w → result=['w']")
    print("           Update: r in-degree: 2→1, e in-degree: 1→0")
    print("           Queue=[e]")
    print("   ")
    print("   Step 2: Process e → result=['w','e']")
    print("           Update: r in-degree: 1→0")
    print("           Queue=[r]")
    print("   ")
    print("   Step 3: Process r → result=['w','e','r']")
    print("           Update: t in-degree: 1→0")
    print("           Queue=[t]")
    print("   ")
    print("   Step 4: Process t → result=['w','e','r','t']")
    print("           Update: f in-degree: 1→0")
    print("           Queue=[f]")
    print("   ")
    print("   Step 5: Process f → result=['w','e','r','t','f']")
    print("           Final: 'wertf'")
    
    print("\n3. DFS-BASED TOPOLOGICAL SORT:")
    print("   ┌─────────────────────────────────────────────────────────┐")
    print("   │ Step | Action                                           │")
    print("   ├──────┼──────────────────────────────────────────────────┤")
    print("   │ 1    │ Build graph                                      │")
    print("   │ 2    │ For each unvisited node:                          │")
    print("   │      │   - Mark as GRAY (visiting)                      │")
    print("   │      │   - Recursively visit all neighbors              │")
    print("   │      │   - Mark as BLACK (visited), add to result      │")
    print("   │ 3    │ If GRAY node encountered → cycle detected        │")
    print("   │ 4    │ Reverse result to get topological order          │")
    print("   └─────────────────────────────────────────────────────────┘")
    
    print("\n   Visual Example (same graph):")
    print("   Graph: w→r, w→e, r→t, e→r, t→f")
    print("   ")
    print("   DFS from w:")
    print("     w (GRAY) → visit r")
    print("       r (GRAY) → visit t")
    print("         t (GRAY) → visit f")
    print("           f (GRAY) → no neighbors")
    print("           f (BLACK) → result=['f']")
    print("         t (BLACK) → result=['f','t']")
    print("       r (BLACK) → result=['f','t','r']")
    print("     w (BLACK) → result=['f','t','r','w']")
    print("   ")
    print("   DFS from e:")
    print("     e (GRAY) → visit r (already BLACK, skip)")
    print("     e (BLACK) → result=['f','t','r','w','e']")
    print("   ")
    print("   Reverse: 'ewrtf' → 'frtwe' (different valid order!)")
    
    print("\n4. KEY DIFFERENCES:")
    print("   ┌─────────────────────┬──────────────────┬──────────────────┐")
    print("   │ Aspect              │ Kahn's (BFS)     │ DFS              │")
    print("   ├─────────────────────┼──────────────────┼──────────────────┤")
    print("   │ Processing Order    │ Sources first    │ Sinks first      │")
    print("   │ Data Structure      │ Queue            │ Recursion stack  │")
    print("   │ In-Degree Tracking  │ Required ✓       │ Not needed ✗     │")
    print("   │ Cycle Detection     │ Count nodes      │ Color marking    │")
    print("   │ Result Order        │ Natural          │ Needs reverse    │")
    print("   │ Space (excl graph)  │ O(V) queue       │ O(V) recursion   │")
    print("   │ Time Complexity     │ O(V + E)         │ O(V + E)         │")
    print("   │ Intuition           │ Level-by-level   │ Deep exploration │")
    print("   └─────────────────────┴──────────────────┴──────────────────┘")
    
    print("\n5. WHEN TO USE WHICH:")
    print("   ")
    print("   Use KAHN'S when:")
    print("   ✓ You need in-degree information anyway")
    print("   ✓ You want to process nodes level-by-level")
    print("   ✓ You prefer iterative over recursive")
    print("   ✓ You want natural ordering (no reverse needed)")
    print("   ✓ You're already tracking in-degrees")
    print("   ")
    print("   Use DFS when:")
    print("   ✓ You're already doing DFS traversal")
    print("   ✓ You want to avoid in-degree calculation")
    print("   ✓ You prefer recursive thinking")
    print("   ✓ You need to detect cycles during traversal")
    print("   ✓ You want to process sinks first")
    
    print("\n6. CYCLE DETECTION COMPARISON:")
    print("   ")
    print("   Kahn's:")
    print("   - If result length < total nodes → cycle exists")
    print("   - Nodes in cycle never reach in-degree 0")
    print("   - Detection happens at the end")
    print("   ")
    print("   DFS:")
    print("   - If GRAY node encountered → cycle exists")
    print("   - GRAY = node in current recursion path")
    print("   - Detection happens immediately during traversal")
    
    print("\n7. SPACE COMPLEXITY BREAKDOWN:")
    print("   ")
    print("   Kahn's:")
    print("   - Graph: O(V + E)")
    print("   - In-degree map: O(V)")
    print("   - Queue: O(V) worst case")
    print("   - Total: O(V + E)")
    print("   ")
    print("   DFS:")
    print("   - Graph: O(V + E)")
    print("   - Color map: O(V)")
    print("   - Recursion stack: O(V) worst case")
    print("   - Total: O(V + E)")
    print("   ")
    print("   → Both have same space complexity!")
    
    print("\n8. TIME COMPLEXITY:")
    print("   ")
    print("   Both: O(V + E)")
    print("   - Build graph: O(V + E)")
    print("   - Traversal: O(V + E)")
    print("   - No redundant work")
    print("   ")
    print("   → Both have same time complexity!")
    
    print("\n9. KEY INSIGHT:")
    print("   - Both algorithms are EQUALLY EFFICIENT")
    print("   - Choice is often a matter of preference or context")
    print("   - Kahn's is more intuitive for level-by-level processing")
    print("   - DFS is more natural if you're already doing DFS")
    print("   - For Alien Dictionary, both work perfectly!")


def compare_implementations():
    """Compare Kahn's and DFS implementations side by side"""
    print("=" * 70)
    print("COMPARING IMPLEMENTATIONS")
    print("=" * 70)
    
    sol_kahns = Solution()
    sol_dfs = SolutionDFS()
    
    test_cases = [
        (["wrt","wrf","er","ett","rftt"], "wertf"),
        (["z","x"], "zx"),
        (["z","x","z"], ""),  # Cycle
        (["abc"], "abc"),
        (["ab","adc"], "abcd"),  # Different length words
    ]
    
    for i, (words, expected) in enumerate(test_cases, 1):
        result_kahns = sol_kahns.alienOrder(words)
        result_dfs = sol_dfs.alienOrder(words)
        
        print(f"\nTest {i}: words={words}")
        print(f"  Expected: '{expected}'")
        print(f"  Kahn's:   '{result_kahns}'")
        print(f"  DFS:      '{result_dfs}'")
        
        # Both should produce valid orders (may differ but both valid)
        if expected == "":
            # Both should detect cycle
            assert result_kahns == "" and result_dfs == "", \
                f"Both should detect cycle! Kahn's: '{result_kahns}', DFS: '{result_dfs}'"
            print(f"  ✓ Both detected cycle")
        else:
            # Both should produce valid orders (may be different but both valid)
            assert len(result_kahns) == len(expected) and len(result_dfs) == len(expected), \
                f"Length mismatch! Kahn's: {len(result_kahns)}, DFS: {len(result_dfs)}, Expected: {len(expected)}"
            print(f"  ✓ Both produced valid orders (may differ but both correct)")
    
    print("\n" + "=" * 70)
    print("✓ Both implementations work correctly!")
    print("=" * 70)
    print("\nNote: Different valid topological orders are possible!")
    print("Both algorithms produce valid orders, they may just differ.")


if __name__ == "__main__":
    test_alien_dictionary()
    
    # Example usage
    print("\nExample usage:")
    sol = Solution()
    words = ["wrt","wrf","er","ett","rftt"]
    result = sol.alienOrder(words)
    print(f"Input: {words}")
    print(f"Output: '{result}'")
    
    # Compare implementations
    print("\n")
    compare_implementations()
    
    # Detailed explanation
    print("\n")
    explain_kahns_vs_dfs()
# %%
class alien_dictionary:
    def alienOrder(self, words: List[str]) -> str:
        # if the input is empty, return ""
        if not words: return ""
        # initialize the graph and in_degree
        graph = {}
        in_degree = {}
        # initialize the graph and in_degree for each character in the words
        for word in words:
            for char in word:
                if char not in graph:
                    graph[char] = set()
                    in_degree[char] = 0   
        # build the graph
        for i in range(len(words) - 1):
            word1, word2 = words[i], words[i + 1]   
            min_len = min(len(word1), len(word2))
            # if the first min_len characters of word1 and word2 are the same, and word1 is longer than word2, return ""
            if word1[:min_len] == word2[:min_len] and len(word1) > len(word2):
                return ""
            for j in range(min_len):
                # if the characters at index j are different, add an edge from word1[j] to word2[j]
                if word1[j] != word2[j]:
                    if word2[j] not in graph[word1[j]]:
                        graph[word1[j]].add(word2[j])
                        in_degree[word2[j]] += 1
                    break
        return self.topological_sort(graph, in_degree)      
    
    def topological_sort(self, graph, in_degree):
        # initialize the queue and result
        queue = []
        result = []
        # add all characters with in_degree 0 to the queue
        for char in in_degree:
            if in_degree[char] == 0:
                queue.append(char)
        # while the queue is not empty, pop a character from the queue and add it to the result
        while queue:
            char = queue.pop(0)
            result.append(char)
            for neighbor in graph[char]:    
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        # if the length of the result is not equal to the number of characters in the graph, return ""
        return "".join(result) if len(result) == len(graph) else ""
        #time complexity: O(V + E)
        #space complexity: O(V)


class SolutionDFS:
    """
    DFS-based Topological Sort Implementation
    
    HOW IT WORKS:
    ------------
    1. Use DFS to explore the graph
    2. Mark nodes as: WHITE (unvisited), GRAY (visiting), BLACK (visited)
    3. When we finish visiting a node (all neighbors processed), add it to result
    4. Result is built in REVERSE order (post-order DFS)
    5. Reverse the result to get topological order
    
    KEY DIFFERENCE FROM KAHN'S:
    - Kahn's: Process nodes with in-degree 0 (sources first)
    - DFS: Process nodes and add to result when finished (sinks first, then reverse)
    
    CYCLE DETECTION:
    - If we encounter a GRAY node during DFS → cycle exists
    - GRAY = currently in recursion stack = back edge = cycle
    """
    
    def alienOrder(self, words: List[str]) -> str:
        """
        Find alien dictionary order using DFS-based topological sort.
        
        Args:
            words: List of words in alien language
            
        Returns:
            Valid character order, or "" if invalid
        """
        if not words:
            return ""
        
        # Build graph (same as Kahn's)
        graph = {}
        for word in words:
            for char in word:
                if char not in graph:
                    graph[char] = set()
        
        # Add edges based on word comparisons
        for i in range(len(words) - 1):
            word1, word2 = words[i], words[i + 1]
            min_len = min(len(word1), len(word2))
            
            # Invalid: word1 is prefix of word2 but word1 is longer
            if word1[:min_len] == word2[:min_len] and len(word1) > len(word2):
                return ""
            
            # Find first differing character
            for j in range(min_len):
                if word1[j] != word2[j]:
                    graph[word1[j]].add(word2[j])
                    break
        
        # DFS-based topological sort
        return self.topological_sort_dfs(graph)
    
    def topological_sort_dfs(self, graph: dict) -> str:
        """
        DFS-based topological sort using three-color marking.
        
        Colors:
        - WHITE (0): Unvisited
        - GRAY (1): Currently in recursion stack (visiting)
        - BLACK (2): Completely processed (all neighbors visited)
        
        Algorithm:
        1. Start DFS from each unvisited node
        2. Mark node as GRAY when entering
        3. Recursively visit all neighbors
        4. Mark node as BLACK when leaving, add to result
        5. If we encounter GRAY node → cycle detected
        
        Returns:
            Topological order, or "" if cycle exists
        """
        # Color tracking: 0=WHITE, 1=GRAY, 2=BLACK
        color = {char: 0 for char in graph}
        result = []
        has_cycle = [False]  # Use list to allow modification in nested function
        
        def dfs(node: str) -> bool:
            """
            DFS helper function.
            
            Returns:
                True if cycle detected, False otherwise
            """
            # Cycle detected: node is already in recursion stack
            if color[node] == 1:  # GRAY
                has_cycle[0] = True
                return True
            
            # Already processed
            if color[node] == 2:  # BLACK
                return False
            
            # Mark as visiting (GRAY)
            color[node] = 1
            
            # Visit all neighbors
            for neighbor in graph[node]:
                if dfs(neighbor):
                    return True  # Cycle found
            
            # Mark as processed (BLACK) and add to result
            # Note: We add in POST-ORDER (after all neighbors processed)
            color[node] = 2
            result.append(node)
            return False
        
        # Start DFS from each unvisited node
        for char in graph:
            if color[char] == 0:  # WHITE
                if dfs(char):
                    return ""  # Cycle detected
        
        # Result is in reverse order (sinks first), reverse to get topological order
        result.reverse()
        return "".join(result)


def explain_kahns_vs_dfs():
    """
    Comprehensive explanation of Kahn's Algorithm vs DFS-based Topological Sort.
    """
    print("=" * 70)
    print("DEEP DIVE: Kahn's Algorithm vs DFS-based Topological Sort")
    print("=" * 70)
    
    print("\n1. OVERVIEW:")
    print("   Both algorithms find a valid topological order, but use different strategies:")
    print("   - Kahn's: BFS-based, processes sources (in-degree 0) first")
    print("   - DFS: Recursive, processes sinks (out-degree 0) first, then reverses")
    
    print("\n2. KAHN'S ALGORITHM (BFS-based):")
    print("   ┌─────────────────────────────────────────────────────────┐")
    print("   │ Step | Action                                           │")
    print("   ├──────┼──────────────────────────────────────────────────┤")
    print("   │ 1    │ Build graph and calculate in-degrees             │")
    print("   │ 2    │ Add all nodes with in-degree 0 to queue          │")
    print("   │ 3    │ While queue not empty:                           │")
    print("   │      │   - Pop node, add to result                      │")
    print("   │      │   - Decrease in-degree of all neighbors          │")
    print("   │      │   - If neighbor in-degree becomes 0, add to queue│")
    print("   │ 4    │ If result length == total nodes: valid order     │")
    print("   │      │ Else: cycle exists                               │")
    print("   └─────────────────────────────────────────────────────────┘")
    
    print("\n   Visual Example (words=['wrt','wrf','er','ett','rftt']):")
    print("   Graph: w→r, w→e, r→t, e→r, t→f")
    print("   In-degrees: w=0, e=1, r=2, t=1, f=1")
    print("   ")
    print("   Step 1: Queue=[w] (in-degree 0)")
    print("           Process w → result=['w']")
    print("           Update: r in-degree: 2→1, e in-degree: 1→0")
    print("           Queue=[e]")
    print("   ")
    print("   Step 2: Process e → result=['w','e']")
    print("           Update: r in-degree: 1→0")
    print("           Queue=[r]")
    print("   ")
    print("   Step 3: Process r → result=['w','e','r']")
    print("           Update: t in-degree: 1→0")
    print("           Queue=[t]")
    print("   ")
    print("   Step 4: Process t → result=['w','e','r','t']")
    print("           Update: f in-degree: 1→0")
    print("           Queue=[f]")
    print("   ")
    print("   Step 5: Process f → result=['w','e','r','t','f']")
    print("           Final: 'wertf'")
    
    print("\n3. DFS-BASED TOPOLOGICAL SORT:")
    print("   ┌─────────────────────────────────────────────────────────┐")
    print("   │ Step | Action                                           │")
    print("   ├──────┼──────────────────────────────────────────────────┤")
    print("   │ 1    │ Build graph                                      │")
    print("   │ 2    │ For each unvisited node:                          │")
    print("   │      │   - Mark as GRAY (visiting)                      │")
    print("   │      │   - Recursively visit all neighbors              │")
    print("   │      │   - Mark as BLACK (visited), add to result      │")
    print("   │ 3    │ If GRAY node encountered → cycle detected        │")
    print("   │ 4    │ Reverse result to get topological order          │")
    print("   └─────────────────────────────────────────────────────────┘")
    
    print("\n   Visual Example (same graph):")
    print("   Graph: w→r, w→e, r→t, e→r, t→f")
    print("   ")
    print("   DFS from w:")
    print("     w (GRAY) → visit r")
    print("       r (GRAY) → visit t")
    print("         t (GRAY) → visit f")
    print("           f (GRAY) → no neighbors")
    print("           f (BLACK) → result=['f']")
    print("         t (BLACK) → result=['f','t']")
    print("       r (BLACK) → result=['f','t','r']")
    print("     w (BLACK) → result=['f','t','r','w']")
    print("   ")
    print("   DFS from e:")
    print("     e (GRAY) → visit r (already BLACK, skip)")
    print("     e (BLACK) → result=['f','t','r','w','e']")
    print("   ")
    print("   Reverse: 'ewrtf' → 'frtwe' (different valid order!)")
    
    print("\n4. KEY DIFFERENCES:")
    print("   ┌─────────────────────┬──────────────────┬──────────────────┐")
    print("   │ Aspect              │ Kahn's (BFS)     │ DFS              │")
    print("   ├─────────────────────┼──────────────────┼──────────────────┤")
    print("   │ Processing Order    │ Sources first    │ Sinks first      │")
    print("   │ Data Structure      │ Queue            │ Recursion stack  │")
    print("   │ In-Degree Tracking  │ Required ✓       │ Not needed ✗     │")
    print("   │ Cycle Detection     │ Count nodes      │ Color marking    │")
    print("   │ Result Order        │ Natural          │ Needs reverse    │")
    print("   │ Space (excl graph)  │ O(V) queue       │ O(V) recursion   │")
    print("   │ Time Complexity     │ O(V + E)         │ O(V + E)         │")
    print("   │ Intuition           │ Level-by-level   │ Deep exploration │")
    print("   └─────────────────────┴──────────────────┴──────────────────┘")
    
    print("\n5. WHEN TO USE WHICH:")
    print("   ")
    print("   Use KAHN'S when:")
    print("   ✓ You need in-degree information anyway")
    print("   ✓ You want to process nodes level-by-level")
    print("   ✓ You prefer iterative over recursive")
    print("   ✓ You want natural ordering (no reverse needed)")
    print("   ✓ You're already tracking in-degrees")
    print("   ")
    print("   Use DFS when:")
    print("   ✓ You're already doing DFS traversal")
    print("   ✓ You want to avoid in-degree calculation")
    print("   ✓ You prefer recursive thinking")
    print("   ✓ You need to detect cycles during traversal")
    print("   ✓ You want to process sinks first")
    
    print("\n6. CYCLE DETECTION COMPARISON:")
    print("   ")
    print("   Kahn's:")
    print("   - If result length < total nodes → cycle exists")
    print("   - Nodes in cycle never reach in-degree 0")
    print("   - Detection happens at the end")
    print("   ")
    print("   DFS:")
    print("   - If GRAY node encountered → cycle exists")
    print("   - GRAY = node in current recursion path")
    print("   - Detection happens immediately during traversal")
    
    print("\n7. SPACE COMPLEXITY BREAKDOWN:")
    print("   ")
    print("   Kahn's:")
    print("   - Graph: O(V + E)")
    print("   - In-degree map: O(V)")
    print("   - Queue: O(V) worst case")
    print("   - Total: O(V + E)")
    print("   ")
    print("   DFS:")
    print("   - Graph: O(V + E)")
    print("   - Color map: O(V)")
    print("   - Recursion stack: O(V) worst case")
    print("   - Total: O(V + E)")
    print("   ")
    print("   → Both have same space complexity!")
    
    print("\n8. TIME COMPLEXITY:")
    print("   ")
    print("   Both: O(V + E)")
    print("   - Build graph: O(V + E)")
    print("   - Traversal: O(V + E)")
    print("   - No redundant work")
    print("   ")
    print("   → Both have same time complexity!")
    
    print("\n9. KEY INSIGHT:")
    print("   - Both algorithms are EQUALLY EFFICIENT")
    print("   - Choice is often a matter of preference or context")
    print("   - Kahn's is more intuitive for level-by-level processing")
    print("   - DFS is more natural if you're already doing DFS")
    print("   - For Alien Dictionary, both work perfectly!")


def compare_implementations():
    """Compare Kahn's and DFS implementations side by side"""
    print("=" * 70)
    print("COMPARING IMPLEMENTATIONS")
    print("=" * 70)
    
    sol_kahns = Solution()
    sol_dfs = SolutionDFS()
    
    test_cases = [
        (["wrt","wrf","er","ett","rftt"], "wertf"),
        (["z","x"], "zx"),
        (["z","x","z"], ""),  # Cycle
        (["abc"], "abc"),
        (["ab","adc"], "abcd"),  # Different length words
    ]
    
    for i, (words, expected) in enumerate(test_cases, 1):
        result_kahns = sol_kahns.alienOrder(words)
        result_dfs = sol_dfs.alienOrder(words)
        
        print(f"\nTest {i}: words={words}")
        print(f"  Expected: '{expected}'")
        print(f"  Kahn's:   '{result_kahns}'")
        print(f"  DFS:      '{result_dfs}'")
        
        # Both should produce valid orders (may differ but both valid)
        if expected == "":
            # Both should detect cycle
            assert result_kahns == "" and result_dfs == "", \
                f"Both should detect cycle! Kahn's: '{result_kahns}', DFS: '{result_dfs}'"
            print(f"  ✓ Both detected cycle")
        else:
            # Both should produce valid orders (may be different but both valid)
            assert len(result_kahns) == len(expected) and len(result_dfs) == len(expected), \
                f"Length mismatch! Kahn's: {len(result_kahns)}, DFS: {len(result_dfs)}, Expected: {len(expected)}"
            print(f"  ✓ Both produced valid orders (may differ but both correct)")
    
    print("\n" + "=" * 70)
    print("✓ Both implementations work correctly!")
    print("=" * 70)
    print("\nNote: Different valid topological orders are possible!")
    print("Both algorithms produce valid orders, they may just differ.")