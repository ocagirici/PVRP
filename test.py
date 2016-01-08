from instance import Instance


def parse_info(st):
    i, x, y, d, q, f, a = st[0:7]
    list = st[7:int(8 + a)]
    if len(st) > 8+a:
        e = st[8 + a]
        l = st[9 + a]
        return [i, x, y, d, q, f, a, list, e, l]
    return [i, x, y, d, q, f, a, list]


type = 0
m = 0
n = 0
t = 0
instances = []

# Begin reading from the files #

for i in range(1, 43):                                              # for i = 1; i < 43; i++
    with open('.\instances\instance' + repr(i) + '.txt') as file:   # open the text file with name 'file'
        lines = file.readlines()                                    # read all lines
        type, m, n, t = [int(x) for x in lines[0].split()]          # the header of the file
        instance = Instance(i, type, m, n, t)                       # an instance is created by parameters of header
        for j in range(t):                                          # for the next t lines
            D, Q = [int(y) for y in lines[1 + j].split()]           # read D Q values from text file
            instance.add_vehicle(j, D, Q)                           # the vehicle read from the file is added
        instance.add_depot(float(y) for y in lines[t+1].split())    # add depot to the instance
        for j in range(t+2, len(lines)):                            # iterate on the actual customers
            info = [float(y) for y in lines[j].split()]             # read i x y d q f a list e l values from text file
            instance.add_customer(parse_info(info))                 # add a customer to the instance
        instances.append(instance)                                  # the instance is appended to instances list

instances[1].find_initial_solution()
# The instances are read from the files #


