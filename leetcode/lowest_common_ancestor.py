# LeetCode 236: Lowest Common Ancestor of a Binary Tree
#%%
"""
Problem Statement:
Given a binary tree, find the lowest common ancestor (LCA) of two given nodes in the tree.

According to the definition of LCA on Wikipedia: "The lowest common ancestor is defined between
two nodes p and q as the lowest node in T that has both p and q as descendants (where we allow
a node to be a descendant of itself)."

Example 1:
Input: root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 1
Output: 3
Explanation: The LCA of nodes 5 and 1 is 3.

Example 2:
Input: root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 4
Output: 5
Explanation: The LCA of nodes 5 and 4 is 5, since a node can be a descendant of itself
according to the LCA definition.

Example 3:
Input: root = [1,2], p = 1, q = 2
Output: 1

INTERVIEW EXPLANATION: Why DFS for Lowest Common Ancestor?

1. **Problem Structure**: We need to find the deepest node that is an ancestor of both p and q.
   This requires traversing the tree and tracking where we find p and q.

2. **Why DFS?**
   - **Tree Traversal**: Need to explore the tree to find p and q
   - **Bottom-Up**: After finding p and q, propagate information upward
   - **Recursive Structure**: Natural fit for tree problems
   - **Single Pass**: Can find LCA in one traversal

3. **IS THIS TOP-DOWN OR BOTTOM-UP?**
   - **BOTTOM-UP** DFS (despite traversing top-down!)
   - We traverse DOWN (root → leaves) but information flows UP (leaves → root)
   - Decisions are made based on SUBTREE RESULTS (bottom-up)
   - LCA is determined when we have information from both subtrees
   - Return values propagate upward from children to parent

4. **Algorithm**:
   a. DFS from root (traverse down)
   b. If current node is None, return None
   c. If current node is p or q, return current node (base case)
   d. Recursively search left and right subtrees (get results from below)
   e. If both left and right return non-None, current node is LCA (decision based on children)
   f. Otherwise, return whichever subtree found a node (propagate upward)

5. **Key Insights**:
   - If we find p in left subtree and q in right subtree, current node is LCA
   - If both p and q in same subtree, LCA is in that subtree
   - If current node is p or q, it might be the LCA (if other is in subtree)
   - **Bottom-up nature**: Can't decide if node is LCA until children report back

6. **Time Complexity**: O(n) - visit each node at most once
   
7. **Space Complexity**: O(h) where h is height (recursion stack)
   
8. **Memoization**: NOT needed - each node visited once, no overlapping subproblems
"""


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution:
    """Solution for Lowest Common Ancestor"""
    
    def lowestCommonAncestor(self, root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
        """
        Find lowest common ancestor of p and q.
        
        IS THIS TOP-DOWN OR BOTTOM-UP?
        ------------------------------
        This is **BOTTOM-UP** DFS, even though we traverse top-down!
        
        Why BOTTOM-UP?
        --------------
        1. **Information Flow**: Information flows UP from children to parent
           - We traverse down (root → leaves)
           - But decisions are made going UP (leaves → root)
           - Return values propagate upward
        
        2. **Decision Making**: Decisions depend on SUBTREE RESULTS
           - We don't know if current node is LCA until we check subtrees
           - LCA decision: "If both subtrees found p and q, I'm the LCA"
           - This requires information FROM BELOW (bottom-up)
        
        3. **Base Cases**: Base cases are at leaves, answer built going up
           - Base: Found p/q or None at leaves
           - Build: Combine results from children
           - Result: Propagate upward
        
        Visual Example (p=5, q=4):
        --------------------------
        Tree structure:
                3
               / \
              5   1
             / \
            6   2
               / \
              7   4
        
        Execution flow (BOTTOM-UP):
        - Traverse DOWN: 3 → 5 → 6 (leaf, return None)
        - Traverse DOWN: 3 → 5 → 2 → 7 (leaf, return None)
        - Traverse DOWN: 3 → 5 → 2 → 4 (found q, return 4)
        - At node 2: left=None, right=4 → return 4 (propagate UP)
        - At node 5: left=None, right=4, and node 5 == p → return 5 (LCA!)
        - At node 3: left=5, right=None → return 5 (propagate UP)
        
        Key Insight:
        - We TRAVERSE top-down (root → leaves)
        - But we DECIDE bottom-up (leaves → root)
        - The LCA is determined when we have information from both subtrees
        
        Why NOT Top-Down?
        ----------------
        Top-down would mean:
        - Pass information DOWN as parameters
        - Make decisions going DOWN
        - Example: "I know p is in left subtree, so LCA must be in left"
        - But we don't know where p/q are until we search!
        
        Args:
            root: Root of binary tree
            p: First node
            q: Second node
            
        Returns:
            Lowest common ancestor node
        """
        # Base cases
        if root is None:
            return None
        
        # If we found p or q, return it (base case - found at current node)
        if root == p or root == q:
            return root
        
        # Search in left and right subtrees (traverse DOWN)
        # But results come BACK UP (bottom-up information flow)
        left = self.lowestCommonAncestor(root.left, p, q)
        right = self.lowestCommonAncestor(root.right, p, q)
        
        # Decision made based on SUBTREE RESULTS (bottom-up decision)
        # If both subtrees return non-None, current node is LCA
        if left and right:
            return root
        
        # Otherwise, propagate result UPWARD (bottom-up propagation)
        return left if left else right
    
    def lowestCommonAncestor_verbose(self, root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
        """
        More verbose version with detailed comments.
        """
        # Base case: empty tree
        if not root:
            return None
        
        # Case 1: Current node is one of p or q
        # This node might be the LCA if the other node is in its subtree
        if root == p or root == q:
            return root
        
        # Recursively search in left and right subtrees
        left_result = self.lowestCommonAncestor_verbose(root.left, p, q)
        right_result = self.lowestCommonAncestor_verbose(root.right, p, q)
        
        # Case 2: p and q are in different subtrees
        # Current node is the LCA
        if left_result and right_result:
            return root
        
        # Case 3: Both p and q are in the same subtree
        # Return the result from that subtree (which is the LCA)
        if left_result:
            return left_result
        if right_result:
            return right_result
        
        # Case 4: Neither p nor q found in this subtree
        return None


def test_lowest_common_ancestor():
    """Test cases for Lowest Common Ancestor"""
    # Note: Creating full test cases requires building trees
    # This is a simplified test structure
    
    sol = Solution()
    
    # Test case 1: Example 1 structure
    # Tree: [3,5,1,6,2,0,8,null,null,7,4]
    # p = 5, q = 1, LCA = 3
    root1 = TreeNode(3)
    root1.left = TreeNode(5)
    root1.right = TreeNode(1)
    root1.left.left = TreeNode(6)
    root1.left.right = TreeNode(2)
    root1.right.left = TreeNode(0)
    root1.right.right = TreeNode(8)
    root1.left.right.left = TreeNode(7)
    root1.left.right.right = TreeNode(4)
    
    p1 = root1.left  # 5
    q1 = root1.right  # 1
    result1 = sol.lowestCommonAncestor(root1, p1, q1)
    assert result1 == root1, f"Expected root (3), got {result1.val if result1 else None}"
    print(f"✓ Test 1: p=5, q=1, LCA={result1.val}")
    
    # Test case 2: Example 2
    # p = 5, q = 4, LCA = 5
    p2 = root1.left  # 5
    q2 = root1.left.right.right  # 4
    result2 = sol.lowestCommonAncestor(root1, p2, q2)
    assert result2 == p2, f"Expected 5, got {result2.val if result2 else None}"
    print(f"✓ Test 2: p=5, q=4, LCA={result2.val}")
    
    # Test case 3: Example 3
    # Tree: [1,2]
    root3 = TreeNode(1)
    root3.left = TreeNode(2)
    p3 = root3  # 1
    q3 = root3.left  # 2
    result3 = sol.lowestCommonAncestor(root3, p3, q3)
    assert result3 == root3, f"Expected 1, got {result3.val if result3 else None}"
    print(f"✓ Test 3: p=1, q=2, LCA={result3.val}")
    
    print("\nAll tests passed!")


def explain_top_down_vs_bottom_up_lca():
    """
    Comprehensive explanation of why LCA is BOTTOM-UP, not top-down.
    """
    print("=" * 70)
    print("TOP-DOWN vs BOTTOM-UP: Lowest Common Ancestor")
    print("=" * 70)
    
    print("\n1. THE CONFUSION:")
    print("   - We TRAVERSE top-down (root → leaves)")
    print("   - But we DECIDE bottom-up (leaves → root)")
    print("   - This is BOTTOM-UP DFS!")
    
    print("\n2. WHY IT'S BOTTOM-UP:")
    print("   ┌─────────────────────────────────────────────────────────┐")
    print("   │ Aspect              │ LCA Algorithm                   │")
    print("   ├─────────────────────┼─────────────────────────────────┤")
    print("   │ Traversal Direction │ Top-Down (root → leaves)        │")
    print("   │ Information Flow    │ Bottom-Up (leaves → root) ✓     │")
    print("   │ Decision Making     │ Based on subtree results ✓      │")
    print("   │ Base Cases          │ At leaves (bottom) ✓            │")
    print("   │ Answer Construction │ Built going up ✓                │")
    print("   │ Return Values       │ Propagate upward ✓              │")
    print("   └─────────────────────┴─────────────────────────────────┘")
    
    print("\n3. VISUAL EXAMPLE: p=5, q=4")
    print("   Tree:")
    print("           3")
    print("          / \\")
    print("         5   1")
    print("        / \\")
    print("       6   2")
    print("          / \\")
    print("         7   4")
    print("")
    print("   Execution (showing bottom-up information flow):")
    print("   Step 1: Traverse DOWN to node 6 (leaf)")
    print("           → Return None (not p or q)")
    print("   Step 2: Traverse DOWN to node 7 (leaf)")
    print("           → Return None (not p or q)")
    print("   Step 3: Traverse DOWN to node 4 (leaf)")
    print("           → Return 4 (found q!) ← BASE CASE")
    print("   Step 4: At node 2: left=None, right=4")
    print("           → Return 4 (propagate UP)")
    print("   Step 5: At node 5: left=None, right=4, and node 5 == p")
    print("           → Return 5 (I'm the LCA!) ← DECISION MADE")
    print("   Step 6: At node 3: left=5, right=None")
    print("           → Return 5 (propagate UP)")
    print("")
    print("   Key: Decision at node 5 depends on SUBTREE RESULTS (bottom-up)!")
    
    print("\n4. COMPARISON: Top-Down vs Bottom-Up in Trees")
    print("   ┌─────────────────────┬──────────────────┬──────────────────┐")
    print("   │ Aspect              │ Top-Down         │ Bottom-Up        │")
    print("   ├─────────────────────┼──────────────────┼──────────────────┤")
    print("   │ Information Flow    │ Down (params)    │ Up (return)      │")
    print("   │ Decision Making     │ Going down       │ Going up         │")
    print("   │ Base Cases          │ At root          │ At leaves        │")
    print("   │ Example             │ Path sum         │ LCA, max depth    │")
    print("   │ LCA Approach        │ ✗ Not suitable   │ ✓ This problem   │")
    print("   └─────────────────────┴──────────────────┴──────────────────┘")
    
    print("\n5. WHY LCA MUST BE BOTTOM-UP:")
    print("   - We don't know where p and q are until we search")
    print("   - LCA decision requires knowing what's in BOTH subtrees")
    print("   - Can't decide 'I'm the LCA' until children report back")
    print("   - Information must flow UP from children to parent")
    
    print("\n6. WHAT IF IT WERE TOP-DOWN?")
    print("   Top-down LCA would look like:")
    print("   ```python")
    print("   def lca_topdown(root, p, q, found_p=False, found_q=False):")
    print("       # Pass information DOWN")
    print("       if root == p: found_p = True")
    print("       if root == q: found_q = True")
    print("       # But we still need to check subtrees!")
    print("       # Can't make decision until we know what's below")
    print("   ```")
    print("   → This doesn't work! We need subtree results first.")
    
    print("\n7. KEY INSIGHT:")
    print("   - Traversal direction ≠ Information flow direction")
    print("   - LCA: Traverse DOWN, but information flows UP")
    print("   - Decision: 'Am I the LCA?' depends on children's results")
    print("   - Therefore: BOTTOM-UP approach")
    
    print("\n8. MEMOIZATION?")
    print("   - LCA doesn't need memoization")
    print("   - Each node visited exactly once")
    print("   - No overlapping subproblems")
    print("   - O(n) time, O(h) space (recursion stack)")


if __name__ == "__main__":
    test_lowest_common_ancestor()
    
    # Example usage
    print("\nExample usage:")
    sol = Solution()
    
    # Build example tree
    root = TreeNode(3)
    root.left = TreeNode(5)
    root.right = TreeNode(1)
    root.left.left = TreeNode(6)
    root.left.right = TreeNode(2)
    root.right.left = TreeNode(0)
    root.right.right = TreeNode(8)
    
    p = root.left  # 5
    q = root.right  # 1
    lca = sol.lowestCommonAncestor(root, p, q)
    print(f"LCA of {p.val} and {q.val} is {lca.val}")
    
    # Detailed explanation
    print("\n")
    explain_top_down_vs_bottom_up_lca()
# %%

