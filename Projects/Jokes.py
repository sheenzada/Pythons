
# pip install pyjokes

import jokes as pj

print("="*30)
print("Python Jokes Generator")
print("="*30)

while True:
    print(pj.get_joke())
    input("Press Enter To Continue..")
    print("-"*30)

