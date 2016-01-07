from vehicle import Truck
from vehicle import Preseller
from customer import Customer
from math import sqrt
import matplotlib.pyplot as plt
from random import choice

def numbers_to_strings(argument):
    switcher = {
        0: 'VRP',
        1: 'PVRP',
        2: 'MDVRP',
        3: 'SDVRP',
        4: 'VRPTW',
        5: 'PVRPTW',
        6: 'MDVRPTW',
        7: 'SDVRPTW'
    }
    return switcher.get(argument, "nothing")


class Instance:

    def __init__(self, id, type, m, n, t):
        self.id = id
        self.type = numbers_to_strings(type)
        self.m = m
        self.n = n
        self.t = t
        self.trucks = []
        self.presellers = []
        self.customers = []                         # initialize customers as empty list
        self.size = 0

    def add_vehicle(self, D, Q):
        self.trucks.append(Truck(D, Q))
        self.presellers.append(Preseller(D, Q))

    def add_customer(self, info):
        self.customers.append(Customer(info, 'customer'))
        self.size += 1

    def add_depot(self, info):
        self.customers.append(Customer(info, 'depot'))
        self.size += 1

    def __repr__(self):
        st = 'id: ' + repr(self.id) + '\n'
        st += 'type: ' + repr(self.type) + '\n'
        st += 'vehicles: '
        for v in self.trucks:
            st += repr(v) + ','
        st = st[:-1]
        st += 'customers:\n'
        for c in self.customers:
            st += repr(c)
        return st

    def euclidean(self, i, j):
        return sqrt((self.customers[i].x - self.customers[j].x)**2 + (self.customers[i].y - self.customers[j].y)**2)

    def sort_customers(self):
        self.customers.sort(key=lambda x: x.d + x.q, reverse=True)

    def pick_random_assignment(self, list):
        r = choice(list)
        bin = "{0:0{1}b}".format(r, self.t)
        i = 0
        d = []
        for b in bin:
            if b is '1':
                d.append(int(b))
        return d

    def random_truck(self):
        return choice(self.trucks)

    def find_initial_solution(self):
        for i in range(self.t):                             # iterate on number of days
            self.trucks[i].schedule.append([0])             # append depot to the trucks' schedule
            self.presellers[i].schedule.append([0])         # append depot to the presellers' schedule
        self.sort_customers()                               # sort customers w.r.t (d + q) values
        for i in self.customers:
            random_assignment = self.pick_random_assignment(i.list)
            for day in random_assignment:
               self.random_truck().append_to_schedule(day, i)






    def plot(self):
        dx = self.customers[0].x
        dy = self.customers[0].y
        x = []
        y = []
        for i in self.customers[1:]:
            x.append(i.x)
            y.append(i.y)
        plt.scatter(dx, dy, s=80, marker="s")
        plt.scatter(x, y)
        plt.show()



