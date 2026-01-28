# LeetCode 1257: Smallest Common Region
#%%
"""
Problem Statement:
You are given a list of regions, where each element in regions is itself a list of strings.
In each of these lists, the first string denotes a region that contains all the other 
regions in that list.

A region X is said to contain another region Y if X is bigger or a parent region of Y.
By definition, a region also contains itself.

Given two region names, region1 and region2, you need to find the smallest region that 
contains both of them.

Example 1:
Input:
regions = [
  ["Earth","North America","South America"],
  ["North America","United States","Canada"],
  ["United States","New York","Boston"],
  ["Canada","Ontario","Quebec"],
  ["South America","Brazil"]
],
region1 = "Quebec",
region2 = "New York"
Output: "North America"
Explanation: North America is the smallest region that contains both Quebec and New York.

Example 2:
Input:
regions = [
  ["Earth", "North America", "South America"],
  ["North America", "United States", "Canada"],
  ["United States", "New York", "Boston"],
  ["Canada", "Ontario", "Quebec"],
  ["South America", "Brazil"]
],
region1 = "Canada",
region2 = "South America"
Output: "Earth"
Explanation: Only Earth contains both Canada and South America.

Constraints:
- 2 <= regions.length <= 10^4
- For each list in regions, 2 <= regions[i].length <= 20
- Lengths of region strings are between 1 and 20
- All strings are composed of English letters
- region1 != region2
- The smallest common region always exists

INTERVIEW EXPLANATION: Why Tree/LCA Approach for Smallest Common Region?

1. **Problem Structure**: The regions form a tree structure where:
   - Each region list represents a parent-child relationship
   - First element is parent, rest are children
   - This creates a hierarchy (like a file system or organizational chart)
   - We need to find the Lowest Common Ancestor (LCA) of two nodes

2. **Why Tree/LCA Approach?**
   - **Tree Structure**: The parent-child relationships naturally form a tree
   - **LCA Problem**: Finding the smallest common region is exactly finding LCA
   - **Efficient Solution**: Can solve in O(h) time where h is tree height
   
3. **Key Insights**:
   - **Build Parent Map**: Create a mapping from each region to its parent
   - **Path to Root**: Find all ancestors of region1 (path from region1 to root)
   - **Find Common Ancestor**: Traverse from region2 up to root, return first 
     ancestor that's also an ancestor of region1
   - **Alternative**: Build both paths and find their intersection point

4. **Algorithm**:
   a. Build parent mapping: for each region list, map children to parent
   b. Find all ancestors of region1 (including itself)
   c. Traverse from region2 up to root:
      - If current region is in region1's ancestors, return it (this is LCA)
      - Otherwise, move to parent
   d. Guaranteed to find answer since root contains everything

5. **Time Complexity**: O(n) where n is number of regions
   - Building parent map: O(n)
   - Finding ancestors: O(h) where h is height
   - Finding LCA: O(h)
   - Overall: O(n) since we process each region once

6. **Space Complexity**: O(n) for parent map and ancestor set
"""

from typing import List


class Solution:
    """Solution for Smallest Common Region"""
    
    def findSmallestRegion(self, regions: List[List[str]], 
                          region1: str, region2: str) -> str:
        """
        Find the smallest common region containing both region1 and region2.
        
        Args:
            regions: List of region lists, first element is parent
            region1: First region name
            region2: Second region name
            
        Returns:
            Name of the smallest common region
        """
        # Build parent mapping: child -> parent
        parent = {}
        
        for region_list in regions:
            # First element is parent, rest are children
            parent_region = region_list[0]
            for child in region_list[1:]:
                parent[child] = parent_region
        
        # Find all ancestors of region1 (including itself)
        ancestors = set()
        current = region1
        
        # Traverse from region1 up to root
        while current:
            ancestors.add(current)
            current = parent.get(current)  # Move to parent
        
        # Traverse from region2 up to root
        # First common ancestor we encounter is the LCA
        current = region2
        while current:
            if current in ancestors:
                return current  # Found LCA
            current = parent.get(current)
        
        # Should never reach here given constraints
        return None
    
    def findSmallestRegion_path_based(self, regions: List[List[str]], 
                                     region1: str, region2: str) -> str:
        """
        Alternative approach: build paths from both regions to root,
        then find the last common node.
        """
        # Build parent mapping
        parent = {}
        for region_list in regions:
            parent_region = region_list[0]
            for child in region_list[1:]:
                parent[child] = parent_region
        
        # Build path from region1 to root
        def get_path_to_root(region: str) -> List[str]:
            path = []
            current = region
            while current:
                path.append(current)
                current = parent.get(current)
            return path
        
        path1 = get_path_to_root(region1)
        path2 = get_path_to_root(region2)
        
        # Convert to sets for easier lookup
        path1_set = set(path1)
        
        # Find first node in path2 that's also in path1
        for node in path2:
            if node in path1_set:
                return node
        
        return None
    
    def findSmallestRegion_dfs(self, regions: List[List[str]], 
                              region1: str, region2: str) -> str:
        """
        DFS-based approach: build the tree and use DFS to find LCA.
        """
        # Build parent mapping and also child mapping for tree structure
        parent = {}
        children = {}
        
        for region_list in regions:
            parent_region = region_list[0]
            if parent_region not in children:
                children[parent_region] = []
            
            for child in region_list[1:]:
                parent[child] = parent_region
                children[parent_region].append(child)
        
        # Find root (region with no parent)
        root = None
        for region_list in regions:
            if region_list[0] not in parent:
                root = region_list[0]
                break
        
        # DFS to find LCA
        def find_lca(node: str) -> tuple:
            """
            Returns (found_region1, found_region2, lca_node)
            """
            found1 = (node == region1)
            found2 = (node == region2)
            lca = None
            
            # Check children
            for child in children.get(node, []):
                child_found1, child_found2, child_lca = find_lca(child)
                found1 = found1 or child_found1
                found2 = found2 or child_found2
                
                if child_lca:
                    lca = child_lca
            
            # If we found both regions in this subtree, and haven't found LCA yet,
            # this node is the LCA
            if found1 and found2 and lca is None:
                lca = node
            
            return found1, found2, lca
        
        _, _, lca = find_lca(root)
        return lca


