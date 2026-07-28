# Day 27: Code Letter Counter (String Counting) 🟢 Easy

## 📋 Problem Statement

Given a message string `S` and a target character `C`, determine how many times `C` occurs in `S`.

**Input Format:**
- First line: string `S`
- Second line: character `C`

**Output Format:** A single integer — the number of occurrences of `C` in `S`

**Constraints:**
- `1 ≤ Length of S ≤ 100`

**Example:** In `BALLOON`, the character `L` appears `2` times. In `MISSISSIPPI`, the character `S` appears `4` times.

---

## 🔍 Identifying the Problem

Strip away the coded-message framing and this is a plain **character counting** problem — count the occurrences of one character within a string. No algorithmic technique is needed beyond a direct scan or using a built-in counting function.

---

## 🧠 Steps of Execution

### Step 1 — Read the input
Read string `S` and character `C` from the standard input.

### Step 2 — Count occurrences
Use Python's built-in `str.count()` to count how many times `C` appears in `S`.

### Step 3 — Print the result
Print the resulting count to standard output.

---

## 💻 Final Code

```python
import sys

def main():
    # Read all input from standard input
    data = sys.stdin.read().split()
    if len(data) < 2:
        return
    
    s = data[0]
    c = data[1]
    
    print(s.count(c))

if __name__ == "__main__":
    main()
```

---

## 🔬 Dry Run — Testcase 1

Input:
```
BALLOON
L
```

- `s = "BALLOON"`, `c = "L"`
- `s.count("L")` → `L` appears at indices 2 and 3 → `2`

**Output: `2`** ✅

Input:
```
MISSISSIPPI
S
```

- `s = "MISSISSIPPI"`, `c = "S"`
- `s.count("S")` → `S` appears 4 times → `4`

**Output: `4`** ✅

---

## ⏱ Complexity

| Metric | Complexity | Why |
|---|---|---|
| Time | $O(|S|)$ | Python's built-in `count()` scans the string in a single linear pass. |
| Space | $O(|S|)$ | Storing the input string in memory requires linear space relative to its length. |

---

## 💡 Lesson Learned

Not every problem needs custom logic — Python's built-in string methods like `count()` handle simple, well-defined tasks like this in a single line. Recognizing when a problem is this direct saves time that can be spent double-checking edge cases (e.g., handling potential empty inputs or making sure the target character is read correctly as a single token) rather than overengineering a solution.
