# Tree-based File System
#%%
"""
Problem Statement:
Implement a tree-based data structure that supports three operations:

1. create(path, value)
   - path is a string like "NA/MX"
   - This means: under the node "NA", create a new child node "MX" with the given value
   - The parent node must already exist
   - If the node already exists, or the parent does not exist, the operation fails

2. set_value(path, value)
   - Finds the node at path
   - If the node exists and it is a leaf (no children), set its value
   - Otherwise (if the node doesn't exist or it has children), return False

3. get_value(path)
   - Finds the node at path
   - If the node exists and it is a leaf, return its value
   - Otherwise (node not found or not a leaf), return None

Example Tree:
root
 ├─ NA
 │   ├─ CA
 │   └─ US
 └─ EU

- create("NA", "val_NA") → success
- create("NA/CA", "val_CA") → success
- get_value("NA") → None (not a leaf)
- get_value("NA/CA") → "val_CA"
- set_value("NA", "x") → False (NA is not a leaf)
- set_value("NA/CA", "new_CA") → success, value updated

INTERVIEW EXPLANATION: Why Tree Structure for File System?

1. **Problem Structure**: We need to represent a hierarchical file system where:
   - Each node can have children (directories)
   - Only leaf nodes can have values (files)
   - Paths are represented as "/" separated strings

2. **Why Tree Structure?**
   - **Hierarchical Nature**: File systems are naturally hierarchical (parent-child relationships)
   - **Path Traversal**: Tree structure makes path navigation O(depth) where depth is path length
   - **Memory Efficient**: Only stores nodes that exist, not all possible paths
   
3. **Key Design Decisions**:
   - **Node Class**: Each node has name, value, and children dictionary
   - **Root Node**: Special empty root node to handle absolute paths
   - **Leaf Check**: Only leaf nodes (no children) can have/get values
   - **Path Parsing**: Split path by "/" and traverse from root

4. **Time Complexity**:
   - create: O(d) where d = depth (path length)
   - set_value: O(d)
   - get_value: O(d)

5. **Space Complexity**: O(n) where n = total number of nodes
"""

from typing import Any, Dict, Optional, List


class Node:
    """Represents a node in the file system tree"""
    
    def __init__(self, name: str, value: Optional[Any] = None):
        self.name = name
        self.value = value
        self.children: Dict[str, 'Node'] = {}
    
    def is_leaf(self) -> bool:
        """Check if node is a leaf (has no children)"""
        return len(self.children) == 0


class PathTree:
    """Tree-based file system implementation"""
    
    def __init__(self):
        self.root = Node("")  # Root has no value
    
    def _split(self, path: str) -> List[str]:
        """Split path string into parts, removing empty strings"""
        return [p for p in path.strip().split("/") if p]
    
    def _find_node(self, parts: List[str]) -> Optional[Node]:
        """Find node at given path parts"""
        cur = self.root
        for p in parts:
            if p not in cur.children:
                return None
            cur = cur.children[p]
        return cur
    
    def create(self, path: str, value: Any) -> bool:
        """
        Create a new node at the given path.
        
        Args:
            path: Path string like "NA/MX"
            value: Value to assign to the new node
            
        Returns:
            True if successful, False otherwise
        """
        parts = self._split(path)
        if not parts:
            return False  # Cannot create at root
        
        parent_parts, child_name = parts[:-1], parts[-1]
        parent = self._find_node(parent_parts) if parent_parts else self.root
        
        if parent is None or child_name in parent.children:
            return False  # Parent doesn't exist or child already exists
        
        parent.children[child_name] = Node(child_name, value)
        return True
    
    def set_value(self, path: str, value: Any) -> bool:
        """
        Set value of a leaf node at the given path.
        
        Args:
            path: Path string
            value: Value to set
            
        Returns:
            True if successful, False otherwise
        """
        node = self._find_node(self._split(path))
        if node is None or not node.is_leaf():
            return False
        node.value = value
        return True
    
    def get_value(self, path: str) -> Optional[Any]:
        """
        Get value of a leaf node at the given path.
        
        Args:
            path: Path string
            
        Returns:
            Value if node exists and is a leaf, None otherwise
        """
        node = self._find_node(self._split(path))
        if node is None or not node.is_leaf():
            return None
        return node.value


def test_tree_file_system():
    """Test cases for Tree-based File System"""
    tree = PathTree()
    
    # Test 1: Create nodes
    assert tree.create("NA", "val_NA") == True, "Should create NA"
    assert tree.create("NA/CA", "val_CA") == True, "Should create NA/CA"
    assert tree.create("NA/US", "val_US") == True, "Should create NA/US"
    assert tree.create("EU", "val_EU") == True, "Should create EU"
    print("✓ Test 1: Created nodes successfully")
    
    # Test 2: Get values
    assert tree.get_value("NA") == None, "NA is not a leaf, should return None"
    assert tree.get_value("NA/CA") == "val_CA", "Should get value for leaf"
    assert tree.get_value("NA/US") == "val_US", "Should get value for leaf"
    assert tree.get_value("EU") == "val_EU", "Should get value for leaf"
    print("✓ Test 2: Get values works correctly")
    
    # Test 3: Set values
    assert tree.set_value("NA", "x") == False, "NA is not a leaf, should fail"
    assert tree.set_value("NA/CA", "new_CA") == True, "Should update leaf value"
    assert tree.get_value("NA/CA") == "new_CA", "Should get updated value"
    print("✓ Test 3: Set values works correctly")
    
    # Test 4: Edge cases
    assert tree.create("NA", "duplicate") == False, "Should fail - node exists"
    assert tree.create("NA/MX/CA", "nested") == False, "Should fail - parent MX doesn't exist"
    assert tree.get_value("nonexistent") == None, "Should return None for nonexistent path"
    assert tree.set_value("nonexistent", "x") == False, "Should fail for nonexistent path"
    print("✓ Test 4: Edge cases handled correctly")
    
    print("\nAll tests passed!")


if __name__ == "__main__":
    test_tree_file_system()
    
    # Example usage
    print("\nExample usage:")
    tree = PathTree()
    
    # Build example tree
    tree.create("NA", "val_NA")
    tree.create("NA/CA", "val_CA")
    tree.create("NA/US", "val_US")
    tree.create("EU", "val_EU")
    
    # Get values
    print(f"get_value('NA'): {tree.get_value('NA')}")  # None (not a leaf)
    print(f"get_value('NA/CA'): {tree.get_value('NA/CA')}")  # val_CA
    
    # Set value
    tree.set_value("NA/CA", "new_CA")
    print(f"get_value('NA/CA' after update: {tree.get_value('NA/CA')}")  # new_CA
# %%

