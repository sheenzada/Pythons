
with open ('index.html' , 'r') as webpage:
    with open ('outputs.txt' , 'a') as wf:
        for line in webpage.readlines():
            if '<a href =' in line:
                pos = line.find('<a href =')
                first_qoute = line.find('\"' , pos)
                second_qoute  = line.find('\"' , first_qoute+1)
                url =line [first_qoute+1:second_qoute]
                wf.write(url,'\n')  
