

print("WEllcome TO OUR CAFE :")

while True :
    print("Select item :")

    items_name = {
        1 : "Milk Tea",
        2 : "Black Tea",
        3 : "Coffee",
        4 : "lattee coffee",
        5 : "Green Tea"
    }

    for i , j in items_name.items() :
        print(i,j)

    select_items = input("Select the items : (1, 5)  :")
    if select_items == "1":
        print("You Selected Milk tea :")
    elif select_items == "2":
        print("You Selected Black Tea :")
    elif select_items == "3":
        print("You Selected Coffee :") 
    elif select_items == "4":
        print("You Selected Green Tea :") 
    elif select_items == "5":
        print("Invalid Selction : Please Try again :")

    add_more_items = input("If You want to add more items");
    if add_more_items == "yes":
        print(select_items)
    elif add_more_items == "no":
        print("Thank You :")
        break
    else:
        print("Inavalid Option . Please selct a valid option :")

