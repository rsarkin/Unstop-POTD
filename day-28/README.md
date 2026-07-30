# Day 28: The Missing Preservation Entry (Bit Manipulation — XOR)

## 📋 Problem Statement

A merged ledger contains `N` artifact registration numbers, where every number appears exactly twice except for one, which appears only once — the newly excavated artifact still awaiting preservation. Find and print that registration number.

**Input Format:**
- First line: `N` (total number of registration numbers, always odd)
- Second line: `N` space-separated integers representing the merged ledger

**Output Format:** The registration number that appears only once

**Constraints:**
- `1 ≤ N ≤ 100000`
- `N` is always odd
- `1 ≤ Registration Number ≤ 10^9`
- Exactly one number appears once; every other number appears exactly twice

**Example:** In `312 451 129 312 451 278 129`, every number appears twice except `278`, which appears once. Output: `278`.

---

## 🔍 Identifying the Problem

Strip away the museum framing and this is the classic **"Single Number"** problem — find the one element that doesn't have a pair in an array where every other element appears exactly twice. This is a textbook signal for the **XOR bit manipulation trick**, since XOR-ing a number with itself cancels to zero (`x ^ x = 0`), and XOR-ing with zero leaves a number unchanged (`x ^ 0 = x`).

---

## 🧠 Steps of Execution

### Step 1 — Read the input
Read `N` and the `N` registration numbers from the merged ledger.

### Step 2 — XOR all numbers together
Initialize a result accumulator to `0`, then XOR every registration number into it, one at a time. Every number that appears twice cancels itself out during this process.

### Step 3 — Print the result
The leftover value in the accumulator after processing all numbers is exactly the registration number that appeared only once.

---

## 💻 Final Code

```python
import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    
    n = int(data[0])
    result = 0
    for i in range(1, n + 1):
        result ^= int(data[i])
    
    print(result)

if __name__ == "__main__":
    main()
```

---

## 🔬 Dry Run — Testcase 1

Input: `7 / 312 451 129 312 451 278 129`

- `result = 0`
- `0 ^ 312 = 312`
- `312 ^ 451 = ...` (some intermediate value)
- `... ^ 129 = ...`
- `... ^ 312 = ...` → the second `312` cancels the first `312`
- `... ^ 451 = ...` → the second `451` cancels the first `451`
- `... ^ 278 = ...`
- `... ^ 129 = ...` → the second `129` cancels the first `129`

After all pairs cancel out, only `278` remains.

**Output: `278`** ✅

---

## ⏱ Complexity

| Metric | Complexity | Why |
|---|---|---|
| Time | O(N) | A single pass through the array, XOR-ing each element once |
| Space | O(1) | Only one accumulator variable is used, regardless of input size |

---

## 💡 Lesson Learned

Whenever a problem says "every element appears exactly twice except one," XOR is almost always the intended trick — it solves in O(N) time and O(1) space, completely avoiding the need for a hash map or sorting (which would cost O(N) space or O(N log N) time respectively). This pattern is worth recognizing instantly, since the story details (museums, artifacts, ledgers) are just dressing on top of the same well-known bitwise identity.
