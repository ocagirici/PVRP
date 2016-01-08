class Customer:
    def __init__(self, info, type):
        self.type = type
        self.dist = {}
        if self.type is 'customer':
            if len(info) is 10:
                self.i, self.x, self.y, self.d, self.q, self.f, self.a, self.list, self.e, self.l = info
            if len(info) is 8:
                self.e, self.l = [None, None]
                self.i, self.x, self.y, self.d, self.q, self.f, self.a, self.list = info
            for l in self.list:
                l = int(round(l))
            self.i = int(round(self.i))
        elif self.type is 'depot':
            self.i, self.x, self.y, self.d, self.q, self.f, self.a = info

    def __repr__(self):
        if self.type is 'customer':
            if self.e and self.l:
                return "{:d}:  ({:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:d}, {}, {:d}, {:d}\n".format(
                    int(self.i), self.x, self.y, self.d, self.q, self.f, int(self.a), self.list, int(self.e),
                    int(self.l))
            else:
                return "{:d}:  ({:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:d}, {}\n".format(
                    int(self.i), self.x, self.y, self.d, self.q, self.f, int(self.a), self.list)
        elif self.type is 'depot':
            return "({:.2f}, {:.2f})".format(self.x, self.y)
