bin = "00100101"
i = 0
d = []
for b in bin:
    if b is '1':
        d.append(i)
    i += 1
print(d)