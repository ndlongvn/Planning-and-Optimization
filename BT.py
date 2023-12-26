#PYTHON 
# N, D, A, B = list(map(int, input().split()))
# list_off= []
# for i in range(N):
#     mn= list(map(int, input().split()))
#     list_off.append(mn[:-1])

""" N=8
    D=6
    A=1
    B=3
    
    8 6 1 3
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
F(i): danh sách các ngày nghỉ phép của nhân viên i 
"""
def read_data():
    N, D, A, B = list(map(int, input().split()))
    list_off= []
    for i in range(N):
        mn= list(map(int, input().split()))
        list_off.append(mn[:-1])
    return N, D, A, B, list_off

# N, D, A, B = 8, 6, 1, 3
# list_off= [[1], [3], [4], [5], [2, 4], [], [], [3]]
# min_shift_night= D

N, D, A, B, list_off= read_data()
min_shift_night= D

# create variables
X = [[] for i in range(N)] # save shift of employee i
day= [[] for i in range(D)] # count number of employee work on day d in shift k
available= [0]*D # save available slot of day d
shift_night= [0]*N # save number of shift night of employee i

best_solution= [[] for i in range(N)]
"""
0 1 1 1 1 1
1 1 0 1 1 1
1 1 1 0 1 1
1 2 1 1 0 2
2 0 4 0 2 2
2 3 2 2 3 4
4 0 3 3 4 0
3 4 0 4 0 3
"""
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

# Mỗi ca trong mỗi ngày có ít nhất A nhân viên và nhiều nhất B nhân viên 
def check_constraint_1(i, d, k):
    global min_shift_night
    # if X[i].count(4) >= min_shift_night:
    #     return False
    if max(shift_night[:i+1]) >= min_shift_night:
        return False
    if day[d][k] >= B:
        return False
    if d<D-1 and X[i][d+1]==0 and k==4:
        return False

    num= 0
    for m in range(1, 5):
        if day[d][m] == 0:
            num+=A

    if available[d]-num <=0:
        if day[d][k]!=0:
            return False
        elif day[d][k]==0:
            return True
    return True

# solution
def solution():
    global min_shift_night, best_solution
    # thoa= True
    # for i in range(D):
    #     for j in range(1, 5):
    #         if day[i][j] < A or day[i][j] > B:
    #             thoa= False
    #             break
    if min_shift_night > max(shift_night):
        min_shift_night= max(shift_night)
        if 1:
            # print("-"*10)
            # print("night shift",min_shift_night)
            for i in range(N):
                for d in range(D):
                #     print(X[i][d], end=' ')
                # print()
                    best_solution[i].append(X[i][d])
            # exit()
  
        # best_solution= X

# Try
# chẵn thì từ trên xuống, lẻ thì từ dưới lên
def Try(i, d):
    # print(i, d)
    # if d==D-1:
    #     if max(shift_night[:i+1]) >= min_shift_night:
    #         return
    if X[i][d]==0:
        # if i== N-1 and d== D-1:
        #     solution()
        if i== N-1 and d== D-1 and (D-1)%2==0:
            solution()
        elif (D-1)%2==1 and i==0 and d== D-1:
            solution()
        else:
            # if i==0 or max(shift_night[:i]+ [shift_night[i]+ (D-d+1)//2])  < min_shift_night:
                # if i== N-1:
                #     Try(0, d+1)
                # else:
                #     Try(i+1, d)
            if d%2==0:
                if i== N-1:
                    Try(i, d+1)
                else:
                    Try(i+1, d)
            else:
                if i==0:
                    Try(i, d+1)
                else:
                    Try(i-1, d)

    elif d>0 and X[i][d-1]==4:
            X[i][d]= 0
            available[d]-=1
            if i== N-1 and d== D-1 and (D-1)%2==0:
                solution()
            elif (D-1)%2==1 and i==0 and d== D-1:
                solution()
            else:
                # if i== N-1:
                #     Try(0, d+1)
                # else:
                #     Try(i+1, d)
                if d%2==0:
                    if i== N-1:
                        Try(i, d+1)
                    else:
                        Try(i+1, d)
                else:
                    if i==0:
                        Try(i, d+1)
                    else:
                        Try(i-1, d)
            
            X[i][d]= -1
            available[d]+=1
    else:
        for k in range(1, 5):
            if check_constraint_1(i, d, k):   
                if k==4:
                    shift_night[i]+=1
                    if d<D-1:  
                        available[d+1]-=1       
                X[i][d]= k
                day[d][k]+=1
                available[d]-=1

                if i== N-1 and d== D-1 and (D-1)%2==0:
                    solution()
                elif (D-1)%2==1 and i==0 and d== D-1:
                    solution()
                else:
                    # if i==0 or max(shift_night[:i]+ [shift_night[i]+ (D-d+1)//2])  < min_shift_night:
                        # if i== N-1:
                        #     Try(0, d+1)
                        # else:
                        #     Try(i+1, d)
                        if d%2==0:
                            if i== N-1:
                                Try(i, d+1)
                            else:
                                Try(i+1, d)
                        else:
                            if i==0:
                                Try(i, d+1)
                            else:
                                Try(i-1, d)

                if k==4:
                    shift_night[i]-=1 
                    if d<D-1:  
                        available[d+1]+=1  
                X[i][d]= -1
                day[d][k]-=1
                available[d]+=1

# main
Try(0, 0)
for i in range(N):
    for d in range(D):
        print(best_solution[i][d], end=' ')
    if i!=N-1:
        print()

# print("""0 4 0 3 2 2 
# 1 1 0 4 0 2 
# 1 3 2 0 3 3 
# 3 1 3 1 0 1 
# 4 0 1 0 1 4 
# 2 2 4 0 3 1 
# 3 3 2 2 4 0 
# 2 2 0 2 1 3 """)
