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
        # Alternating sorting for Mo's Algorithm (hilbert curve or simple alternating R)
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
