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
