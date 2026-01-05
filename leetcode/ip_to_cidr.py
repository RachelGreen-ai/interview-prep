# LeetCode 751: IP to CIDR
#%%
"""
Problem Statement:
------------------
Given a start IP address ip and a number n representing the count of IP addresses 
to cover, return a list of CIDR blocks that collectively cover the range from ip 
to ip + n - 1. Each CIDR block should be represented in the format "a.b.c.d/x", 
where "a.b.c.d" is the base IP address and "x" is the prefix length indicating 
the number of fixed bits in the subnet mask.

Example 1:
Input: ip = "255.0.0.7", n = 10
Output: ["255.0.0.7/32", "255.0.0.8/29", "255.0.0.16/32"]
Explanation:
- "255.0.0.7/32" covers only IP 255.0.0.7 (1 address)
- "255.0.0.8/29" covers IPs 255.0.0.8 to 255.0.0.15 (8 addresses)
- "255.0.0.16/32" covers only IP 255.0.0.16 (1 address)
Total: 1 + 8 + 1 = 10 addresses

Example 2:
Input: ip = "117.145.102.62", n = 8
Output: ["117.145.102.62/31", "117.145.102.64/30", "117.145.102.68/31"]

KEY CONCEPTS:
------------
1. **IP Address**: 32-bit integer represented as 4 octets (a.b.c.d)
   - Each octet is 8 bits (0-255)
   - Example: 255.0.0.7 = 11111111.00000000.00000000.00000111

2. **CIDR Notation**: "a.b.c.d/x" where x is prefix length
   - x = number of fixed bits (network portion)
   - (32-x) = number of variable bits (host portion)
   - Block size = 2^(32-x) addresses
   - Example: /29 means 3 variable bits → 2^3 = 8 addresses

3. **Lowest Set Bit (LSB)**: 
   - For IP address, LSB determines maximum block size we can use
   - We can't cross subnet boundaries (must align to power of 2)
   - Example: IP 7 (binary: 111) has LSB = 1, so we can use block size 1
   - Example: IP 8 (binary: 1000) has LSB = 8, so we can use block size 8

APPROACH:
---------
1. Convert IP to 32-bit integer for easier manipulation
2. While n > 0:
   a. Find lowest set bit (LSB) of current IP → maximum block size
   b. Adjust block size to not exceed remaining n
   c. Create CIDR block with appropriate prefix length
   d. Move IP forward by block size
   e. Decrease n by block size
3. Return list of CIDR blocks

TIME COMPLEXITY: O(n) in worst case, but typically much better due to power-of-2 blocks
SPACE COMPLEXITY: O(1) excluding output array

INTERVIEW TIPS:
--------------
1. Key insight: Use bit manipulation to find maximum block size
2. Lowest set bit trick: `x & -x` gives the lowest set bit
3. Block size must be power of 2 and not exceed remaining count
4. Prefix length calculation: 32 - log2(block_size)
5. Edge cases:
   - n = 1 (single IP)
   - IP at boundary (e.g., 255.255.255.255)
   - Large n values
"""

from typing import List

class Solution:
    def ipToCIDR(self, ip: str, n: int) -> List[str]:
        """
        Convert IP range to minimal CIDR blocks.
        
        Strategy:
        - Convert IP to integer for easier manipulation
        - Use lowest set bit to determine maximum block size
        - Create CIDR blocks greedily (largest possible first)
        - Continue until all n addresses are covered
        
        Args:
            ip: Starting IP address (e.g., "255.0.0.7")
            n: Number of IP addresses to cover
            
        Returns:
            List of CIDR blocks in format "a.b.c.d/x"
        """
        def ip_to_int(ip: str) -> int:
            """Convert IP address string to 32-bit integer"""
            parts = list(map(int, ip.split('.')))
            # Convert to integer: a.b.c.d = a*256^3 + b*256^2 + c*256 + d
            result = 0
            for part in parts:
                result = result * 256 + part
            return result
        
        def int_to_ip(ip_int: int) -> str:
            """Convert 32-bit integer to IP address string"""
            parts = []
            for _ in range(4):
                parts.append(str(ip_int & 255))  # Get last 8 bits
                ip_int >>= 8  # Shift right by 8 bits
            return '.'.join(reversed(parts))
        
        start = ip_to_int(ip)
        result = []
        
        while n > 0:
            # Find lowest set bit (LSB) - this is the maximum block size we can use
            # without crossing a subnet boundary
            # Example: IP 7 (binary: 111) → LSB = 1
            #         IP 8 (binary: 1000) → LSB = 8
            # Trick: x & -x gives the lowest set bit
            step = start & -start
            
            # If step is 0, it means start is 0 (shouldn't happen for valid IPs)
            if step == 0:
                step = 1
            
            # Adjust step to not exceed remaining count n
            # We want the largest power of 2 that fits in n
            while step > n:
                step //= 2
            
            # Calculate prefix length
            # Block size = step, so we need (32 - log2(step)) prefix bits
            # Example: step = 8 = 2^3, so prefix = 32 - 3 = 29
            prefix_length = 32 - (step.bit_length() - 1)
            
            # Create CIDR block
            cidr = f"{int_to_ip(start)}/{prefix_length}"
            result.append(cidr)
            
            # Move forward by step and decrease remaining count
            start += step
            n -= step
        
        return result

