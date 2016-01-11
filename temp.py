def moving_window(iterable):
    start, stop = 0, 1
    while stop < len(iterable):
        print(iterable[start], iterable[stop])
        start += 1
        stop += 1


iterable = [0, 1, 2, 3, 4, 5]
print(iterable[1:])
