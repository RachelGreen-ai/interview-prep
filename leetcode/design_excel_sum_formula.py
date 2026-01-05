# LeetCode 631: Design Excel Sum Formula
#%%
"""
Problem Statement:
Design the basic function of Excel and implement the sum function.

Implement the Excel class:
- Excel(int height, char width) Initializes the object with the height and the width of the sheet.
  The sheet is an integer matrix mat of size height x width with the row index in the range [1, height]
  and the column index in the range ['A', width]. The value at Mat(row, column) is 0.
  
- void set(int row, char column, int val) Sets the value at Mat(row, column) to be val.
  
- int get(int row, char column) Returns the value at Mat(row, column).
  
- int sum(int row, char column, List[str> numbers) Sets the value at Mat(row, column) to be the sum
  of cells represented by numbers and returns the value. numbers[i] could be on the format:
  - "ColRow" that represents a single cell.
  - "ColRow1:ColRow2" that represents a range of cells. (where Col = column, Row = row)
  
Note: You could assume that there won't be any circular sum reference. For example, A1 = sum(B1) and B1 = sum(A1).

Example 1:
Input:
["Excel", "set", "sum", "set", "get"]
[[3, "C"], [1, "A", 2], [3, "C", ["A1", "A1:B2"]], [2, "B", 2], [3, "C"]]
Output: [null, null, 4, null, 6]

Explanation:
Excel excel = new Excel(3, "C");
// construct a 3*3 2D array with all zero.
//   A B C
// 1 0 0 0
// 2 0 0 0
// 3 0 0 0

excel.set(1, "A", 2);
// set mat[1]["A"] = 2.
//   A B C
// 1 2 0 0
// 2 0 0 0
// 3 0 0 0

excel.sum(3, "C", ["A1", "A1:B2"]);
// set mat[3]["C"] = (mat[1]["A"]) + (mat[1]["A"] + mat[1]["B"] + mat[2]["A"] + mat[2]["B"]) = 2 + (2+0+0+0) = 4
//   A B C
// 1 2 0 0
// 2 0 0 0
// 3 0 0 4

excel.set(2, "B", 2);
// set mat[2]["B"] = 2.
//   A B C
// 1 2 0 0
// 2 0 2 0
// 3 0 0 4

excel.get(3, "C");
// return 4 + 2 = 6

INTERVIEW EXPLANATION: Why Dependency Graph for Excel Sum Formula?

1. **Problem Structure**: We need to support:
   - Setting cell values directly
   - Setting cell values as sum of other cells (with formulas)
   - Getting cell values (which may depend on other cells)
   - Formulas can reference ranges of cells

2. **Why Dependency Graph?**
   - **Formula Dependencies**: When a cell has a formula, it depends on other cells
   - **Recomputation**: When a dependency changes, we need to recompute dependent cells
   - **Topological Order**: Use dependency graph to determine recomputation order
   - **Efficient Updates**: Only recompute cells that are affected by changes

3. **Algorithm**:
   a. Maintain a 2D grid for cell values
   b. Maintain a dependency graph: cell -> set of cells that depend on it
   c. When setting a cell:
      - Clear old formula dependencies
      - Set new value
      - Recompute all dependent cells
   d. When setting a sum formula:
      - Parse formula to get referenced cells
      - Update dependencies
      - Compute sum value
      - Recompute dependents
   e. When getting a cell: return current value (may trigger recomputation)

4. **Key Insights**:
   - Parse formulas: "A1" (single cell) or "A1:B2" (range)
   - Build dependency graph: if C3 = sum(A1, B1), then C3 depends on A1 and B1
   - When A1 changes, recompute C3
   - Use DFS or topological sort to recompute in correct order

5. **Time Complexity**:
   - set: O(D) where D is number of dependent cells
   - sum: O(R + D) where R is number of referenced cells, D is dependents
   - get: O(1)

6. **Space Complexity**: O(H * W + E) where E is number of dependencies
"""

from collections import defaultdict, deque


