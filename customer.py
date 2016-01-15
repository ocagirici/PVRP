from collections import OrderedDict
class Customer:
    def __init__(self, info, type):
        self.type = type
        self.dist = dict()
        if self.type is 'customer':
            if len(info) is 10:
                self.i, self.x, self.y, self.d, self.q, self.f, self.a, self.list, self.e, self.l = info
                self.attributes = [self.x, self.y, self.d, self.q, self.f, self.a, self.list, self.e, self.l]
            if len(info) is 8:
                self.e, self.l = [None, None]
                self.i, self.x, self.y, self.d, self.q, self.f, self.a, self.list = info
                self.attributes = [self.x, self.y, self.d, self.q, self.f, self.a, self.list]
            for i in range(len(self.list)):
                self.list[i] = int(self.list[i])
            self.i = int(round(self.i))
        elif self.type is 'depot':
            self.i, self.x, self.y, self.d, self.q, self.f, self.a = info
            self.i = int(round(self.i))
            self.attributes = [self.x, self.y, self.d, self.q, self.f, self.a]

    def __repr__(self):
        return repr(self.i)

    def distance_to_10th_nearest(self):
        return list(OrderedDict(sorted(self.dist.items(), key=lambda t: t[1])))[9]




