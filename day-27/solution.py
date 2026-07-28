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
