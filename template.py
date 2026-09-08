import sys

if sys.stdin.isatty():
    print("Žádný stdin")
    sys.exit(1)

lines = [x.strip() for x in sys.stdin] 
print(lines)
 
