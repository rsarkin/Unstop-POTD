# Day 26: Interdimensional Trade Routes (All-Pairs Shortest Path — Floyd-Warshall)

## 📋 Problem Statement

The Interdimensional Trade Council maintains a network of `N` worlds connected by `M` bidirectional gateways, each with an Energy Tax cost. Given `Q` audit requests, each asking for the minimum Energy Tax to transport cargo between two worlds, report the minimum cost for each request, or `-1` if no route exists.

**Input Format:**
- First line: `N M Q`
- Next `M` lines: `U V W` — a bidirectional gateway between worlds `U` and `V` with tax `W`
- Next `Q` lines: `A B` — an audit request for the minimum tax between worlds `A` and `B`

**Output Format:** For each audit request, print the minimum energy tax, or `-1` if transportation is impossible

**Constraints:**
- `2 ≤ N ≤ 400`
- `1 ≤ M ≤ N(N−1)/2`
- `1 ≤ Q ≤ 100000`
- `1 ≤ W ≤ 10^9`

**Example:** With gateways `1-2(5), 1-3(12), 2-3(3), 2-4(4), 3-4(7)`, query `(1,3)` costs `8` via `1→2→3` (cheaper than the direct edge `12`).

---

## 🔍 Identifying the Problem

Strip away the interdimensional framing and this is a classic **All-Pairs Shortest Path** problem. The key signal is the combination of a small `N ≤ 400` with a large number of queries `Q ≤ 100000` on arbitrary world pairs — running Dijkstra separately for each of up to 100000 queries would be wasteful and slow. Instead, precomputing shortest distances between **every pair of worlds upfront** turns each query into an O(1) lookup. With `N ≤ 400`, this points directly to **Floyd-Warshall**, whose `O(N³)` complexity (~64 million operations) comfortably fits within time limits.

---

## 🧠 Steps of Execution

### Step 1 — Read the input
Read `N`, `M`, `Q`, then the `M` gateway edges and `Q` queries.

### Step 2 — Initialize the distance matrix
Build an `(N+1) × (N+1)` matrix filled with infinity, with `dist[i][i] = 0` for every world. For each gateway, set `dist[u][v] = dist[v][u]` to the minimum of the existing value and the new edge weight (handles possible duplicate edges).

### Step 3 — Run Floyd-Warshall
For every intermediate world `k`, for every pair `(i, j)`, relax `dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])` — this considers routing through `k` as a potential shortcut.

### Step 4 — Skip unreachable intermediates early
If `dist[i][k]` is still infinity, skip the entire inner loop for that `(k, i)` pair — critical for performance when the graph is sparse, since otherwise the loop still burns `O(N)` iterations doing useless infinity arithmetic for every unreachable pair.

### Step 5 — Answer queries
For each query `(A, B)`, print `dist[A][B]` if it's finite, otherwise print `-1`.

---

## 💻 Final Code

```python
import sys

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    m = int(data[idx]); idx += 1
    q = int(data[idx]); idx += 1

    INF = float('inf')
    dist = [[INF] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        dist[i][i] = 0

    for _ in range(m):
        u = int(data[idx]); idx += 1
        v = int(data[idx]); idx += 1
        w = int(data[idx]); idx += 1
        if w < dist[u][v]:
            dist[u][v] = w
            dist[v][u] = w

    for k in range(1, n + 1):
        for i in range(1, n + 1):
            if dist[i][k] == INF:            # skip early — nothing reachable through k from i
                continue
            for j in range(1, n + 1):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

    out = []
    for _ in range(q):
        a = int(data[idx]); idx += 1
        b = int(data[idx]); idx += 1
        d = dist[a][b]
        out.append(str(d) if d != INF else "-1")

    sys.stdout.write('\n'.join(out) + '\n')

if __name__ == "__main__":
    main()
```

---

## 🔬 Dry Run — Testcase 1

Input: `4 5 3 / 1 2 5 / 1 3 12 / 2 3 3 / 2 4 4 / 3 4 7 / 1 3 / 1 4 / 3 4`

Initial direct distances: `dist[1][2]=5, dist[1][3]=12, dist[2][3]=3, dist[2][4]=4, dist[3][4]=7`

After Floyd-Warshall:
- `dist[1][3]`: via `k=2` → `5+3=8` beats direct `12` → updated to `8`
- `dist[1][4]`: via `k=2` → `5+4=9` beats infinity → updated to `9`
- `dist[3][4]`: direct edge `7` remains the shortest

Query `(1,3)` → `8`, Query `(1,4)` → `9`, Query `(3,4)` → `7`

**Output:**
```
8
9
7
```
✅

---

## ⏱ Complexity

| Metric | Complexity | Why |
|---|---|---|
| Time | O(N³) | Floyd-Warshall's triple nested loop over all intermediate/source/destination worlds |
| Space | O(N²) | The full `N × N` distance matrix storing shortest paths between every pair |

---

## 💡 Lesson Learned

When a problem has a small `N` but a very large number of arbitrary-pair queries, precomputing all-pairs shortest paths once (Floyd-Warshall) beats running single-source shortest path algorithms repeatedly, turning each query into an O(1) lookup. Also, a valuable performance lesson from the timeout: on sparse graphs, skipping the innermost loop early whenever the intermediate distance is infinity isn't just a micro-optimization — for M=0 or very sparse graphs, it's the difference between finishing instantly and grinding through 64 million wasted iterations of infinity arithmetic on every test case.
