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
