from math import inf,sqrt

def euclidean(i, j):
    return sqrt((i.x - j.x)**2 + (i.y - j.y)**2)

class Vehicle:
    def __init__(self, id, D, Q, t):
        self.id = id
        self.D = D
        self.Q = Q
        self.load = {}
        self.time = {}
        self.score = 0
        self.schedule = {}
        self.schedule_dist = {}
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
        self.schedule_dist[(0, 0)]= 0
        self.last_visited = depot

    def insert_into_schedule_after(self, customer, index):
        self.schedule.index(customer, index)

    def print_schedule(self):
        pass


class Truck(Vehicle):
    def find_minimum_cost(self, day, customer):
        i, j = 0, 1
        min = i
        dist = inf
        while j < len(self.schedule[day]):
            dist = customer.dist[self.schedule[day][min]] + customer.dist[self.schedule[day][min + 1]]
            if customer.dist[self.schedule[day][i]] + customer.dist[self.schedule[day][j]] < dist:
                min = i
                print('min', min)
            i += 1
            j += 1
        return min, dist

    def append_to_schedule(self, day, customer, instance):
        if customer.i in self.schedule[day]:
            return True
        if self.load[day] + customer.q > self.Q:
            return False
        min, dist = self.find_minimum_cost(day, customer)
        self.schedule[day].insert((min+1), customer.i)
        print(self.id, ',', day, ':', self.schedule[day])
        # self.schedule[day].insert(-1, customer.i)
        self.load[day] += customer.q
        print('time:', self.time[day])
        self.time[day] += dist
        print('time:', self.time[day])
        print(
                'insert:', self.schedule[day][min+1], \
                'dist(', self.schedule[day][min], ',', self.schedule[day][min+2], ')=', \
                instance.customers[self.schedule[day][min]].dist[self.schedule[day][min+2]],\
                euclidean(instance.customers[self.schedule[day][min]],
                          instance.customers[self.schedule[day][min+2]]
                          ))
        print('customers:', instance.customers[self.schedule[day][min]], instance.customers[self.schedule[day][min+2]])
        self.time[day] -= instance.customers[self.schedule[day][min]].dist[self.schedule[day][min+2]]
        print('time:', self.time[day])
        # self.time[day] -= self.turning_back
        # self.time[day] += customer.dist[0]
        # self.turning_back = customer.dist[0]
        # self.last_visited = customer
        return True

    def print_schedule(self):
        print('Truck', self.id, ':')
        for d, s in self.schedule.items():
            print("Day {0}: {1}\t\tLoad: {2:.2f}\t\t Time: {3:.2f}".format(d, s, self.load[d], self.time[d]),
                  end="", flush=True)
            if self.load[d] > self.Q:
                print(' Overloaded!', end="", flush=True)
            print('\n')


class Preseller(Vehicle):
    def append_to_schedule(self, day, customer):
        if customer.i in self.schedule[day]:
            return True
        if self.time[day] + customer.d + customer.dist[self.last_visited] + customer.dist[0] > self.D:
            return False

        self.schedule[day].insert(-1, customer.i)
        self.time[day] += customer.dist[self.last_visited]
        self.time[day] -= self.turning_back
        self.time[day] += customer.dist[0]
        self.turning_back = customer.dist[0]
        self.last_visited = customer
        return True

    def print_schedule(self):
        print('Preseller', self.id, ':')
        for d, s in self.schedule.items():
            print("Day {0}: {1}\t\tLoad: {2:.2f}\t\t Time: {3:.2f}".format(d, s, self.load[d], self.time[d]),
                  end="", flush=True)
            if self.time[d] > self.D:
                print(' Overloaded!', end="", flush=True)
            print('\n')