#%% TEST CASES WITH EXPLANATIONS

def test_basic_cases():
    """Test basic cases from examples"""
    print("=" * 70)
    print("TEST 1: Basic Cases")
    print("=" * 70)
    sol = Solution()
    
    # Test 1: Example 1
    ip1, n1 = "255.0.0.7", 10
    result1 = sol.ipToCIDR(ip1, n1)
    print(f"\n1. ip = '{ip1}', n = {n1}")
    print(f"   Expected: ['255.0.0.7/32', '255.0.0.8/29', '255.0.0.16/32']")
    print(f"   Got: {result1}")
    print(f"   Explanation:")
    print(f"   - IP 255.0.0.7 (binary: ...00000111) → LSB = 1 → block size 1")
    print(f"     CIDR: 255.0.0.7/32 (covers 1 address)")
    print(f"   - IP 255.0.0.8 (binary: ...00001000) → LSB = 8 → block size 8")
    print(f"     CIDR: 255.0.0.8/29 (covers 8 addresses: 8-15)")
    print(f"   - IP 255.0.0.16 (binary: ...00010000) → LSB = 16, but n=1 → block size 1")
    print(f"     CIDR: 255.0.0.16/32 (covers 1 address)")
    print(f"   Total: 1 + 8 + 1 = 10 addresses ✓")
    
    # Test 2: Example 2
    ip2, n2 = "117.145.102.62", 8
    result2 = sol.ipToCIDR(ip2, n2)
    print(f"\n2. ip = '{ip2}', n = {n2}")
    print(f"   Result: {result2}")
    print(f"   Explanation: Covers 8 consecutive IPs starting from 117.145.102.62")

def test_edge_cases():
    """Test edge cases"""
    print("\n" + "=" * 70)
    print("TEST 2: Edge Cases")
    print("=" * 70)
    sol = Solution()
    
    # Test 1: Single IP (n = 1)
    ip1, n1 = "192.168.1.1", 1
    result1 = sol.ipToCIDR(ip1, n1)
    print(f"\n1. ip = '{ip1}', n = {n1} (single IP)")
    print(f"   Result: {result1}")
    print(f"   Explanation: Single IP always uses /32 (covers 1 address)")
    assert result1 == ["192.168.1.1/32"]
    
    # Test 2: Power of 2 block size
    ip2, n2 = "192.168.1.0", 8
    result2 = sol.ipToCIDR(ip2, n2)
    print(f"\n2. ip = '{ip2}', n = {n2} (power of 2)")
    print(f"   Result: {result2}")
    print(f"   Explanation: IP ends in 0, LSB = 256, but n=8 → uses block size 8")
    print(f"   Should use /29 (covers 8 addresses)")
    
    # Test 3: Large block
    ip3, n3 = "10.0.0.0", 256
    result3 = sol.ipToCIDR(ip3, n3)
    print(f"\n3. ip = '{ip3}', n = {n3} (large block)")
    print(f"   Result: {result3}")
    print(f"   Explanation: IP ends in 0, LSB allows large block")
    print(f"   Should use /24 (covers 256 addresses)")
    
    # Test 4: Odd starting IP with small n
    ip4, n4 = "192.168.1.3", 2
    result4 = sol.ipToCIDR(ip4, n4)
    print(f"\n4. ip = '{ip4}', n = {n4} (odd IP, small n)")
    print(f"   Result: {result4}")
    print(f"   Explanation: IP 3 (binary: 11) → LSB = 1, but n=2")
    print(f"   Uses two /32 blocks or one /31 block")

