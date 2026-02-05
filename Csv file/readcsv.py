from csv import reader

with open ('file.csv' ,'r') as f:
    csv_reader = reader(f)
    # print(type(csv_reader))

    # for row in csv_reader:
    #     print(row)
    next(csv_reader)
    for col in csv_reader:
        print(col)