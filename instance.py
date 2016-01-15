from vehicle import Truck, Preseller
from customer import Customer
from math import sqrt
import matplotlib.pyplot as plt
from random import choice
from copy import copy

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
        self.type = type
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

    def add_truck(self, id, D, Q):
        self.trucks.append(Truck(id, D, Q, self.t))

    def add_preseller(self, id, D, Q):
        self.presellers.append(Preseller(id, D, Q, self.t))

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
            st += c.type + '\t'
            for a in c.attributes:
                st += repr(a) + '\t'
            st += '\n'
        return st

    def compute_distances(self):
        for i in self.customers:
            for j in self.customers:
                dist = euclidean(i, j)
                i.dist[j.i] = dist
                j.dist[i.i] = dist

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
        unsatisfied = copy(self.customers)
        satisfied = []
        partially_satisfied = []
        self.sort_customers()
        for i in self.customers:                            # iterate on customers
            if i.type is not 'depot':
                random_assignment = self.pick_random_assignment(i.list)  # pick random assignment from the customer's list
                satisfied_days = 0
                for day in random_assignment:                            # for each day (1 in the binary representation
                    limit = 0                                            # of the possible schedule),
                    appended = self.random_truck().append_to_schedule(day, i, self)
                    while not appended and limit < 100:
                        appended = self.random_truck().append_to_schedule(day, i, self)
                        limit += 1
                    if limit < 100:
                        satisfied_days += 1
                if satisfied_days != 0:
                    unsatisfied.remove(i)
                    if satisfied_days == len(random_assignment):
                        satisfied.append(i)
                    else:
                        partially_satisfied.append(i)
            else:
                unsatisfied.remove(i)

        print('{:3d}: T({:5d}:{:5d}:{:5d})'.format(self.id, len(unsatisfied), len(partially_satisfied), len(satisfied)), end="", flush=True)

        unsatisfied = copy(self.customers)
        satisfied = []
        partially_satisfied = []
        for i in self.customers:                            # iterate on customers
            if i.type is not 'depot':
                random_assignment = self.pick_random_assignment(i.list)  # pick random assignment from the customer's list
                satisfied_days = 0
                for day in random_assignment:                            # for each day (1 in the binary representation
                    limit = 0                                            # of the possible schedule),
                    appended = self.random_preseller().append_to_schedule(day, i, self)
                    while not appended and limit < 100:
                        appended = self.random_preseller().append_to_schedule(day, i, self)
                        limit += 1
                    if limit < 100:
                        satisfied_days += 1
                if satisfied_days != 0:
                    unsatisfied.remove(i)
                    if satisfied_days == len(random_assignment):
                        satisfied.append(i)
                    else:
                        partially_satisfied.append(i)
            else:
                unsatisfied.remove(i)
        print(' P({:5d}:{:5d}:{:5d})'.format(len(unsatisfied), len(partially_satisfied), len(satisfied)))
        # for t in self.trucks:
        #      t.print_schedule()

    def to_file(self):
            st = repr(self.type) + ' ' + repr(self.m) + ' ' + repr(self.n) + ' ' + repr(self.t) + '\n'
            for t in self.trucks:
                st += repr(t.D) + ' ' + repr(t.Q) + '\n'
            for p in self.presellers:
                st += repr(p.D) + ' ' + repr(p.Q) + '\n'
            for c in self.customers:
                st += '{:3d} {} {} {:.2f} {:.2f} {:.2f} {:d} '.format(c.i, c.x, c.y, c.d, c.q, c.f, int(c.a))
                if c.type is not 'depot':
                    for l in c.list:
                        st += repr(l) + ' '
                    if c.e is not None:
                        st += repr(c.e) + ' '
                    if c.l is not None:
                        st += repr(c.l)
                st += '\n'
            return st

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