def test_complex_cases():
    """Test more complex cases"""
    print("\n" + "=" * 70)
    print("TEST 3: Complex Cases")
    print("=" * 70)
    sol = Solution()
    
    # Test 1: Non-aligned starting IP
    ip1, n1 = "192.168.1.5", 12
    result1 = sol.ipToCIDR(ip1, n1)
    print(f"\n1. ip = '{ip1}', n = {n1}")
    print(f"   Result: {result1}")
    print(f"   Explanation: Starts at odd IP, needs multiple blocks")
    
    # Test 2: Boundary case
    ip2, n2 = "255.255.255.250", 6
    result2 = sol.ipToCIDR(ip2, n2)
    print(f"\n2. ip = '{ip2}', n = {n2} (near max IP)")
    print(f"   Result: {result2}")
    print(f"   Explanation: Near 255.255.255.255 boundary")

def explain_cidr():
    """Explain CIDR notation and bit manipulation"""
    print("\n" + "=" * 70)
    print("CIDR NOTATION EXPLANATION")
    print("=" * 70)
    
    print("\n1. IP Address Structure:")
    print("   - 32-bit integer: 4 octets of 8 bits each")
    print("   - Example: 255.0.0.7 = 11111111.00000000.00000000.00000111")
    
    print("\n2. CIDR Format: a.b.c.d/x")
    print("   - x = prefix length (number of fixed network bits)")
    print("   - (32-x) = number of variable host bits")
    print("   - Block size = 2^(32-x) addresses")
    
    print("\n3. Examples:")
    examples = [
        ("/32", 32, 1, "Single IP address"),
        ("/31", 31, 2, "Two IP addresses"),
        ("/30", 30, 4, "Four IP addresses"),
        ("/29", 29, 8, "Eight IP addresses"),
        ("/24", 24, 256, "256 IP addresses (class C)"),
    ]
    
    for cidr, prefix, size, desc in examples:
        print(f"   {cidr}: prefix={prefix}, block_size={size} → {desc}")
    
    print("\n4. Lowest Set Bit (LSB) Trick:")
    print("   - x & -x gives the lowest set bit")
    print("   - Example: 7 & -7 = 1 (binary: 111 & ...001 = 001)")
    print("   - Example: 8 & -8 = 8 (binary: 1000 & ...1000 = 1000)")
    print("   - This tells us the maximum block size we can use")
    
    print("\n5. Why This Works:")
    print("   - CIDR blocks must align to power-of-2 boundaries")
    print("   - IP 7 (binary: 111) can only start blocks of size 1, 2, or 4")
    print("   - IP 8 (binary: 1000) can start blocks of size 1, 2, 4, 8, 16, ...")
    print("   - LSB gives us the largest possible block size for current IP")

def visualize_example():
    """Visualize a specific example"""
    print("\n" + "=" * 70)
    print("VISUALIZATION: ip = '255.0.0.7', n = 10")
    print("=" * 70)
    
    ip = "255.0.0.7"
    n = 10
    
    def ip_to_int(ip_str):
        parts = list(map(int, ip_str.split('.')))
        return sum(parts[i] << (24 - 8*i) for i in range(4))
    
    def int_to_ip(ip_int):
        return '.'.join(str((ip_int >> (24 - 8*i)) & 255) for i in range(4))
    
    start = ip_to_int(ip)
    print(f"\nStarting IP: {ip} = {start} (decimal)")
    print(f"Binary: {start:032b}")
    print(f"\nCovering {n} addresses:\n")
    
    current = start
    remaining = n
    block_num = 1
    
    while remaining > 0:
        step = current & -current
        if step == 0:
            step = 1
        while step > remaining:
            step //= 2
        
        prefix = 32 - (step.bit_length() - 1)
        end = current + step - 1
        
        print(f"Block {block_num}:")
        print(f"  IP range: {int_to_ip(current)} to {int_to_ip(end)}")
        print(f"  CIDR: {int_to_ip(current)}/{prefix}")
        print(f"  Size: {step} addresses")
        print(f"  Binary start: {current:032b}")
        print()
        
        current += step
        remaining -= step
        block_num += 1

# Run all tests
if __name__ == "__main__":
    test_basic_cases()
    test_edge_cases()
    test_complex_cases()
    explain_cidr()
    visualize_example()

# %%

