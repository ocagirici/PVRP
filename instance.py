from vehicle import Truck, Preseller
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


def euclidean(i, j):
    return sqrt((i.x - j.x)**2 + (i.y - j.y)**2)

class Instance:

    def __init__(self, id, type, m, n, t):
        self.id = id
        self.type = numbers_to_strings(type)
        self.m = m
        self.n = n
        self.t = t
        self.trucks = []
        self.presellers = []
        self.customers = []                      # initialize customers as empty list
        self.size = 0

    def add_vehicle(self, id, D, Q):
        self.trucks.append(Truck(id, D, Q, self.t))
        self.presellers.append(Preseller(id, Q, D, self.t))

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

    def sort_customers(self):
        self.customers.sort(key=lambda x: x.d + x.q, reverse=True)

    def sort_trucks(self, day):
        self.trucks.sort(key=lambda x: x.load[day], reverse=True)

    def sort_presellers(self, day):
        self.presellers.sort(key=lambda x: x.time[day], reverse=True)

    def pick_random_assignment(self, list):
        r = choice(list)
        bin = '{0:0{1}b}'.format(int(r), int(self.t))
        i = 0
        d = []
        for b in bin:
            if b is '1':
                d.append(int(i))
            i += 1
        list.remove(r)
        return d

    def random_truck(self):
        return choice(self.trucks)

    def random_preseller(self):
        return choice(self.presellers)

    def find_initial_solution(self):
        for i in range(self.t):
            for j in self.trucks:
                j.append_depot(i, self.customers[0])
            for j in self.presellers:
                j.append_depot(i, self.customers[0])
        for i in self.customers:
            for j in self.customers:
                dist = euclidean(i, j)
                i.dist[j.i] = dist
                j.dist[i.i] = dist
                                  # sort customers w.r.t (d + q) values
        for i in self.customers:                            # iterate on customers
            if i.type is not 'depot':
                random_assignment = self.pick_random_assignment(i.list)  # pick random assignment from the customer's list
                for day in random_assignment:                            # for each day (1 in the binary representation
                    limit = 0                                            # of the possible schedule),
                    while not self.random_truck().append_to_schedule(day, i, self) and (limit < 100): #  if the load limit is exceeded
                         limit += 1

                    # limit = 0
                    # while (not self.random_preseller().append_to_schedule(day, i)) and (limit < 100): #  if the time limit is exceeded
                    #     self.random_preseller().append_to_schedule(day, i)
                    #     limit += 1
        for t in self.trucks:
            t.print_schedule()
            for d, s in t.schedule.items():
                print('Day', d, 'cost:', t.load[d], 'time:', t.time[d])
                sum = 0
                for c in range(len(s)-1):
                    sum += self.customers[s[c]].dist[s[c+1]]
                print('sum:', sum)

        for p in self.presellers:
            p.print_schedule()

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





