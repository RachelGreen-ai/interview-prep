# 🎯 One-Day Deep Dive (Interview Tomorrow)

You’re interviewing tomorrow, so this doc is now a **one-day algorithm review** (not a multi-week plan).

Goals for today:
- Refresh the **highest-leverage patterns** (sliding window, BFS shortest path, DP, graphs/topo, backtracking)
- Build a **mental index**: “If I see X, I use Y template”
- Do 1–2 timed reps to warm up (not 20 new problems)

---

## ✅ Quick “If you see this → do this” templates

- **Minimum window / substring with constraints** → Sliding window with counts  
  (`minimum_window_substring.py`, `longest_substring_without_repeating_characters.py`, `subarray_product_less_than_k.py`)

- **Unweighted shortest path in grid / state space** → BFS (queue), visited, layers  
  (`shortest_path_binary_matrix.py`, `shortest_path_get_all_keys.py`, `sliding_puzzle.py`)

- **Shortest path with constraints (K stops / extra state)** → Dijkstra-with-state OR Bellman-Ford DP  
  (`cheapest_flights_k_stops.py`)

- **“Min cost / max profit / ways”** → DP (pick state carefully, then iterate)  
  (`coin_change.py`, `edit_distance.py`, `house_robber*.py`, `maximum_profit_job_scheduling.py`, `maxsquare.py`)

- **“Order with dependencies / alien language”** → Topological sort (+ cycle detection)  
  (`aliendictionary.py`)

- **Search all combinations / board backtracking** → DFS + pruning  
  (`combination_sum.py`, `word_search.py`, `word_search_ii.py`, `shopping_offers.py`, `pyramid_transition_matrix.py`)

---

## 🧠 Algorithm clusters (scan of your whole `leetcode/` folder)

### 1) BFS / Shortest Path (you were right — this deserves its own cluster)
- **Classic BFS shortest path (unweighted)**:
  - `shortest_path_binary_matrix.py`
  - `sliding_puzzle.py`
  - `shortest_path_get_all_keys.py` (BFS with bitmask state)
- **Shortest path with constraints / extra dimension**:
  - `cheapest_flights_k_stops.py` (K-stops)
- **Related graph/grid expansions**:
  - `number_of_islands_ii.py` (dynamic connectivity flavor)
  - `making_a_large_island.py` (grid / components; not shortest path but same grid-reasoning muscle)

What to review here (fast):
- BFS layer-by-layer invariant
- How to encode **state** (pos, keys bitmask, stops used)
- When BFS fails → add state or switch to Dijkstra / DP

### 2) Graphs / Topological / Tree-ish
- `aliendictionary.py` (toposort)
- `minimum_vertices_reach_all.py`, `minimum_vertices_traverse_graph.py` (graph reachability / covering)
- `smallest_common_region.py` (LCA-on-parent pointers)
- `lowest_common_ancestor.py` (tree LCA patterns)
- `travel_buddy.py` (graph-ish / real-world modeling)

### 3) Dynamic Programming (core interview muscle)
- **Classic 1D DP**:
  - `coin_change.py`
  - `house_robber.py`, `house_robber_ii.py`, `house_robber_iii.py`
  - `maximum_subarray.py`
- **2D DP / strings / grids**:
  - `edit_distance.py`
  - `maxsquare.py`
  - `k_edit_distance.py`
- **DP + sorting / binary search**:
  - `maximum_profit_job_scheduling.py`

### 4) Sliding Window / Two Pointers (high ROI)
- `minimum_window_substring.py`
- `longest_substring_without_repeating_characters.py`
- `subarray_product_less_than_k.py`

### 5) Backtracking / DFS + pruning
- `combination_sum.py`
- `word_search.py`, `word_search_ii.py`
- `shopping_offers.py`
- `pyramid_transition_matrix.py`
- `palindrome_pairs.py` (often hash/trie-ish; still heavy pruning/lookup thinking)

### 6) Intervals / Heaps / Scheduling
- `meetingroom2.py`
- `employee_free_time.py`
- `maximum_profit_job_scheduling.py` (also DP)

### 7) Data Structures / Design
- **Iterators**:
  - `vector2d.py` (LC 251)
  - `nested_list_iterator.py` (LC 341)
- **Key-value / DS design**:
  - `time_based_key_value_store.py`
  - `all_oone_data_structure.py`
  - `design_circular_queue.py`
  - `design_tic_tac_toe.py`
  - `simplebanksystem.py`
- **File system**:
  - `design_file_system.py` (LC 1166)
  - `tree_file_system.py` (your leaf-only variant)

### 8) Parsing / Math / Bits / Misc
- Parsing: `basic_calculator_ii.py`, `mini_parser.py`, `csv_parser.py`
- Math/number: `happy_number.py`, `nth_digit.py`, `collatz_conjecture.py`, `fraction_to_recurring_decimal.py`
- Bits: `reverse_bits.py`
- Greedy/rounding: `minimize_rounding_error_to_meet_target.py`

---

## 📅 One-day review schedule (practical, interview-eve)

### Block A (60–90 min): “Must-hit” patterns
- Sliding window: `minimum_window_substring.py` (say the invariant out loud)
- BFS shortest path: `shortest_path_binary_matrix.py` + skim `shortest_path_get_all_keys.py` state encoding
- DP: `coin_change.py` (state + transition + base cases)

### Block B (60–90 min): Graphs + constraints
- Toposort: `aliendictionary.py` (Kahn vs DFS, cycle detection)
- Constrained shortest path: `cheapest_flights_k_stops.py` (what state is, why plain BFS fails)

### Block C (60–90 min): Backtracking + pruning
- `word_search_ii.py` (Trie + DFS pruning) OR `shopping_offers.py` (state memo/backtracking)
- `combination_sum.py` (template warm-up)

### Block D (30–60 min): Systems/design warm-up (optional but common)
- `design_file_system.py` (LC 1166)
- `time_based_key_value_store.py` (API + DS)

### Block E (30–45 min): Timed rep + cool-down
- Pick ONE: `minimum_window_substring.py` or `shortest_path_binary_matrix.py`
- Do a clean re-implementation timed, then stop. Sleep matters more than extra problems.

---

## 🔍 “Common misses” checklist (use before you end the day)
- **Shortest path**: did I justify BFS vs Dijkstra vs DP-with-steps?
- **Sliding window**: do I track “missing” or “formed” correctly?
- **DP**: did I define state + transition clearly before coding?
- **Graphs**: cycle detection and visited semantics (node vs state)?

