from csv import DictWriter
with open ('final.csv' , 'w') as f:
    csv_writer = DictWriter(f,fieldnames=['firstname','lastname','age'])
    csv_writer.writeheader()

    # csv_writer.writerow({
    #     'firstname' : 'Inam',
    #     'lastname' : 'Ullah',
    #     'age' : 18
    # })
    # csv_writer.writerow({
    #     'firstname' : 'Tajwar',
    #     'lastname' : 'Shaheen',
    #     'age' : 20
    # })

    csv_writer.writerows([
        {'firstname' : 'Inam' , 'lastname' : 'Ullah' , 'age' : '18'},
        {'firstname' : 'Tajwar' , 'lastname' : 'Shaheen' , 'age' : '20'},
        {'firstname' : 'Yaseen' , 'lastname' : 'Malik' , 'age' : '21'},
    ])