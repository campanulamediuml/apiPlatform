import time

time_stamp = time.localtime()
time_struct = []
for i in time_stamp[:6]:
    time_struct.append(str(i))

for i in time_struct:
    if len(i) == 1:
        time_struct[time_struct.index(i)] = '0'+i

result = '-'.join(time_struct[:3])+' '+':'.join(time_struct[3:])
print(result)