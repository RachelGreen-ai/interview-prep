# LeetCode 1041: Robot Bounded In Circle
#%%
"""
Problem Statement:
------------------
On an infinite plane, a robot initially stands at (0, 0) and faces north. The robot 
can receive one of three instructions:
- 'G': go straight 1 unit
- 'L': turn 90 degrees to the left (counterclockwise)
- 'R': turn 90 degrees to the right (clockwise)

The robot performs the instructions given in order, and repeats them forever.

Return true if and only if there exists a circle in the plane such that the robot 
never leaves the circle.

Example 1:
Input: instructions = "GGLLGG"
Output: true
Explanation: The robot moves from (0,0) to (0,2), turns 180 degrees, and then 
returns to (0,0). When repeating these instructions, the robot remains in the 
circle of radius 2 centered at the origin.

Example 2:
Input: instructions = "GG"
Output: false
Explanation: The robot moves north indefinitely.

Example 3:
Input: instructions = "GL"
Output: true
Explanation: The robot moves from (0, 0) -> (0, 1) -> (-1, 1) -> (-1, 0) -> (0, 0) -> ...

KEY INSIGHT:
-----------
The robot is bounded in a circle if and only if:
1. After one cycle, it returns to origin (0, 0), OR
2. After one cycle, it's facing a different direction than it started (not North)

Why?
- If robot returns to origin: it will repeat the same path forever (bounded)
- If robot changes direction: after 1-4 cycles, it will form a closed loop
- If robot ends at non-origin facing North: it will move away indefinitely (unbounded)

APPROACH:
---------
1. Simulate one cycle of instructions
2. Track position (x, y) and direction
3. Use direction vectors: North=(0,1), East=(1,0), South=(0,-1), West=(-1,0)
4. Check if (x==0 and y==0) OR direction != North

TIME COMPLEXITY: O(n) where n is length of instructions
SPACE COMPLEXITY: O(1) - only using constant extra space

INTERVIEW TIPS:
--------------
1. Key insight: Only need to simulate ONE cycle, not infinite repetitions
2. Direction tracking: Use modulo arithmetic for turning (L: -1, R: +1)
3. Edge cases: Empty string (returns to origin), single instruction
4. Common mistake: Trying to simulate multiple cycles (unnecessary!)
"""

from typing import List

class Solution:
    def isRobotBounded(self, instructions: str) -> bool:
        """
        Determine if robot stays in a bounded circle.
        
        Strategy:
        - Simulate one cycle of instructions
        - If robot returns to origin OR faces different direction → bounded
        - Otherwise → unbounded
        """
        # Initial position
        x, y = 0, 0
        
        # Direction vectors: North, East, South, West
        # Each direction is (dx, dy) representing movement
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        # Current direction index (0 = North, 1 = East, 2 = South, 3 = West)
        direction_idx = 0
        
        # Process each instruction
        for instruction in instructions:
            if instruction == 'G':
                # Move forward in current direction
                dx, dy = directions[direction_idx]
                x += dx
                y += dy
            elif instruction == 'L':
                # Turn left (counterclockwise): North -> West -> South -> East -> North
                direction_idx = (direction_idx - 1) % 4
            elif instruction == 'R':
                # Turn right (clockwise): North -> East -> South -> West -> North
                direction_idx = (direction_idx + 1) % 4
        
        # Robot is bounded if:
        # 1. Returns to origin (will repeat same path)
        # 2. Direction changed (will form closed loop after 1-4 cycles)
        return (x == 0 and y == 0) or direction_idx != 0

#%% TEST CASES WITH EXPLANATIONS

def test_basic_cases():
    """Test basic cases: bounded and unbounded scenarios"""
    print("=" * 70)
    print("TEST 1: Basic Cases")
    print("=" * 70)
    sol = Solution()
    
    # Test 1: Returns to origin
    instructions = "GGLLGG"
    result = sol.isRobotBounded(instructions)
    print(f"\n1. instructions = '{instructions}'")
    print(f"   Expected: True")
    print(f"   Got: {result}")
    print(f"   Explanation: Robot goes (0,0) -> (0,2) -> turns 180° -> returns to (0,0)")
    print(f"   After one cycle: at origin, will repeat same path → BOUNDED")
    
    # Test 2: Moves north indefinitely
    instructions = "GG"
    result = sol.isRobotBounded(instructions)
    print(f"\n2. instructions = '{instructions}'")
    print(f"   Expected: False")
    print(f"   Got: {result}")
    print(f"   Explanation: Robot moves (0,0) -> (0,2), still facing North")
    print(f"   After one cycle: at (0,2) facing North → will move away → UNBOUNDED")
    
    # Test 3: Forms a square/loop
    instructions = "GL"
    result = sol.isRobotBounded(instructions)
    print(f"\n3. instructions = '{instructions}'")
    print(f"   Expected: True")
    print(f"   Got: {result}")
    print(f"   Explanation: Robot goes (0,0) -> (0,1) -> turns left -> faces West")
    print(f"   After one cycle: direction changed (North -> West) → will form loop → BOUNDED")

