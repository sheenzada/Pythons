class Car:
    @staticmethod
    def start():
        print('Car Started..')

    @staticmethod
    def stop():
        print('Car Stoped..')
class ToyotaCar(Car):
    def __init__(self, brand):
        self.brand = brand

class Fortuner(ToyotaCar):
    def __init__(self, type):
        self.type = (type)
car1 = Fortuner('diesel')
car1.start()