def test_smallest_common_region():
    """Test cases for Smallest Common Region"""
    sol = Solution()
    
    # Test case 1: Example 1
    regions1 = [
        ["Earth","North America","South America"],
        ["North America","United States","Canada"],
        ["United States","New York","Boston"],
        ["Canada","Ontario","Quebec"],
        ["South America","Brazil"]
    ]
    result1 = sol.findSmallestRegion(regions1, "Quebec", "New York")
    assert result1 == "North America", f"Expected 'North America', got '{result1}'"
    print(f"✓ Test 1: region1='Quebec', region2='New York'")
    print(f"  Result: {result1}")
    
    # Test case 2: Example 2
    regions2 = [
        ["Earth", "North America", "South America"],
        ["North America", "United States", "Canada"],
        ["United States", "New York", "Boston"],
        ["Canada", "Ontario", "Quebec"],
        ["South America", "Brazil"]
    ]
    result2 = sol.findSmallestRegion(regions2, "Canada", "South America")
    assert result2 == "Earth", f"Expected 'Earth', got '{result2}'"
    print(f"✓ Test 2: region1='Canada', region2='South America'")
    print(f"  Result: {result2}")
    
    # Test case 3: Same parent
    regions3 = [
        ["A", "B", "C"],
        ["B", "D", "E"]
    ]
    result3 = sol.findSmallestRegion(regions3, "D", "E")
    assert result3 == "B", f"Expected 'B', got '{result3}'"
    print(f"✓ Test 3: region1='D', region2='E' (same parent)")
    print(f"  Result: {result3}")
    
    # Test case 4: One is ancestor of the other
    regions4 = [
        ["A", "B", "C"],
        ["B", "D"]
    ]
    result4 = sol.findSmallestRegion(regions4, "B", "D")
    assert result4 == "B", f"Expected 'B', got '{result4}'"
    print(f"✓ Test 4: region1='B', region2='D' (B is ancestor of D)")
    print(f"  Result: {result4}")
    
    # Test case 5: Root is the answer
    regions5 = [
        ["Root", "A", "B"],
        ["A", "C"]
    ]
    result5 = sol.findSmallestRegion(regions5, "C", "B")
    assert result5 == "Root", f"Expected 'Root', got '{result5}'"
    print(f"✓ Test 5: region1='C', region2='B' (root is LCA)")
    print(f"  Result: {result5}")
    
    print("\nAll tests passed!")
    
    # Test alternative approaches
    print("\nTesting path-based approach:")
    result1_path = sol.findSmallestRegion_path_based(regions1, "Quebec", "New York")
    assert result1_path == "North America", "Path-based approach failed"
    print(f"✓ Path-based Test 1: {result1_path}")
    
    print("\nTesting DFS approach:")
    result1_dfs = sol.findSmallestRegion_dfs(regions1, "Quebec", "New York")
    assert result1_dfs == "North America", "DFS approach failed"
    print(f"✓ DFS Test 1: {result1_dfs}")


if __name__ == "__main__":
    test_smallest_common_region()
    
    # Example usage
    print("\nExample usage:")
    sol = Solution()
    
    regions = [
        ["Earth","North America","South America"],
        ["North America","United States","Canada"],
        ["United States","New York","Boston"],
        ["Canada","Ontario","Quebec"],
        ["South America","Brazil"]
    ]
    
    region1 = "Quebec"
    region2 = "New York"
    result = sol.findSmallestRegion(regions, region1, region2)
    
    print(f"Input:")
    print(f"  regions = {regions}")
    print(f"  region1 = '{region1}'")
    print(f"  region2 = '{region2}'\n")
    print(f"Output: '{result}'")
# %%
