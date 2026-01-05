# LeetCode 348: Design Tic-Tac-Toe
#%%
"""
Problem Statement:
Assume the following rules are for the tic-tac-toe game on an n x n board between two players:

1. A move is guaranteed to be valid and is placed on an empty block.
2. Once a winning condition is reached, no more moves are allowed.
3. A player who succeeds in placing n of their marks in a horizontal, vertical,
   or diagonal row wins the game.

Implement the TicTacToe class:
- TicTacToe(int n) Initializes the object the size of the board n.
- int move(int row, int col, int player) Indicates that player with id player plays
  at the cell (row, col) of the board. The move is guaranteed to be a valid move.

Return:
- 0 if no one wins
- 1 if player 1 wins
- 2 if player 2 wins

Example:
Input:
["TicTacToe", "move", "move", "move", "move", "move", "move", "move"]
[[3], [0, 0, 1], [0, 2, 2], [2, 2, 1], [1, 1, 2], [2, 0, 1], [1, 0, 2], [2, 1, 1]]
Output: [null, 0, 0, 0, 0, 0, 0, 1]

Explanation:
TicTacToe ticTacToe = new TicTacToe(3);
Assume that player 1 is "X" and player 2 is "O".
ticTacToe.move(0, 0, 1); // return 0 (no one wins)
|X| | |
| | | |    // Player 1 makes a move at (0, 0).
| | | |

ticTacToe.move(0, 2, 2); // return 0 (no one wins)
|X| |O|
| | | |    // Player 2 makes a move at (0, 2).
| | | |

ticTacToe.move(2, 2, 1); // return 0 (no one wins)
|X| |O|
| | | |    // Player 1 makes a move at (2, 2).
| | |X|

ticTacToe.move(1, 1, 2); // return 0 (no one wins)
|X| |O|
| |O| |    // Player 2 makes a move at (1, 1).
| | |X|

ticTacToe.move(2, 0, 1); // return 0 (no one wins)
|X| |O|
| |O| |    // Player 1 makes a move at (2, 0).
|X| |X|

ticTacToe.move(1, 0, 2); // return 0 (no one wins)
|X| |O|
|O|O| |    // Player 2 makes a move at (1, 0).
|X| |X|

ticTacToe.move(2, 1, 1); // return 1 (player 1 wins)
|X| |O|
|O|O| |    // Player 1 makes a move at (2, 1).
|X|X|X|

INTERVIEW EXPLANATION: Why Efficient Tracking for Tic-Tac-Toe?

1. **Problem Structure**: We need to check if a move results in a win. A win occurs when
   a player has n marks in a row (horizontal, vertical, or diagonal).

2. **Why Efficient Tracking?**
   - **Naive Approach**: After each move, check all rows, columns, and diagonals - O(n²)
   - **Optimized Approach**: Track counts for each row, column, and diagonal - O(1) per move
   - **Key Insight**: We only need to check if the current move completes a line

3. **Algorithm**:
   - Maintain arrays for row counts, column counts, and diagonal counts
   - For each move at (row, col) by player:
     a. Increment row[row] count for player
     b. Increment col[col] count for player
     c. If row == col, increment main diagonal count
     d. If row + col == n-1, increment anti-diagonal count
     e. Check if any count equals n (win condition)

4. **Key Insights**:
   - Player 1 adds +1, Player 2 adds -1 (or use separate arrays)
   - Win occurs when absolute value of any count equals n
   - Only need to check the row/column/diagonals affected by current move

5. **Time Complexity**: O(1) per move
   - Constant time to update counts and check win condition

6. **Space Complexity**: O(n) for tracking arrays
"""


class TicTacToe:
    """Design Tic-Tac-Toe Game"""
    
    def __init__(self, n: int):
        """
        Initialize the tic-tac-toe board.
        
        Args:
            n: Size of the board (n x n)
        """
        self.n = n
        # Track counts for each row (player 1: +1, player 2: -1)
        self.rows = [0] * n
        # Track counts for each column
        self.cols = [0] * n
        # Track main diagonal (top-left to bottom-right)
        self.diag = 0
        # Track anti-diagonal (top-right to bottom-left)
        self.anti_diag = 0
    
    def move(self, row: int, col: int, player: int) -> int:
        """
        Make a move and check if a player wins.
        
        Args:
            row: Row index (0-indexed)
            col: Column index (0-indexed)
            player: Player ID (1 or 2)
            
        Returns:
            0 if no one wins, player ID if that player wins
        """
        # Value to add: +1 for player 1, -1 for player 2
        value = 1 if player == 1 else -1
        
        # Update row count
        self.rows[row] += value
        # Update column count
        self.cols[col] += value
        
        # Update main diagonal (if on main diagonal)
        if row == col:
            self.diag += value
        
        # Update anti-diagonal (if on anti-diagonal)
        if row + col == self.n - 1:
            self.anti_diag += value
        
        # Check win condition: any count equals n (in absolute value)
        if (abs(self.rows[row]) == self.n or
            abs(self.cols[col]) == self.n or
            abs(self.diag) == self.n or
            abs(self.anti_diag) == self.n):
            return player
        
        return 0


