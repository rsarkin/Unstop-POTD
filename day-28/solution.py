import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    
    n = int(data[0])
    result = 0
    for i in range(1, n + 1):
        result ^= int(data[i])
    
    print(result)

if __name__ == "__main__":
    main()
