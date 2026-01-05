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
   - Topological sort vs DFS: Topological sort is more efficient for this problem
   - Cycle detection: We handle cycles by returning empty string

"""
from typing import List

class Solution:
    def alienOrder(self, words: List[str]) -> str:
        if not words: return ""
        graph = {}
        in_degree = {}
        for word in words:
            for char in word:
                if char not in graph:
                    graph[char] = set()
                    in_degree[char] = 0         
        for i in range(len(words) - 1):
            word1, word2 = words[i], words[i + 1]
            min_len = min(len(word1), len(word2))
            if word1[:min_len] == word2[:min_len] and len(word1) > len(word2):
                return ""
            for j in range(min_len):
                if word1[j] != word2[j]:
                    if word2[j] not in graph[word1[j]]:
                        graph[word1[j]].add(word2[j])
                        in_degree[word2[j]] += 1
                    break
        return self.topological_sort(graph, in_degree)      

    def topological_sort(self, graph, in_degree):
        queue = []
        result = []
        for char in in_degree:
            if in_degree[char] == 0:
                queue.append(char)
        while queue:
            char = queue.pop(0)
            result.append(char)
            for neighbor in graph[char]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)      
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


if __name__ == "__main__":
    test_alien_dictionary()
    
    # Example usage
    print("\nExample usage:")
    sol = Solution()
    words = ["wrt","wrf","er","ett","rftt"]
    result = sol.alienOrder(words)
    print(f"Input: {words}")
    print(f"Output: '{result}'")
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