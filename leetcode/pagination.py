# Pagination Problem
#%%
"""
Problem Statement:
Given a list of CSV strings (each entry has: host_id, listing_id, score, city).
Results are already sorted by score descending.

Rules:
- Show k results per page (k=12 in example)
- Try to ensure no host appears more than once per page if possible
- If not enough unique hosts exist, allow duplicates but preserve input order

Output: Reordered list (still preserving score ordering when possible) and printed in pages.

Example (page size = 3):
Input:
[
  "1,28,300.1,San Francisco",
  "4,56,295.0,Chicago",
  "20,80,290.5,New York",
  "6,29,285.0,San Francisco",
  "1,97,283.0,San Francisco",
  "6,32,280.0,Seattle",
  "20,55,279.0,Boston"
]

Output:
Page 1:
1,28,300.1,San Francisco
4,56,295.0,Chicago
20,80,290.5,New York

Page 2:
6,29,285.0,San Francisco
1,97,283.0,San Francisco
6,32,280.0,Seattle

Page 3:
20,55,279.0,Boston

INTERVIEW EXPLANATION: Why Greedy Round-Robin for Pagination?

1. **Problem Structure**: We need to paginate results while:
   - Maximizing host diversity per page (no duplicate hosts if possible)
   - Preserving score ordering (higher scores first)
   - Handling cases where we can't avoid duplicates

2. **Why Greedy Round-Robin?**
   - **Greedy Approach**: For each page, we try to select unique hosts first.
     This maximizes diversity locally (per page), which is optimal for user experience.
   
   - **Round-Robin Logic**: We process items in order, skipping items from hosts
     already on the current page. If the page isn't full after one pass, we go
     back and fill with skipped items (allowing duplicates).
   
   - **Time Complexity**: 
     * O(n) where n is total number of items
     * Each item is processed once per page it appears on
     * In worst case (all same host), O(n) still
   
   - **Space Complexity**: O(n) for storing items and pages

3. **Key Insight**: Use a queue to maintain order, and for each page:
   - First pass: Add items with unique hosts
   - Second pass: Fill remaining slots with any items (allowing duplicates)
   - This ensures we maximize diversity while preserving order
"""

from collections import deque
from typing import List, Tuple


def paginate_results(results: List[str], per_page: int = 12) -> List[List[str]]:
    """
    Paginate results ensuring maximum host diversity per page.
    
    Args:
        results: List of CSV strings in format "host_id,listing_id,score,city"
        per_page: Number of results per page
        
    Returns:
        List of pages, where each page is a list of CSV strings
    """
    # Parse input CSV strings
    parsed = [line.split(",") for line in results]
    
    # Store as (host_id, full_line) in a queue
    items = deque([(row[0], line) for row, line in zip(parsed, results)])
    
    output = []
    
    while items:
        page = []
        seen_hosts = set()
        skipped = []
        
        # First pass: Try to fill page with unique hosts
        while items and len(page) < per_page:
            host, line = items.popleft()
            if host not in seen_hosts:
                page.append(line)
                seen_hosts.add(host)
            else:
                skipped.append((host, line))
        
        # Second pass: If still space, add skipped items (duplicates allowed now)
        while skipped and len(page) < per_page:
            host, line = skipped.pop(0)
            page.append(line)
        
        # Put remaining skipped items back into queue (at front to maintain order)
        items.extendleft(reversed(skipped))
        
        output.append(page)
    
    return output


def print_pages(pages: List[List[str]]) -> None:
    """Print pages in a readable format"""
    for i, page in enumerate(pages, 1):
        print(f"Page {i}:")
        for line in page:
            print(line)
        print()


def test_pagination():
    """Test cases for pagination"""
    # Test case 1: Example from problem
    results1 = [
        "1,28,300.1,San Francisco",
        "4,56,295.0,Chicago",
        "20,80,290.5,New York",
        "6,29,285.0,San Francisco",
        "1,97,283.0,San Francisco",
        "6,32,280.0,Seattle",
        "20,55,279.0,Boston"
    ]
    
    pages1 = paginate_results(results1, per_page=3)
    assert len(pages1) == 3, f"Expected 3 pages, got {len(pages1)}"
    assert len(pages1[0]) == 3, f"Page 1 should have 3 items"
    assert len(pages1[1]) == 3, f"Page 2 should have 3 items"
    assert len(pages1[2]) == 1, f"Page 3 should have 1 item"
    
    # Check that page 1 has unique hosts
    hosts_page1 = set([page.split(',')[0] for page in pages1[0]])
    assert len(hosts_page1) == 3, f"Page 1 should have 3 unique hosts, got {len(hosts_page1)}"
    
    print("✓ Test 1 passed: Basic pagination with host diversity")
    
    # Test case 2: All same host (must allow duplicates)
    results2 = [
        "1,28,300.1,San Francisco",
        "1,56,295.0,Chicago",
        "1,80,290.5,New York",
        "1,29,285.0,San Francisco"
    ]
    pages2 = paginate_results(results2, per_page=2)
    assert len(pages2) == 2, f"Expected 2 pages, got {len(pages2)}"
    print("✓ Test 2 passed: All same host (duplicates allowed)")
    
    # Test case 3: Perfect diversity (each host appears once)
    results3 = [
        "1,28,300.1,San Francisco",
        "2,56,295.0,Chicago",
        "3,80,290.5,New York",
        "4,29,285.0,Seattle"
    ]
    pages3 = paginate_results(results3, per_page=2)
    assert len(pages3) == 2, f"Expected 2 pages, got {len(pages3)}"
    assert all(len(set([p.split(',')[0] for p in page])) == len(page) for page in pages3), \
        "Each page should have unique hosts"
    print("✓ Test 3 passed: Perfect diversity")
    
    print("\nAll tests passed!")


if __name__ == "__main__":
    test_pagination()
    
    # Example usage
    print("\nExample usage:")
    results = [
        "1,28,300.1,San Francisco",
        "4,56,295.0,Chicago",
        "20,80,290.5,New York",
        "6,29,285.0,San Francisco",
        "1,97,283.0,San Francisco",
        "6,32,280.0,Seattle",
        "20,55,279.0,Boston"
    ]
    
    pages = paginate_results(results, per_page=3)
    print_pages(pages)
# %%

