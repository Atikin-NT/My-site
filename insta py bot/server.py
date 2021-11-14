n, m = map(int, input().split())
def_dict = {a:[] for a in range(1, n+1)}
for _ in range(m):
    u, v = map(int, input().split())
    def_dict[u].append(v)
    def_dict[v].append(u)
#print(dict)
dictr = def_dict.copy()
print(def_dict)

def F(x):
    arrDelKey = []
    for key in x:
        tmp = x[key]
        flag = 0
        if len(tmp) > 0:
            for i in tmp:
                if i <= key: 
                    flag = 1
                    break
            if flag == 0: arrDelKey.append(key)
    print(len(x), def_dict)
    if len(arrDelKey) == 0: return int(len(x))
    for key in arrDelKey: 
        del x[key]
        for i in x:
            if key in x[i]: x[i].remove(key)
    return F(x)



q = int(input())
for _ in range(q):
    command = str(input())
    if command == "3":
        tmp = def_dict.copy()
        print('rez =', F(tmp))
        print(def_dict, tmp, dictr)
    else:
        a, u, v = map(int, input().split())
        if a == 1:
            def_dict[u].append(v)
            def_dict[v].append(u)
        else:
            def_dict[u].append(v)
            def_dict[v].append(u)