class Vehicle:

    def __init__(self, id, D, Q, t):
        self.id = id
        self.D = D
        self.Q = Q
        self.load = {}
        self.time = {}
        self.score = 0
        self.schedule = {}
        self.last_visited = None
        self.turning_back = 0
        for i in range(t):
            self.schedule[i] = []
            self.load[i] = 0
            self.time[i] = 0

    def __repr__(self):
        st = '(' + repr(self.D) + ',' + repr(self.Q) + ')'
        return st

    def append_depot(self, day, depot):
        self.schedule[day].append(0)
        self.schedule[day].append(0)
        self.last_visited = depot

    def append_to_schedule(self, day, customer):
        self.schedule[day].insert(-1, customer.i)
        self.load[day] += customer.q
        self.time[day] += customer.dist[self.last_visited]
        self.time[day] -= self.turning_back
        self.time[day] += customer.dist[0]
        self.turning_back = customer.dist[0]
        self.last_visited = customer

    def insert_into_schedule_after(self, customer, index):
        self.schedule.index(customer, index)

    def print_schedule(self):
       pass


class Truck(Vehicle):
    def print_schedule(self):
        print('Truck', self.id, ':')
        for d, s in self.schedule.items():
            print("Day {0}: {1}\t\tLoad: {2:.2f}\t\t Time: {3:.2f}".format(d, s, self.load[d], self.time[d]),
                  end="", flush=True)
            if self.load[d] > self.Q:
                print(' Overloaded!', end="", flush=True)
            print('\n')


class Preseller(Vehicle):
    def print_schedule(self):
        print('Preseller', self.id, ':')
        for d, s in self.schedule.items():
            print('Day', d, ': ', s)