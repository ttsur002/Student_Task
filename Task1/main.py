#!/usr/bin/python3


from datetime import datetime


class Dummy:
    def __init__(self, bias, baseline):
        self.__bias = bias
        self.__baseline = baseline / 3

    @property
    def bias(self):
        return self.__bias

    @property
    def baseline(self):
        return self.__baseline

    @baseline.setter
    def baseline(self, new_baseline):
        self.__baseline = new_baseline

    def multiplier(self, multiplier):
        result = self.__baseline * multiplier + self.__bias
        return round(result, 2)

    def date_time(self):
        current_time = datetime.now()
        return current_time.strftime('%H:%M:%S %d/%m/%y')


#def main():
#    dummy = Dummy(3, 4.2)
#    print(dummy.bias)
#    print(dummy.baseline)
#    dummy.baseline=6.5
#    print(dummy.baseline)
#   print(dummy.multiplier(4))
#    print(dummy.date_time())


#if __name__ == '__main__':
#    main()
