# Travel Buddy Problem
#%%
"""
Problem Statement:
Each person has a set of cities they want to visit.
Define similarity(A, B) = Jaccard similarity = |A ∩ B| / |A ∪ B|
If similarity > 0.5 → A and B are travel buddies.
For a given person P, output a sorted list of buddies by similarity score (high → low).

Example:
people = {
  "Alice": {"Paris", "London", "Tokyo"},
  "Bob": {"London", "Berlin", "Tokyo", "Paris"},
  "Charlie": {"Beijing", "Tokyo", "Paris"},
  "Diana": {"San Francisco", "LA"}
}

For Alice:
- Similarity with Bob: |{Paris, London, Tokyo} ∩ {London, Berlin, Tokyo, Paris}| / |{Paris, London, Tokyo, Berlin}| 
  = 3 / 4 = 0.75 > 0.5 ✓
- Similarity with Charlie: |{Paris, Tokyo}| / |{Paris, London, Tokyo, Beijing}| = 2 / 4 = 0.5 (not > 0.5)
- Similarity with Diana: 0 / 5 = 0 (not > 0.5)

Output: [('Bob', 0.75)]

INTERVIEW EXPLANATION: Why Jaccard Similarity + Optimization Strategies?

1. **Problem Structure**: We need to find people with similar travel interests.
   Similarity is measured by overlap in cities they want to visit.

2. **Why Jaccard Similarity?**
   - **Symmetric**: Jaccard(A, B) = Jaccard(B, A), which makes sense for mutual interests
   - **Normalized**: Always between 0 and 1, easy to interpret
   - **Set-based**: Perfect for comparing sets of cities
   - **Standard Metric**: Commonly used in recommendation systems

3. **Approach 1: Brute Force (Baseline)**
   - Compare each person with every other person
   - Time: O(n²·m) where n = #people, m = avg cities per person
   - Space: O(n·m) for storing all people's cities
   - Good for: Small datasets (hundreds of users)

4. **Approach 2: Inverted Index (Optimization)**
   - Build index: city → list of people interested
   - Only compare with people sharing at least one city
   - Time: O(n·m·p) where p = avg people per city (usually p << n)
   - Good for: Sparse datasets where interests don't overlap much

5. **Approach 3: Embeddings + ANN (Advanced)**
   - Represent each person as embedding vector
   - Use Approximate Nearest Neighbor search
   - Time: ~O(n·log n) for large scale
   - Good for: Millions of users, semantic similarity

6. **Key Insight**: Start with brute force to show understanding, then discuss
   optimizations. Mention embeddings if semantic similarity matters (e.g., 
   "Paris" and "Rome" are similar even if sets don't overlap).
"""

from typing import Dict, Set, List, Tuple


def jaccard_similarity(set_a: Set[str], set_b: Set[str]) -> float:
    """
    Calculate Jaccard similarity between two sets.
    Jaccard(A, B) = |A ∩ B| / |A ∪ B|
    
    Args:
        set_a: First set
        set_b: Second set
        
    Returns:
        Jaccard similarity score (0.0 to 1.0)
    """
    intersection = len(set_a & set_b)
    union = len(set_a | set_b)
    
    if union == 0:
        return 0.0
    
    return intersection / union


def find_travel_buddies_brute_force(
    person: str, 
    people: Dict[str, Set[str]], 
    threshold: float = 0.5
) -> List[Tuple[str, float]]:
    """
    Find travel buddies using brute force approach.
    Compare person with every other person.
    
    Time Complexity: O(n²·m) where n = #people, m = avg cities per person
    Space Complexity: O(1) extra space
    
    Args:
        person: Name of the person to find buddies for
        people: Dictionary mapping person names to their city sets
        threshold: Minimum similarity to be considered a buddy
        
    Returns:
        List of (buddy_name, similarity_score) tuples, sorted by score descending
    """
    if person not in people:
        return []
    
    target = people[person]
    buddies = []
    
    for other, cities in people.items():
        if other == person:
            continue
        
        sim = jaccard_similarity(target, cities)
        if sim > threshold:
            buddies.append((other, sim))
    
    # Sort by similarity descending
    buddies.sort(key=lambda x: -x[1])
    return buddies