def test_edge_cases():
    """Test edge cases: empty string, single instructions, complex patterns"""
    print("\n" + "=" * 70)
    print("TEST 2: Edge Cases")
    print("=" * 70)
    sol = Solution()
    
    # Test 1: Empty string
    instructions = ""
    result = sol.isRobotBounded(instructions)
    print(f"\n1. instructions = '{instructions}' (empty)")
    print(f"   Expected: True")
    print(f"   Got: {result}")
    print(f"   Explanation: No movement, stays at origin → BOUNDED")
    
    # Test 2: Single G
    instructions = "G"
    result = sol.isRobotBounded(instructions)
    print(f"\n2. instructions = '{instructions}'")
    print(f"   Expected: False")
    print(f"   Got: {result}")
    print(f"   Explanation: Moves to (0,1), still facing North → UNBOUNDED")
    
    # Test 3: Only turns (no movement)
    instructions = "LR"
    result = sol.isRobotBounded(instructions)
    print(f"\n3. instructions = '{instructions}'")
    print(f"   Expected: True")
    print(f"   Got: {result}")
    print(f"   Explanation: Turns left then right, back to North, at origin → BOUNDED")
    
    # Test 4: Complex pattern that returns to origin
    instructions = "GLGLGGLGL"
    result = sol.isRobotBounded(instructions)
    print(f"\n4. instructions = '{instructions}'")
    print(f"   Expected: False")
    print(f"   Got: {result}")
    print(f"   Explanation: Need to trace the path...")

def test_direction_change():
    """Test cases where direction change makes it bounded"""
    print("\n" + "=" * 70)
    print("TEST 3: Direction Change Cases")
    print("=" * 70)
    sol = Solution()
    
    test_cases = [
        ("L", True, "Turn left once, faces West, at origin → BOUNDED"),
        ("R", True, "Turn right once, faces East, at origin → BOUNDED"),
        ("LL", True, "Turn left twice, faces South, at origin → BOUNDED"),
        ("RR", True, "Turn right twice, faces South, at origin → BOUNDED"),
        ("GR", True, "Move North, turn right, at (0,1) facing East → BOUNDED (direction changed)"),
        ("GL", True, "Move North, turn left, at (0,1) facing West → BOUNDED (direction changed)"),
    ]
    
    for instructions, expected, explanation in test_cases:
        result = sol.isRobotBounded(instructions)
        status = "✓" if result == expected else "✗"
        print(f"{status} instructions = '{instructions}': {result} (expected {expected})")
        print(f"   {explanation}")

def visualize_path(instructions: str, cycles: int = 1):
    """Helper function to visualize robot path"""
    x, y = 0, 0
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    direction_names = ["North", "East", "South", "West"]
    direction_idx = 0
    
    path = [(0, 0)]
    step_count = 0
    print(f"\nPath visualization for '{instructions}' ({cycles} cycle(s)):")
    print(f"Start: (0, 0) facing {direction_names[direction_idx]}")
    
    for cycle in range(cycles):
        for i, instruction in enumerate(instructions):
            step_count += 1
            if instruction == 'G':
                dx, dy = directions[direction_idx]
                x += dx
                y += dy
                path.append((x, y))
                print(f"  Step {step_count}: {instruction} → ({x}, {y}) facing {direction_names[direction_idx]}")
            elif instruction == 'L':
                direction_idx = (direction_idx - 1) % 4
                print(f"  Step {step_count}: {instruction} → turn to {direction_names[direction_idx]}")
            elif instruction == 'R':
                direction_idx = (direction_idx + 1) % 4
                print(f"  Step {step_count}: {instruction} → turn to {direction_names[direction_idx]}")
    
    print(f"End: ({x}, {y}) facing {direction_names[direction_idx]}")
    return (x, y), direction_idx

# Run all tests
if __name__ == "__main__":
    test_basic_cases()
    test_edge_cases()
    test_direction_change()
    
    # Visualize some paths
    print("\n" + "=" * 70)
    print("PATH VISUALIZATION")
    print("=" * 70)
    visualize_path("GGLLGG", 1)
    visualize_path("GL", 2)

# %%

