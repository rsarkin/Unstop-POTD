# Day 24: Beacon Synchronization Energy (Mo's Algorithm — Offline Range Queries) 🔴 Hard

## 📋 Problem Statement

The Celestial Ring consists of `N` energy beacons, each emitting a frequency code. For `Q` diagnostic requests, each asking about a range `[L, R]`, compute the **Synchronization Energy** of that section — the sum of `f²` over every distinct frequency code, where `f` is how many times that code appears in the range.

**Input Format:**
- First line: `N` and `Q`
- Second line: `N` integers (beacon frequency codes)
- Next `Q` lines: `L R` describing each inspection range

**Output Format:** The Synchronization Energy for each query, each on its own line

**Constraints:**
- `1 ≤ N, Q ≤ 2 × 10^5`
- `1 ≤ Frequency Code ≤ 10^6`
- `1 ≤ L ≤ R ≤ N`
- Answer fits in a signed 64-bit integer

**Example:** For range `5 5 3 8 3 8 5 8 8 2`, frequencies are `5→3, 3→2, 8→4, 2→1`, giving `9+4+16+1=30`.

---

## 🔍 Identifying the Problem

Strip away the beacon framing and this is a classic **offline range-query** problem asking for a sum-of-squares-of-frequencies over arbitrary subarrays, with up to `2 × 10^5` queries. Recomputing frequencies from scratch for every query is $O(N)$ per query — $O(N \times Q)$ overall, which is far too slow. Since all queries are known upfront (offline) and the array is static, this is the textbook setup for **Mo's Algorithm**: reorder queries so a sliding window can answer them all with only $O((N + Q) \sqrt{N})$ total pointer movement, instead of resetting from scratch each time.

The key trick that avoids recomputing frequencies inside the window: when a frequency code's count changes from $cnt$ to $cnt + 1$, its contribution changes from $cnt^2$ to $(cnt + 1)^2$ — a delta of exactly $2 \cdot cnt + 1$. This lets a single running `energy` total be updated in $O(1)$ per element added or removed, rather than summing all frequencies each time.

---

## 🧠 Steps of Execution

### Step 1 — Read input and queries
Read `N`, `Q`, the array, and all `Q` queries (converted to 0-indexed).

### Step 2 — Apply Mo's ordering
Divide the array into blocks of size $\approx \sqrt{N}$. Sort queries by `(block of L, R)` — alternating ascending/descending `R` per block to reduce pointer thrashing (also known as the sorting optimization).

### Step 3 — Slide the window
Maintain a window `[cl, cr]` and a `freq[]` array. For each query, move `cl`/`cr` one step at a time toward the target range, updating `energy` incrementally on every single add/remove using the $2 \cdot cnt + 1$ delta trick.

### Step 4 — Record and output
Once the window matches the query's exact range, store `energy` as that query's answer (indexed by original query order). Print all answers, one per line.

---

## 💻 Final Code

```python
import sys

def main():
    # Fast I/O
    input_data = sys.stdin.buffer.read().split()
    if not input_data:
        return
    idx = 0
    n = int(input_data[idx]); idx += 1
    q = int(input_data[idx]); idx += 1

    arr = [0] * n
    max_val = 0
    for i in range(n):
        val = int(input_data[idx]); idx += 1
        arr[i] = val
        if val > max_val:
            max_val = val

    block = max(1, int(n ** 0.5))
    queries = []
    for i in range(q):
        l = int(input_data[idx]) - 1; idx += 1
        r = int(input_data[idx]) - 1; idx += 1
        b = l // block
        # Alternating sorting for Mo's Algorithm
        key_r = r if b % 2 == 0 else -r
        queries.append((b, key_r, l, r, i))

    queries.sort()

    freq = [0] * (max(10**6, max_val) + 2)
    answers = [0] * q
    energy = 0
    cl, cr = 0, -1

    for b, key_r, l, r, orig_i in queries:
        while cr < r:
            cr += 1
            x = arr[cr]
            energy += 2 * freq[x] + 1
            freq[x] += 1
        while cr > r:
            x = arr[cr]
            freq[x] -= 1
            energy -= 2 * freq[x] + 1
            cr -= 1
        while cl > l:
            cl -= 1
            x = arr[cl]
            energy += 2 * freq[x] + 1
            freq[x] += 1
        while cl < l:
            x = arr[cl]
            freq[x] -= 1
            energy -= 2 * freq[x] + 1
            cl += 1
        answers[orig_i] = energy

    sys.stdout.write('\n'.join(map(str, answers)) + '\n')

if __name__ == "__main__":
    main()
```

---

## 🔬 Dry Run — Testcase 1

Input: `10 2 / 5 5 3 8 3 8 5 8 8 2 / 1 10 / 4 9`

Query `1 10` (0-indexed `0 9`): window expands to cover the full array. Frequencies build up: `5→3, 3→2, 8→4, 2→1`. Running energy accumulates to `9 + 4 + 16 + 1 = 30`.

Query `4 9` (0-indexed `3 8`): window shifts — array is `8 3 8 5 8 8`. Frequencies: `8→4, 3→1, 5→1`. Energy: `16 + 1 + 1 = 18`.

**Output:**
```
30
18
```
✅

---

## ⏱ Complexity

| Metric | Complexity | Why |
|---|---|---|
| Time | $O((N + Q) \sqrt{N})$ | Mo's ordering bounds total pointer movement across all queries to this bound. |
| Space | $O(N + \text{max frequency code})$ | Array storage plus the `freq[]` counting array. |

---

## 💡 Lesson Learned

This one earns its "hard" rating: whenever a problem has **many offline range queries** on a **static array** asking for something that changes predictably with single-element insertion/removal (like sum of squares of frequencies), Mo's Algorithm is the go-to pattern — it converts what looks like an $O(N \times Q)$ problem into $O((N + Q) \sqrt{N})$ by cleverly reordering queries instead of needing a fancier per-query data structure. It took combining an unfamiliar technique (Mo's ordering) with a subtle math identity ($f^2 \to (f+1)^2$ delta = $2f+1$) to get an efficient solution.
