# Day 25: Mirror Word Check (String / Palindrome) 🟢 Easy

## 📋 Problem Statement

Given a string `S` containing only lowercase English letters, determine whether it is a "Mirror Word" — a word that reads the same from left to right and from right to left. Print `YES` if it is, `NO` otherwise.

**Input Format:** A single string `S`

**Output Format:** `YES` if `S` is a Mirror Word, `NO` otherwise

**Constraints:**
- `1 ≤ |S| ≤ 100`
- `S` contains only lowercase English letters

**Example:** `level` reversed is still `level` → `YES`. `apple` reversed is `elppa` → `NO`.

---

## 🔍 Identifying the Problem

Strip away the "Mirror Word" naming and this is simply a **palindrome check** — one of the most fundamental string problems. A string reads the same in both directions if and only if it equals its own reverse.

---

## 🧠 Steps of Execution

### Step 1 — Read the string
Read the single string `S` from input.

### Step 2 — Compare with its reverse
Reverse `S` using slicing (`S[::-1]`) and compare it against the original.

### Step 3 — Print the result
Print `YES` if they match, `NO` otherwise.

---

## 💻 Final Code

```python
import sys

def main():
    # Read all input from standard input
    data = sys.stdin.read().split()
    if not data:
        return
    
    s = data[0]
    
    # Check if the string is equal to its reverse
    if s == s[::-1]:
        print("YES")
    else:
        print("NO")

if __name__ == "__main__":
    main()
```

---

## 🔬 Dry Run — Testcase 1

Input: `level`

- Reverse of `level` is `level`
- `s == s[::-1]` → `True`

**Output: `YES`** ✅

Input: `apple`

- Reverse of `apple` is `elppa`
- `s == s[::-1]` → `False`

**Output: `NO`** ✅

---

## ⏱ Complexity

| Metric | Complexity | Why |
|---|---|---|
| Time | $O(|S|)$ | Reversing and comparing strings of length $|S|$ takes linear time. |
| Space | $O(|S|)$ | Python's slice operation `S[::-1]` creates a new reversed copy of string $S$. |

---

## 💡 Lesson Learned

Not every problem in a challenge needs a fancy algorithm — recognizing when a creatively-worded problem ("Mirror Word") maps directly onto a well-known, trivial pattern (palindrome check) is itself a useful skill, and Python's slice notation (`s[::-1]`) makes such checks a one-liner without needing any explicit loop or helper function.