class Excel:
    """Design Excel with Sum Formula"""
    
    def __init__(self, height: int, width: str):
        """
        Initialize Excel sheet.
        
        Args:
            height: Number of rows (1-indexed)
            width: Last column letter (e.g., 'C' means columns A, B, C)
        """
        self.height = height
        self.width = ord(width) - ord('A') + 1
        
        # Grid: row (1-indexed) -> col (0-indexed) -> value
        self.grid = [[0] * self.width for _ in range(height + 1)]
        
        # Formulas: (row, col) -> list of referenced cells
        self.formulas = {}
        
        # Dependencies: (row, col) -> set of cells that depend on it
        self.dependencies = defaultdict(set)
    
    def _get_col_index(self, col: str) -> int:
        """Convert column letter to index (A=0, B=1, ...)."""
        return ord(col) - ord('A')
    
    def _parse_cell(self, cell: str) -> tuple[int, int]:
        """Parse cell reference like 'A1' to (row, col)."""
        col = self._get_col_index(cell[0])
        row = int(cell[1:])
        return (row, col)
    
    def _parse_range(self, range_str: str) -> list[tuple[int, int]]:
        """
        Parse range like 'A1:B2' to list of cells.
        
        Args:
            range_str: Either "A1" (single cell) or "A1:B2" (range)
            
        Returns:
            List of (row, col) tuples
        """
        if ':' not in range_str:
            # Single cell
            return [self._parse_cell(range_str)]
        
        # Range: "A1:B2"
        start, end = range_str.split(':')
        start_row, start_col = self._parse_cell(start)
        end_row, end_col = self._parse_cell(end)
        
        cells = []
        for row in range(start_row, end_row + 1):
            for col in range(start_col, end_col + 1):
                cells.append((row, col))
        
        return cells
    
    def _recompute(self, row: int, col: int):
        """
        Recompute value of a cell and propagate to dependents.
        
        Args:
            row: Row index (1-indexed)
            col: Column index (0-indexed)
        """
        if (row, col) not in self.formulas:
            return  # No formula, value is set directly
        
        # Compute sum from formula
        total = 0
        for ref_cell in self.formulas[(row, col)]:
            ref_row, ref_col = ref_cell
            total += self.grid[ref_row][ref_col]
        
        self.grid[row][col] = total
        
        # Recompute all cells that depend on this cell
        for dep_row, dep_col in self.dependencies[(row, col)]:
            self._recompute(dep_row, dep_col)
    
    def set(self, row: int, column: str, val: int) -> None:
        """
        Set cell value directly.
        
        Args:
            row: Row index (1-indexed)
            column: Column letter (A, B, C, ...)
            val: Value to set
        """
        col = self._get_col_index(column)
        
        # Clear old formula if exists
        if (row, col) in self.formulas:
            # Remove dependencies
            for ref_cell in self.formulas[(row, col)]:
                self.dependencies[ref_cell].discard((row, col))
            del self.formulas[(row, col)]
        
        # Set new value
        self.grid[row][col] = val
        
        # Recompute dependents
        for dep_row, dep_col in list(self.dependencies[(row, col)]):
            self._recompute(dep_row, dep_col)
    
    def get(self, row: int, column: str) -> int:
        """
        Get cell value.
        
        Args:
            row: Row index (1-indexed)
            column: Column letter
            
        Returns:
            Cell value
        """
        col = self._get_col_index(column)
        return self.grid[row][col]
    
    def sum(self, row: int, column: str, numbers: list[str]) -> int:
        """
        Set cell to sum of referenced cells.
        
        Args:
            row: Row index (1-indexed)
            column: Column letter
            numbers: List of cell references (e.g., ["A1", "A1:B2"])
            
        Returns:
            Computed sum value
        """
        col = self._get_col_index(column)
        
        # Clear old formula dependencies
        if (row, col) in self.formulas:
            for ref_cell in self.formulas[(row, col)]:
                self.dependencies[ref_cell].discard((row, col))
        
        # Parse all referenced cells
        referenced_cells = []
        for num_str in numbers:
            referenced_cells.extend(self._parse_range(num_str))
        
        # Store formula
        self.formulas[(row, col)] = referenced_cells
        
        # Update dependencies
        for ref_cell in referenced_cells:
            self.dependencies[ref_cell].add((row, col))
        
        # Compute and set value
        total = sum(self.grid[r][c] for r, c in referenced_cells)
        self.grid[row][col] = total
        
        # Recompute dependents
        for dep_row, dep_col in list(self.dependencies[(row, col)]):
            self._recompute(dep_row, dep_col)
        
        return total


def test_excel():
    """Test cases for Excel Sum Formula"""
    # Test case 1: Example from problem
    excel = Excel(3, "C")
    
    excel.set(1, "A", 2)
    assert excel.get(1, "A") == 2, "Set value"
    
    result = excel.sum(3, "C", ["A1", "A1:B2"])
    assert result == 4, f"Expected 4, got {result}"
    assert excel.get(3, "C") == 4, "Get sum"
    
    excel.set(2, "B", 2)
    assert excel.get(3, "C") == 6, f"Expected 6 after update, got {excel.get(3, 'C')}"
    
    print("✓ Test 1: Example from problem description")
    
    # Test case 2: Simple sum
    excel2 = Excel(2, "B")
    excel2.set(1, "A", 5)
    excel2.set(1, "B", 3)
    result2 = excel2.sum(2, "A", ["A1", "B1"])
    assert result2 == 8, f"Expected 8, got {result2}"
    print("✓ Test 2: Simple sum")
    
    # Test case 3: Range sum
    excel3 = Excel(3, "C")
    excel3.set(1, "A", 1)
    excel3.set(1, "B", 2)
    excel3.set(2, "A", 3)
    excel3.set(2, "B", 4)
    result3 = excel3.sum(3, "C", ["A1:B2"])
    assert result3 == 10, f"Expected 10, got {result3}"
    print("✓ Test 3: Range sum")
    
    print("\nAll tests passed!")


if __name__ == "__main__":
    test_excel()
    
    # Example usage
    print("\nExample usage:")
    excel = Excel(3, "C")
    
    excel.set(1, "A", 2)
    print(f"Set A1 = 2")
    
    result = excel.sum(3, "C", ["A1", "A1:B2"])
    print(f"Set C3 = sum(A1, A1:B2) = {result}")
    
    excel.set(2, "B", 2)
    print(f"Set B2 = 2")
    print(f"Get C3 = {excel.get(3, 'C')}")
# %%

