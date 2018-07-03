import math 
from multiprocessing import Pool

def forth_cal(x):
    list = [] 
    while x > 3: 
        list.append(str(x % 4)) 
        x = x // 4
    if x: 
        list.append(str(x)) 
    x = ''.join(reversed(list)) 
    while 1:
        if len(x) < 10:
            x = '0'+x
        else:
            break
    return x


def answer(x):
    min_S = min('0123',key=x.count)
    max_S = max('0123',key=x.count)
    n = []
    for i in x:
        n.append(int(i))

    select_2 = '2301'
    if select_2[n[1]] != x[4]:
        return 0
    
    select_3 = '2513'
    tmp = select_3.replace(select_3[n[2]],'')
    if x[int(select_3[n[2]])] in [x[int(i)] for i in tmp]:
        return 0
    
    select_4 = [(0,4),(1,6),(0,8),(5,9)]
    tmp = select_4[n[3]]
    if x[tmp[0]] != x[tmp[1]]:
        return 0

    select_5 = '7386'
    if x[int(select_5[n[4]])] != x[4]:
        return 0

    select_6 = [(1,3),(0,5),(2,9),(4,8)]
    tmp = select_6[n[5]]
    if x[tmp[0]] != x[7] or x[tmp[1]] != x[7]:
        return 0
    
    select_7 = '2103'
    if select_7[n[6]] != min_S:
        return 0

    select_8 = '6419'
    if abs(int(select_8[n[7]]) - int(x[0])) == 1:
        return 0

    select_9 = '5918'
    tmp = x[int(select_9[n[8]])] == x[4]
    if (x[0] == x[5]) == tmp:
        return 0

    select_10 = '3241'
    if (x.count(max_S) - x.count(min_S)) != int(select_10[n[9]]):
        return 0

    return 1

def run(x):
    x = forth_cal(x)
    if answer(x) == 1:
        x = x.replace('0','A')
        x = x.replace('1','B')
        x = x.replace('2','C')
        x = x.replace('3','D')
        print(x)
        exit()


range_list = range(int(math.pow(4,10)))
Pool().map(run,range_list)
