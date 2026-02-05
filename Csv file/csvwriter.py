from csv import writer
with open ('file2.csv' , 'w', newline='' ) as f:
    csv_writer = writer(f)
    # csv_writer.writerow(['name' , 'country'])
    # csv_writer.writerow(['inam' , 'Pakistan'])
    # csv_writer.writerow(['ikram' , 'Turkey'])

    csv_writer.writerows([['name' , 'country'] , ['inam' , 'Pakistan'], ['ikram' , 'America']])