name, char= input("enter comma separated name and character: ").split(",")
print(f"length of your name is {len(name)}")
print(f" caharacter count : {name.strip().lower().count(char.strip().lower())}")# case sensitive
#char.strip().lower()