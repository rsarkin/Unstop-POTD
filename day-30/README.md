# Day 30: Currency Exchange Consistency (Weighted Union-Find / Weighted DSU)

## 📋 Problem Statement

A confederation of `N` islands each mint their own currency, and pairs of islands negotiate direct exchange-rate agreements over time. All arithmetic is performed modulo `P = 1,000,000,007`, with ratios represented as `a·b⁻¹ mod P`. Process `M` events:
- `1 u v p q` — declare that 1 unit of currency `u` equals `p/q` units of currency `v`. If `u` and `v` are already connected, check consistency against the implied rate (`OK` or `CONTRADICTION`); otherwise merge and print `OK`.
- `2 u v` — query the implied rate from `u` to `v`, or `UNKNOWN` if not connected. If `u = v`, the answer is always `1`.

**Input Format:**
- `N`, `M`
- `M` events, each either `1 u v p q` or `2 u v`

**Output Format:** For each event, print `OK`/`CONTRADICTION` (type 1) or `UNKNOWN`/the rate mod P (type 2)

**Constraints:**
- `1 ≤ N, M ≤ 2 × 10^5`
- `1 ≤ p, q ≤ 10^9`
- Time Limit: 2 sec, Memory Limit: 256 MB

**Example:** Declaring `1 2 = 2 units of 3` then `2 3 = 3 units of 3`... connects islands transitively with implied rate `2×3=6`; querying `(1,3)` returns `6`, and a later declaration claiming rate `5` between them is rejected as `CONTRADICTION`.

---

## 🔍 Identifying the Problem

Strip away the currency-exchange framing and this is **Weighted Union-Find (Weighted DSU)** — a significant step up from plain "are these connected" DSU, since every union carries a **multiplicative ratio**, not just a link.

**Key insight:** For each node `x`, maintain `weight[x]` = the rate such that `1 unit of x = weight[x] units of parent[x]` (and eventually `root(x)` after path compression). During `find(x)` with path compression, every node's `weight` gets updated to be its rate *directly to the root*, not just to its immediate parent. Comparing or merging two components then becomes modular multiplication/division using these root-relative weights.

---

## 🧠 Steps of Execution

### Step 1 — Initialize DSU
`parent[i] = i`, `weight[i] = 1` for every island — every node starts as its own root with rate 1 to itself.

### Step 2 — `find(x)` with weighted path compression
Walk up from `x` to the root, collecting the chain of visited nodes. Then process the chain **from the node nearest the root down to `x`**, so each node's weight can be multiplied by its already-corrected parent's weight before being attached directly to the root — this ensures weights compose correctly during compression.

### Step 3 — Handle type-1 declarations
Compute the declared rate `r = p · q⁻¹ mod P`. Find the roots of `u` and `v`.
- Same root → compute the implied rate from existing weights and compare to `r` → `OK` or `CONTRADICTION`.
- Different roots → solve for the new root's weight so both components' rates agree, attach one root under the other → `OK`.

### Step 4 — Handle type-2 queries
If `u = v`, answer is `1`. Otherwise find both roots — if different, `UNKNOWN`; if the same, the answer is `weight[u] · weight[v]⁻¹ mod P`.

---

## 💻 Final Code

```python
import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    idx = 0
    MOD = 1000000007
    
    n = int(data[idx]); idx += 1
    m = int(data[idx]); idx += 1
    
    parent = list(range(n + 1))
    weight = [1] * (n + 1)
    
    def find(x):
        if parent[x] == x:
            return x, weight[x]
        chain = []
        cur = x
        while parent[cur] != cur:
            chain.append(cur)
            cur = parent[cur]
        root = cur
        for node in reversed(chain):
            p = parent[node]
            if p != root:
                weight[node] = weight[node] * weight[p] % MOD
            parent[node] = root
        return root, weight[x]
    
    out = []
    for _ in range(m):
        t = data[idx]; idx += 1
        if t == b'1':
            u = int(data[idx]); idx += 1
            v = int(data[idx]); idx += 1
            p = int(data[idx]); idx += 1
            q = int(data[idx]); idx += 1
            
            r = p * pow(q, MOD - 2, MOD) % MOD
            ru, wu = find(u)
            rv, wv = find(v)
            
            if ru == rv:
                if wv == 1:
                    computed = wu
                else:
                    computed = wu * pow(wv, MOD - 2, MOD) % MOD
                out.append("OK" if computed == r else "CONTRADICTION")
            else:
                if wu == 1:
                    new_w = r * wv % MOD
                else:
                    new_w = r * wv % MOD * pow(wu, MOD - 2, MOD) % MOD
                parent[ru] = rv
                weight[ru] = new_w
                out.append("OK")
        else:
            u = int(data[idx]); idx += 1
            v = int(data[idx]); idx += 1
            
            if u == v:
                out.append("1")
            else:
                ru, wu = find(u)
                rv, wv = find(v)
                if ru != rv:
                    out.append("UNKNOWN")
                else:
                    if wv == 1:
                        ans = wu
                    else:
                        ans = wu * pow(wv, MOD - 2, MOD) % MOD
                    out.append(str(ans))
    
    sys.stdout.write('\n'.join(out) + '\n')

if __name__ == "__main__":
    main()
```

---

## 🔬 Dry Run — Testcase 1

Input: `3 4 / 1 1 2 1 5 / 2 1 2 / 2 2 1 / 2 1 3`

- Event `1 1 2 1 5`: `r = 1 · inv(5) = 400000003`. Islands 1, 2 in separate components → merge, `weight[1] = 400000003` → print `OK`
- Event `2 1 2`: same component now. `weight[1]=400000003, weight[2]=1` → `answer = 400000003 · inv(1) = 400000003` → print `400000003`
- Event `2 2 1`: `answer = weight[2] · inv(weight[1]) = 1 · inv(400000003) = 5` → print `5`
- Event `2 1 3`: island 3 untouched, different component → print `UNKNOWN`

**Output:**
```
OK
400000003
5
UNKNOWN
```
✅

---

## ⏱ Complexity

| Metric | Complexity | Why |
|---|---|---|
| Time | O(M α(N) log P) | DSU operations are near-O(1) amortized (α = inverse Ackermann); each also does at most a constant number of `pow(x, MOD-2, MOD)` calls costing O(log P). Since many weights are 1, the `pow` is bypassed in many operations, optimizing execution time. |
| Space | O(N) | `parent` and `weight` arrays sized to N |

---

## 💡 Lesson Learned

Weighted Union-Find extends plain DSU by attaching a multiplicative relationship to every edge. The key challenge lies in the path compression during `find()` — every node's weight must end up expressed relative to the root, which requires processing the path compression chain in root-to-leaf order. We also optimized performance by bypassing modular exponentiation `pow(x, MOD-2, MOD)` when the weight `x == 1`, significantly reducing the overhead of modular inverses for 200,000 queries in standard Python.
