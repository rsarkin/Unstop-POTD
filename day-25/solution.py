import sys

def main():
    # Read all input from standard input
    data = sys.stdin.read().split()
    if not data:
        return
    
    s = data[0]
    
    # Check if the string is equal to its reverse
    if s == s[::-1]:
        print("YES")
    else:
        print("NO")

if __name__ == "__main__":
    main()
