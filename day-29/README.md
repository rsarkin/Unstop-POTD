# Day 29: Subtree Score Spread (Tree DFS/BFS + Subtree Aggregation)

## 📋 Problem Statement

A company has `N` employees organized into a reporting tree rooted at employee 1 (the CEO), connected by `N-1` weighted edges representing adjustment scores. For any employee `v`, `pathScore(v)` is the sum of adjustment scores along the path from the root to `v`. For any employee `v`, `spread(v)` is the difference between the maximum and minimum `pathScore` among all employees in the subtree rooted at `v` (including `v` itself). Given `Q` queries, each naming an employee, output `spread(v)` for each.

**Input Format:**
- `N`
- `N-1` lines: `u v w` — an edge between employees `u` and `v` with adjustment score `w`
- `Q`
- `Q` lines: an employee ID `v` to query

**Output Format:** For each query, print `spread(v)` on its own line

**Constraints:**
- `2 ≤ N ≤ 2 × 10^5`
- `1 ≤ Q ≤ 2 × 10^5`
- `-10^9 ≤ w ≤ 10^9`
- Time Limit: 1.5 sec, Memory Limit: 256 MB

**Example:** With edges `1-2(5), 1-3(10), 1-4(-5)`, path scores are `1=0, 2=5, 3=10, 4=-5`. Subtree(1) covers everyone: `max=10, min=-5, spread=15`. Employees 2 and 4 are leaves, so their own spread is `0`.

---

## 🔍 Identifying the Problem

Strip away the corporate framing and this is a **Tree DFS/BFS + Subtree Aggregation** problem. Two distinct pieces need computing: `pathScore(v)` is a straightforward root-to-node prefix sum, computable with a single BFS/DFS pass. `spread(v)` requires aggregating min/max `pathScore` values across an entire subtree — a classic "process children before parents" pattern. With `N, Q` up to `2×10^5`, everything must run in O(N + Q) using **iterative** traversal (no recursion, to avoid stack overflow on deep/skewed trees), so every query can be answered by O(1) array lookup after one preprocessing pass.

---

## 🧠 Steps of Execution

### Step 1 — Read the tree
Build an adjacency list from the `N-1` weighted edges (bidirectional, since the tree is undirected but rooted at 1).

### Step 2 — BFS from the root
Starting at employee 1, do an iterative BFS. For each newly visited node, record its `parent`, compute its `pathScore` as `parent's pathScore + edge weight`, and append it to the visit `order` list. Since BFS visits parents before children, this `order` list is a valid "top-down" processing order.

### Step 3 — Aggregate min/max in reverse order
Initialize `lo[v] = hi[v] = pathScore[v]` for every node. Process nodes in **reverse** of the BFS order (children before parents) — for each non-root node, update its parent's `lo`/`hi` using `min`/`max` against the child's already-finalized values. By the time a parent is processed, all its descendants have already contributed.

### Step 4 — Answer queries
For each query `v`, print `hi[v] - lo[v]`.

---

## 💻 Final Code

```python
import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    idx = 0
    n = int(data[idx]); idx += 1

    adj = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        u, v, w = int(data[idx]), int(data[idx+1]), int(data[idx+2]); idx += 3
        adj[u].append((v, w)); adj[v].append((u, w))

    score = [0] * (n + 1)
    par = [0] * (n + 1)
    order = [1]
    seen = [False] * (n + 1); seen[1] = True

    for cur in order:
        for nxt, w in adj[cur]:
            if not seen[nxt]:
                seen[nxt] = True
                par[nxt] = cur
                score[nxt] = score[cur] + w
                order.append(nxt)

    lo, hi = score[:], score[:]
    for cur in reversed(order):
        if cur != 1:
            p = par[cur]
            lo[p] = min(lo[p], lo[cur])
            hi[p] = max(hi[p], hi[cur])

    q = int(data[idx]); idx += 1
    print('\n'.join(str(hi[int(data[idx+i])] - lo[int(data[idx+i])]) for i in range(q)))

if __name__ == "__main__":
    main()
```

---

## 🔬 Dry Run — Testcase 1

Input: `6 / 1 2 5 / 1 3 -2 / 2 4 3 / 2 5 -6 / 3 6 4 / 4 / 1 2 3 4`

BFS from 1: `pathScore = {1:0, 2:5, 3:-2, 4:8, 5:-1, 6:2}`, `order = [1,2,3,4,5,6]`, parents: `par[2]=1, par[3]=1, par[4]=2, par[5]=2, par[6]=3`

Reverse aggregation (`6,5,4,3,2`):
- `cur=6`: updates parent 3 → `lo[3]=min(-2,2)=-2`, `hi[3]=max(-2,2)=2`
- `cur=5`: updates parent 2 → `lo[2]=min(5,-1)=-1`, `hi[2]=5`
- `cur=4`: updates parent 2 → `lo[2]=min(-1,8)=-1`, `hi[2]=max(5,8)=8`
- `cur=3`: updates parent 1 → `lo[1]=min(0,-2)=-2`, `hi[1]=max(0,2)=2`
- `cur=2`: updates parent 1 → `lo[1]=min(-2,-1)=-2`, `hi[1]=max(2,8)=8`

Queries: `spread(1)=8-(-2)=10`, `spread(2)=8-(-1)=9`, `spread(3)=2-(-2)=4`, `spread(4)=8-8=0`

**Output:**
```
10
9
4
0
```
✅

---

## ⏱ Complexity

| Metric | Complexity | Why |
|---|---|---|
| Time | O(N + Q) | One BFS pass builds pathScore/parent, one reverse pass aggregates min/max, queries are O(1) lookups |
| Space | O(N) | Adjacency list, plus `score`, `par`, `lo`, `hi` arrays sized to N |

---

## 💡 Lesson Learned

"Process children before parents" is a recurring pattern for subtree aggregation problems — BFS order guarantees parents come before children, so simply **reversing** that order gives a valid children-before-parents processing sequence, without needing a separate DFS post-order pass. This is a cheap trick worth remembering: BFS order reversed = a valid bottom-up order for trees. Also, a good debugging reminder from this problem: when a loop's output looks scrambled or repeats one value oddly, check every array index inside the same expression for a mismatched loop variable — a single stray literal (`data[idx+1]` instead of `data[idx+i]`) can silently break only *part* of an otherwise-correct expression, since Python won't flag it as an error.
