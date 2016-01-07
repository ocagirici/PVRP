class Vehicle:
    D = 0
    Q = 0
    schedule = []
    capacity = 0
    score = 0

    def __init__(self, D, Q):
        self.D = D
        self.Q = Q

    def __repr__(self):
        st = '(' + repr(self.D) + ',' + repr(self.Q) + ')'
        return st

    def append_to_schedule(self, day, customer):
       self. schedule[day].append(customer)

    def insert_into_schedule_after(self, customer, index):
        self.schedule.index(customer, index)

class Truck(Vehicle):

    def __init__(self, D, Q):
        self.__D = D
        self.__Q = Q


class Preseller(Vehicle):

    def __init__(self, D, Q):           # The parameters are assigned in reversed order since the load of a truck is
                                        # equivalent to the time constraint of a preseller.
        self.__D = Q
        self.__Q = D

