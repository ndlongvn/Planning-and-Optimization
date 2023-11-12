# N, D, A, B = list(map(int, input().split()))
# list_off= []
# for i in range(N):
#     mn= list(map(int, input().split()))
#     list_off.append(mn[:-1])

"""N=8
    D=6
    A=1
    B=3
    
    1  -1
    3 -1
    4 -1
    5 -1
    2 4  -1
    -1
    -1
    3 -1
Mỗi ngày, một nhân viên chỉ làm nhiều nhất 1 ca 
Ngày hôm trước làm ca đêm thì hôm sau được nghỉ
Mỗi ca trong mỗi ngày có ít nhất A nhân viên và nhiều nhất B nhân viên 
F(i): danh sách các ngày nghỉ phép của nhân viên i """
def read_data():
    N, D, A, B = list(map(int, input().split()))
    list_off= []
    for i in range(N):
        mn= list(map(int, input().split()))
        list_off.append(mn[:-1])
    return N, D, A, B, list_off

N, D, A, B = 8, 6, 1, 3
list_off= [[1], [3], [4], [5], [2, 4], [], [], [3]]
min_shift_night= D

# create variables
X = [[] for i in range(N)] # save shift of employee i
day= [[] for i in range(D)] # count number of employee work on day d in shift k
available= [0]*D # save available slot of day d
change= [0]*D # save number of change shift of day d

best_solution= []
# init X
for i in range(N):
    for d in range(D):
        if d+1 in list_off[i]:
            X[i].append(0)    # 0: off

        else:
            X[i].append(-1)  # -1: on
# init day
for i in range(D):
    for k in range(5):
        day[i].append(0) 
# init available slot shift
for d in range(D):
    available[d] = N - sum([list_off[i].count(d+1) for i in range(N)])
    change[d] = N - sum([list_off[i].count(d+1) for i in range(N)])

def check_constraint_1(i, d, k):
    if X[i].count(4) >= min_shift_night:
        return False
    if day[d][k] >= B:
        return False
    num= 0
    for m in range(1, 5):
        if day[d][m] > 0:
            num+=day[d][m]
        else:
            num+=A
    # if day[d][k] >= available[d]-  num :#sum(day[d][i] for i in range(k+1, 5) if i!= k):
    #     return False
    if available[d]-num <=0:
        if day[d][k] >= A:
            return False
        # return False
    return True
# def solution():
#     thoa= True
#     for d in range(D):
#         for i in range(1, 5):
#             if day[d][i] <A:
#                 thoa= False
#                 break
#     if thoa:
#         global min_shift_night
#         # print("-"*20)
#         if sum(X[i].count(4) for i in range(N)) < min_shift_night:
#             best_solution= X
#             min_shift_night= sum(X[i].count(4) for i in range(N))
#         # min_shift_night= min(min_shift_night, sum(X[i].count(4) for i in range(N)))
#         # for i in range(N):
#         #     for d in range(D):
#         #         print(X[i][d], end=' ')
#         #     print()
def solution():
    print("-"*20)
    for i in range(N):
        for d in range(D):
            best_solution[i][d]= X[i][d]

def Try(i, d):
    if X[i][d]==0:
        if i== N-1 and d== D-1:
            solution()
        else:
            if d== D-1:
                Try(i+1, 0)
            else:
                Try(i, d+1)
    elif d>0 and X[i][d-1]==4:
        X[i][d]= 0
        available[d]-=1
        if i== N-1 and d== D-1:
            solution()
        else:
            if d== D-1:
                Try(i+1, 0)
            else:
                Try(i, d+1)
    else:
        for k in range(1, 5):
            if check_constraint_1(i, d, k):
                if k!=4:
                    X[i][d]= k
                    day[d][k]+=1
                    if i== N-1 and d== D-1:
                        solution()
                    else:
                        # if day[d][k]+ available[d]-i-1 >= A:
                            if d== D-1:
                                Try(i+1, 0)
                            else:
                                Try(i, d+1)

                    X[i][d]= -1
                    day[d][k]-=1
                # else:
                #     X[i][d]= k
                #     day[d][k]+=1
                #     if i== N-1 and d== D-1:
                #         solution()
                #     else:
                #         # if day[d][k]+ available[d]-i-1 >= A:
                #             if d== D-1:
                #                 Try(i+1, 0)
                #             else:
                #                 Try(i, d+1)

                #     X[i][d]= -1
                #     day[d][k]-=1
                #     available[d]+=1


Try(0, 0)
for i in range(N):
    for d in range(D):
        print(best_solution[i][d], end=' ')
    print()
