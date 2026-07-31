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
            
            # Since p, q <= 10^9 and MOD = 10^9 + 7, p, q < MOD holds.
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