def find_travel_buddies_optimized(
    person: str,
    people: Dict[str, Set[str]],
    threshold: float = 0.5
) -> List[Tuple[str, float]]:
    """
    Find travel buddies using inverted index optimization.
    Only compare with people sharing at least one city.
    
    Time Complexity: O(n·m·p) where p = avg people per city
    Space Complexity: O(c·p) for inverted index where c = #cities
    
    Args:
        person: Name of the person to find buddies for
        people: Dictionary mapping person names to their city sets
        threshold: Minimum similarity to be considered a buddy
        
    Returns:
        List of (buddy_name, similarity_score) tuples, sorted by score descending
    """
    if person not in people:
        return []
    
    target = people[person]
    
    # Build inverted index: city -> set of people
    city_to_people: Dict[str, Set[str]] = {}
    for p, cities in people.items():
        for city in cities:
            if city not in city_to_people:
                city_to_people[city] = set()
            city_to_people[city].add(p)
    
    # Find candidate buddies (people sharing at least one city)
    candidate_buddies = set()
    for city in target:
        if city in city_to_people:
            candidate_buddies.update(city_to_people[city])
    
    # Remove self
    candidate_buddies.discard(person)
    
    # Compute similarity only for candidates
    buddies = []
    for other in candidate_buddies:
        sim = jaccard_similarity(target, people[other])
        if sim > threshold:
            buddies.append((other, sim))
    
    buddies.sort(key=lambda x: -x[1])
    return buddies


def test_travel_buddy():
    """Test cases for Travel Buddy"""
    people = {
        "Alice": {"Paris", "London", "Tokyo"},
        "Bob": {"London", "Berlin", "Tokyo", "Paris"},
        "Charlie": {"Beijing", "Tokyo", "Paris"},
        "Diana": {"San Francisco", "LA"}
    }
    
    # Test brute force
    buddies1 = find_travel_buddies_brute_force("Alice", people, threshold=0.5)
    assert len(buddies1) == 1, f"Expected 1 buddy, got {len(buddies1)}"
    assert buddies1[0][0] == "Bob", f"Expected Bob, got {buddies1[0][0]}"
    assert abs(buddies1[0][1] - 0.75) < 0.01, f"Expected similarity ~0.75, got {buddies1[0][1]}"
    print(f"✓ Test 1 (brute force): {buddies1}")
    
    # Test optimized
    buddies2 = find_travel_buddies_optimized("Alice", people, threshold=0.5)
    assert len(buddies2) == 1, f"Expected 1 buddy, got {len(buddies2)}"
    assert buddies2[0][0] == "Bob", f"Expected Bob, got {buddies2[0][0]}"
    print(f"✓ Test 2 (optimized): {buddies2}")
    
    # Test with lower threshold (should include Charlie)
    buddies3 = find_travel_buddies_brute_force("Alice", people, threshold=0.4)
    assert len(buddies3) == 2, f"Expected 2 buddies, got {len(buddies3)}"
    print(f"✓ Test 3 (lower threshold): {buddies3}")
    
    # Test person with no buddies
    buddies4 = find_travel_buddies_brute_force("Diana", people, threshold=0.5)
    assert len(buddies4) == 0, f"Expected 0 buddies, got {len(buddies4)}"
    print("✓ Test 4 (no buddies): []")
    
    print("\nAll tests passed!")


if __name__ == "__main__":
    test_travel_buddy()
    
    # Example usage
    print("\nExample usage:")
    people = {
        "Alice": {"Paris", "London", "Tokyo"},
        "Bob": {"London", "Berlin", "Tokyo", "Paris"},
        "Charlie": {"Beijing", "Tokyo", "Paris"},
        "Diana": {"San Francisco", "LA"}
    }
    
    print("Finding buddies for Alice:")
    buddies = find_travel_buddies_brute_force("Alice", people)
    for buddy, score in buddies:
        print(f"  {buddy}: {score:.2f}")
# %%

