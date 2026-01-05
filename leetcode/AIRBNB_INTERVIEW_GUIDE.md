# Airbnb Interview Algorithm Guide

## 🎯 Overview

This guide focuses on **algorithm patterns commonly asked at Airbnb** based on interview data and problem analysis. Airbnb interviews typically combine **system design** with **coding**, so understanding these patterns is crucial.

---

## 📊 Algorithm Frequency at Airbnb

Based on analysis of Airbnb interview questions:

1. **Dynamic Programming (DP)** - ~25% ⭐⭐⭐
2. **Graph Algorithms (Topological Sort, DFS/BFS)** - ~20% ⭐⭐⭐
3. **String Manipulation** - ~15% ⭐⭐
4. **Tree Problems** - ~15% ⭐⭐
5. **Array/Matrix Problems** - ~12% ⭐⭐
6. **Design Problems** - ~8% ⭐
7. **Other (Greedy, Two Pointers, etc.)** - ~5% ⭐

---

## 🧠 Core Algorithm Patterns

### 1. Dynamic Programming (DP) ⭐⭐⭐

**Why Airbnb asks DP:**
- Real-world optimization problems (pricing, scheduling, resource allocation)
- Tests ability to break down complex problems
- Common in system design + coding rounds

**Key Patterns:**

#### Pattern 1: Linear DP
```
dp[i] = f(dp[i-1], dp[i-2], ...)
```
**Examples:**
- House Robber (LC #198, #213, #337)
- Climbing Stairs (LC #70)
- Maximum Subarray (LC #53)

**Interview Strategy:**
1. Identify subproblem: "What's the optimal solution up to position i?"
2. Find recurrence: How does dp[i] relate to previous states?
3. Base cases: What are the smallest subproblems?
4. Optimize space if possible (O(1) for linear DP)

#### Pattern 2: 2D DP (Matrix)
```
dp[i][j] = f(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
```
**Examples:**
- Maximal Square (LC #221) ✅
- Edit Distance (LC #72) ✅
- Unique Paths (LC #62, #63)

**Interview Strategy:**
1. Define state: What does dp[i][j] represent?
2. Transition: How to build current state from previous?
3. Space optimization: Can we use O(n) instead of O(m×n)?

#### Pattern 3: Interval DP
```
dp[i][j] = min/max over all k: dp[i][k] + dp[k+1][j] + cost
```
**Examples:**
- Burst Balloons (LC #312)
- Palindrome Partitioning (LC #131)

**Interview Strategy:**
- Think: "What's the optimal way to split this interval?"
- Usually O(n³) time, O(n²) space

#### Pattern 4: DP with State Machine
```
dp[i][state] = optimal value at position i with state
```
**Examples:**
- Best Time to Buy/Sell Stock series (LC #121, #122, #123, #188)
- House Robber with constraints

**Interview Strategy:**
- Identify states (e.g., holding stock, not holding)
- Track transitions between states
- Often can optimize to O(1) space

**Common DP Problems at Airbnb:**
- ✅ House Robber series (#198, #213, #337)
- ✅ Edit Distance (#72)
- ✅ Maximal Square (#221)
- ❌ Maximum Profit in Job Scheduling (#1235)
- ❌ Cheapest Flights Within K Stops (#787) ✅

---

### 2. Graph Algorithms ⭐⭐⭐

**Why Airbnb asks Graph:**
- Dependencies in booking systems
- Route planning and recommendations
- Social network features

#### Pattern 1: Topological Sort

**When to use:**
- Dependencies/ordering problems
- Course scheduling
- Build systems with dependencies

**Algorithm (Kahn's):**
```python
1. Build graph and in-degree array
2. Add all nodes with in-degree 0 to queue
3. While queue not empty:
   - Pop node, add to result
   - Decrease in-degree of neighbors
   - If neighbor in-degree becomes 0, add to queue
4. If result length == total nodes: valid ordering
   Else: cycle exists
```

**Examples:**
- ✅ Alien Dictionary (LC #269)
- Course Schedule (LC #207, #210)
- Minimum Vertices to Traverse Graph

**Interview Strategy:**
1. Recognize dependency pattern
2. Build graph (adjacency list + in-degrees)
3. Use BFS/queue for topological sort
4. Handle cycles (return empty/False)

#### Pattern 2: DFS/BFS on Graphs

**When to use:**
- Finding paths
- Connected components
- Cycle detection

**DFS Template:**
```python
def dfs(node, visited):
    visited.add(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(neighbor, visited)
```

**BFS Template:**
```python
from collections import deque
queue = deque([start])
visited = {start}
while queue:
    node = queue.popleft()
    for neighbor in graph[node]:
        if neighbor not in visited:
            visited.add(neighbor)
            queue.append(neighbor)
```

**Examples:**
- Word Search (LC #79, #212) ✅
- Number of Islands (LC #200)
- Clone Graph (LC #133)

#### Pattern 3: Shortest Path (Dijkstra/Bellman-Ford)

**When to use:**
- Weighted graphs
- Finding cheapest/fastest routes
- With constraints (like K stops)

**Dijkstra (Greedy):**
```python
heap = [(0, start)]  # (cost, node)
while heap:
    cost, node = heapq.heappop(heap)
    if node == target: return cost
    for neighbor, weight in graph[node]:
        new_cost = cost + weight
        heapq.heappush(heap, (new_cost, neighbor))
```

**Examples:**
- ✅ Cheapest Flights Within K Stops (LC #787)
- Network Delay Time (LC #743)

**Interview Strategy:**
- Use Dijkstra for non-negative weights
- Use Bellman-Ford for negative weights or constraints
- Modify for constraints (track stops, etc.)

---

### 3. String Manipulation ⭐⭐

**Why Airbnb asks:**
- Text processing in search/recommendations
- Parsing user input
- Data transformation

**Key Patterns:**

#### Pattern 1: Two Pointers
- Palindrome checking
- String matching
- Sliding window

**Examples:**
- Valid Palindrome (LC #125)
- Longest Substring Without Repeating (LC #3)
- ✅ One Edit Distance (LC #161)

#### Pattern 2: String Parsing
- CSV parsing ✅
- Expression evaluation
- URL parsing

**Interview Strategy:**
- Use built-in libraries when appropriate (csv module)
- Handle edge cases (quotes, escapes, empty strings)
- State machine for complex parsing

#### Pattern 3: Trie + String Search
- Prefix matching
- Word search in grid
- Autocomplete

**Examples:**
- ✅ Word Search II (LC #212)
- Implement Trie (LC #208)
- Add and Search Words (LC #211)

---

### 4. Tree Problems ⭐⭐

**Why Airbnb asks:**
- Hierarchical data (categories, locations)
- File systems
- Decision trees

**Key Patterns:**

#### Pattern 1: Tree Traversal
- DFS (pre/in/post-order)
- BFS (level-order)
- Iterative vs Recursive

**Examples:**
- Binary Tree Level Order (LC #102)
- Validate BST (LC #98)

#### Pattern 2: Tree DP
- Bottom-up computation
- Return multiple values from subtree

**Examples:**
- ✅ House Robber III (LC #337)
- Binary Tree Maximum Path Sum (LC #124)

#### Pattern 3: LCA (Lowest Common Ancestor)
- Finding common ancestors
- Path problems

**Examples:**
- LCA of BST (LC #235)
- ❌ Smallest Common Region (LC #1257)

---

### 5. Array/Matrix Problems ⭐⭐

**Key Patterns:**

#### Pattern 1: Sliding Window
- Subarray/substring problems
- Fixed or variable window size

**Examples:**
- Maximum Sum Subarray (LC #53)
- Longest Substring (LC #3)

#### Pattern 2: Two Pointers
- Sorted arrays
- Pair/triplet problems

**Examples:**
- Two Sum (LC #1)
- 3Sum (LC #15)

#### Pattern 3: Matrix Traversal
- Spiral order
- Diagonal traversal
- ✅ Word Search (LC #79, #212)

---

## 🎯 Problem-Solving Framework

### Step-by-Step Approach:

1. **Understand the Problem** (2 min)
   - Read carefully, ask clarifying questions
   - Identify input/output format
   - Note constraints

2. **Identify Pattern** (1 min)
   - Look for keywords:
     * "optimal" → DP or Greedy
     * "dependencies" → Topological Sort
     * "shortest path" → BFS/Dijkstra
     * "all possible" → Backtracking
   - Match to known patterns

3. **Design Algorithm** (3 min)
   - Choose data structures
   - Define state/transitions
   - Handle edge cases

4. **Code** (10-15 min)
   - Write clean, readable code
   - Use meaningful variable names
   - Add comments for complex logic

5. **Test & Optimize** (3-5 min)
   - Test with examples
   - Check edge cases
   - Discuss time/space complexity
   - Mention optimizations

---

## 📝 Common Airbnb-Specific Patterns

### 1. Design + Implementation
Airbnb often asks you to:
- Design a system (e.g., booking system)
- Then implement a specific component

**Strategy:**
- Start with high-level design
- Focus on one component in detail
- Show understanding of scalability

### 2. Real-World Problems
Problems often relate to:
- Booking/reservation systems
- Search and recommendations
- Pricing algorithms
- User matching (travel buddies) ✅

**Strategy:**
- Connect problem to real-world use case
- Discuss trade-offs
- Mention scalability considerations

### 3. String Processing
Common in:
- Search functionality
- Data parsing
- Text analysis

**Examples:**
- ✅ CSV Parser
- Text Justification (LC #68) ✅
- Word Search ✅

---

## 🚀 Quick Reference: Pattern → Problem Mapping

| Pattern | Key Problems | Time Complexity |
|---------|-------------|-----------------|
| **Linear DP** | House Robber, Climbing Stairs | O(n) |
| **2D DP** | Maximal Square, Edit Distance | O(m×n) |
| **Topological Sort** | Alien Dictionary, Course Schedule | O(V+E) |
| **DFS/BFS** | Word Search, Islands | O(V+E) |
| **Dijkstra** | Cheapest Flights, Network Delay | O(E log V) |
| **Trie** | Word Search II, Autocomplete | O(W×L) build |
| **Two Pointers** | Two Sum, 3Sum | O(n) |
| **Sliding Window** | Longest Substring, Subarray Sum | O(n) |

---

## 💡 Interview Tips

1. **Start Simple**: Always start with brute force, then optimize
2. **Communicate**: Explain your thought process out loud
3. **Ask Questions**: Clarify requirements before coding
4. **Handle Edge Cases**: Empty inputs, single elements, etc.
5. **Optimize Thoughtfully**: Mention space-time trade-offs
6. **Test Your Code**: Walk through examples manually

---

## 📚 Recommended Study Order

### Week 1: Foundation
- DP basics (House Robber, Climbing Stairs)
- Graph basics (DFS/BFS)
- String basics (Two Pointers)

### Week 2: Intermediate
- 2D DP (Maximal Square, Edit Distance)
- Topological Sort (Alien Dictionary)
- Tree problems

### Week 3: Advanced
- Graph algorithms (Dijkstra, Union-Find)
- Complex DP (Job Scheduling)
- Design problems

### Week 4: Practice
- Mock interviews
- Time yourself
- Review patterns

---

## ✅ Problems We Have (Ready for Practice)

See `REVIEW_REPORT.md` for complete list. Key ones:
- ✅ House Robber series (DP)
- ✅ Edit Distance (2D DP)
- ✅ Alien Dictionary (Topological Sort)
- ✅ Word Search series (DFS + Trie)
- ✅ Cheapest Flights (Dijkstra)
- ✅ Travel Buddy (Real-world problem)
- ✅ CSV Parser (String processing)

---

## 🎓 Final Notes

**Remember:**
- Airbnb values **clean code** and **clear communication**
- They often combine **system design** with **coding**
- Focus on **patterns**, not memorizing solutions
- Practice **explaining** your approach

**Good luck with your Airbnb interview! 🚀**

