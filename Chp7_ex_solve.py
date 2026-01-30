def divide (a,b):
    try:
     return a/b
    except ZeroDivisionError as err:
    #  print("'You Can't divide a number by zero")
     print(err)
    except TypeError as err:
    #   print(err)
     print("numbers must be int or floats")
    except:
      print("Unexcepted error")
print(divide(10,'2'))