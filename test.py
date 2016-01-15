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
    with open('.\modified_instances\instance' + repr(i) + '.txt') as file:   # open the text file with name 'file'
        lines = file.readlines()                                    # read all lines
        type, m, n, t = [int(x) for x in lines[0].split()]          # the header of the file
        instance = Instance(i, type, m, n, t)                       # an instance is created by parameters of header
        for j in range(1, t+1):                                       # for the next t lines
            D, Q = [int(y) for y in lines[j].split()]               # read D Q values from text file
            instance.add_truck(j, D, Q)                           # the vehicle read from the file is added
        for j in range(t+1, 2*t+1):                                       # for the next t lines
            D, Q = [int(y) for y in lines[j].split()]               # read D Q values from text file
            instance.add_preseller(j, D, Q)
        instance.add_depot(float(y) for y in lines[2*t+1].split())    # add depot to the instance
        for j in range(2*t+2, len(lines)):                            # iterate on the actual customers
            info = [float(y) for y in lines[j].split()]             # read i x y d q f a list e l values from text file
            instance.add_customer(parse_info(info))                 # add a customer to the instance
        instances.append(instance)                                  # the instance is appended to instances list
        instance.compute_distances()

for i in instances:
    i.find_initial_solution()
# for i in range(1, 43):                                              # for i = 1; i < 43; i++
#     with open('.\instances\instance' + repr(i) + '.txt') as file:   # open the text file with name 'file'
#         lines = file.readlines()                                    # read all lines
#         type, m, n, t = [int(x) for x in lines[0].split()]          # the header of the file
#         instance = Instance(i, type, m, n, t)                       # an instance is created by parameters of header
#         for j in range(1, t+1):                                       # for the next t lines
#             D, Q = [int(y) for y in lines[j].split()]               # read D Q values from text file
#             instance.add_vehicle(j, D, Q)                           # the vehicle read from the file is added
#         instance.add_depot(float(y) for y in lines[t+1].split())    # add depot to the instance
#         for j in range(t+2, len(lines)):                            # iterate on the actual customers
#             info = [float(y) for y in lines[j].split()]             # read i x y d q f a list e l values from text file
#             instance.add_customer(parse_info(info))                 # add a customer to the instance
#         instances.append(instance)                                  # the instance is appended to instances list
#         instance.compute_distances()

# for instance in instances:
#     print('modifying instance', instance.id)
#     sum = 0.0
#     for i in instance.customers:
#         if i.type is not 'depot':
#             sum += float(i.q*i.f + i.distance_to_10th_nearest())
#         else:
#             sum += float(instance.m * i.distance_to_10th_nearest())
#     result = float(sum)/float(instance.t*instance.m)
#     for p in instance.presellers:
#         p.D = int(result)
#         p.Q = 0

# for i in range(42):
#     |[i].find_initial_solution()
# The instances are read from the files #


