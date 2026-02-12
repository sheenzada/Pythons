
task_list = {
    1 : 'Add Task',
    2 : 'Remove Task',
    3 : 'Show Task',
    4 : 'Exit'
}

for i ,j in task_list.items():
    print(i , j)
task = []

while True :
    user_choice = int(input("Enter Your Choice (1, 4) :"))
    if user_choice == 1 :
        adding = input("Add the Task :")
        task.append(adding)
    elif user_choice == 2:
        removing = input("Remove the Task :")
        task.remove(removing)
    elif user_choice == 3:
        print(task)
    elif user_choice == 4:
        break
else:
    print('inavalid input try again !')