class TicTacToeSeparateArrays:
    """Alternative implementation using separate arrays for each player"""
    
    def __init__(self, n: int):
        self.n = n
        # Separate tracking for each player
        self.rows_p1 = [0] * n
        self.cols_p1 = [0] * n
        self.rows_p2 = [0] * n
        self.cols_p2 = [0] * n
        self.diag_p1 = 0
        self.diag_p2 = 0
        self.anti_diag_p1 = 0
        self.anti_diag_p2 = 0
    
    def move(self, row: int, col: int, player: int) -> int:
        """Make a move using separate arrays."""
        if player == 1:
            self.rows_p1[row] += 1
            self.cols_p1[col] += 1
            if row == col:
                self.diag_p1 += 1
            if row + col == self.n - 1:
                self.anti_diag_p1 += 1
            
            if (self.rows_p1[row] == self.n or
                self.cols_p1[col] == self.n or
                self.diag_p1 == self.n or
                self.anti_diag_p1 == self.n):
                return 1
        else:
            self.rows_p2[row] += 1
            self.cols_p2[col] += 1
            if row == col:
                self.diag_p2 += 1
            if row + col == self.n - 1:
                self.anti_diag_p2 += 1
            
            if (self.rows_p2[row] == self.n or
                self.cols_p2[col] == self.n or
                self.diag_p2 == self.n or
                self.anti_diag_p2 == self.n):
                return 2
        
        return 0


def test_tic_tac_toe():
    """Test cases for Tic-Tac-Toe"""
    # Test case 1: Example from problem
    game = TicTacToe(3)
    
    assert game.move(0, 0, 1) == 0, "Move 1"
    assert game.move(0, 2, 2) == 0, "Move 2"
    assert game.move(2, 2, 1) == 0, "Move 3"
    assert game.move(1, 1, 2) == 0, "Move 4"
    assert game.move(2, 0, 1) == 0, "Move 5"
    assert game.move(1, 0, 2) == 0, "Move 6"
    assert game.move(2, 1, 1) == 1, "Move 7 - Player 1 wins"
    
    print("✓ Test 1: Example from problem description")
    
    # Test case 2: Horizontal win
    game2 = TicTacToe(3)
    assert game2.move(0, 0, 1) == 0
    assert game2.move(1, 0, 2) == 0
    assert game2.move(0, 1, 1) == 0
    assert game2.move(1, 1, 2) == 0
    assert game2.move(0, 2, 1) == 1  # Player 1 wins horizontally
    
    print("✓ Test 2: Horizontal win")
    
    # Test case 3: Vertical win
    game3 = TicTacToe(3)
    assert game3.move(0, 0, 1) == 0
    assert game3.move(0, 1, 2) == 0
    assert game3.move(1, 0, 1) == 0
    assert game3.move(0, 2, 2) == 0
    assert game3.move(2, 0, 1) == 1  # Player 1 wins vertically
    
    print("✓ Test 3: Vertical win")
    
    # Test case 4: Diagonal win
    game4 = TicTacToe(3)
    assert game4.move(0, 0, 1) == 0
    assert game4.move(0, 1, 2) == 0
    assert game4.move(1, 1, 1) == 0
    assert game4.move(0, 2, 2) == 0
    assert game4.move(2, 2, 1) == 1  # Player 1 wins on main diagonal
    
    print("✓ Test 4: Diagonal win")
    
    # Test case 5: Anti-diagonal win
    game5 = TicTacToe(3)
    assert game5.move(0, 2, 1) == 0
    assert game5.move(0, 0, 2) == 0
    assert game5.move(1, 1, 1) == 0
    assert game5.move(0, 1, 2) == 0
    assert game5.move(2, 0, 1) == 1  # Player 1 wins on anti-diagonal
    
    print("✓ Test 5: Anti-diagonal win")
    
    print("\nAll tests passed!")


if __name__ == "__main__":
    test_tic_tac_toe()
    
    # Example usage
    print("\nExample usage:")
    game = TicTacToe(3)
    
    moves = [
        (0, 0, 1), (0, 2, 2), (2, 2, 1), (1, 1, 2),
        (2, 0, 1), (1, 0, 2), (2, 1, 1)
    ]
    
    for i, (row, col, player) in enumerate(moves, 1):
        result = game.move(row, col, player)
        print(f"Move {i}: Player {player} at ({row}, {col}) -> Result: {result}")
        if result != 0:
            print(f"  Player {result} wins!")
            break
# %%

