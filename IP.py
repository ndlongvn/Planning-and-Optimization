#PYTHON 
from ortools.linear_solver import pywraplp
import numpy as np
N, D, A, B = list(map(int, input().split()))
# """N=8
#     D=6
#     A=1
#     B=3
    
#     1  -1
#     3 -1
#     4 -1
#     5 -1
#     2 4  -1
#     -1
#     -1
#     3 -1"""

list_off= []
for i in range(N):
    mn= list(map(int, input().split()))
    list_off.append(mn[:-1])
# N, D, A, B = 8, 6, 1, 3
# list_off= [[1], [3], [4], [5], [2, 4], [], [], [3]]
# print(list_off)
# Create a solver
solver = pywraplp.Solver.CreateSolver('SCIP')


# Create binary decision variables X[i][d][k] for deciding whether employee i works on day d during shift k
X = []
for i in range(N):
    X.append([])
    for d in range(D):
        X[i].append([])
        for k in range(4):
            X[i][d].append(solver.IntVar(0, 1, f'X[{i}][{d}][{k}]'))

for i in range(N):
    for d in range(D):
        if d+1 in list_off[i]:
            for k in range(4): # ngay nghi
                solver.Add(X[i][d][k] == 0)
        if d+2 in list_off[i]: # truoc ngay nghi ko phai lam ca dem
            solver.Add(X[i][d][3] == 0)

for i in range(N): # 1 nguoi lam toi da 1 ca trong 1 ngay
    for d in range(D):
        solver.Add(solver.Sum(X[i][d][k] for k in range(4)) <= 1)

# Constraint 2: If an employee works the night shift on day d, they must have a day off on the entire next day (d+1)
for d in range(0, D-1):  # Start from the second day, as there is no "tomorrow" for the last day
    for i in range(N):
        if d==0 and d+1 not in list_off[i]:
            solver.Add(solver.Sum(X[i][d][k] for k in range(4)) == 1)
        if d+2 in list_off[i]: # neu ngay d la ngay nghi va d-1 ko nghi thi d-1 phai di lam ban ngay
            if d+1 not in list_off[i]:
                solver.Add(X[i][d][0] + X[i][d][1] + X[i][d][2] == 1)
        if d+2 not in list_off[i] and d+1 not in list_off[i]:
            solver.Add(1000*(X[i][d][3]-1) + X[i][d+1][0] + X[i][d+1][1] + X[i][d+1][2] + X[i][d+1][3] <= 0)
            solver.Add(1000*X[i][d][3] + X[i][d+1][0] + X[i][d+1][1] + X[i][d+1][2] + X[i][d+1][3] >=1 )



# Constraint 1: Each day must have shifts for at least A and at most B employees
for d in range(D):
    for k in range(4):
        solver.Add(solver.Sum(X[i][d][k] for i in range(N)) >= A)
        solver.Add(solver.Sum(X[i][d][k] for i in range(N)) <= B)


# Objective: Minimize the maximum number of night shifts assigned to any employee
max_night_shifts = solver.IntVar(0, D, 'max_night_shifts')
for i in range(N):
    solver.Add(max_night_shifts >= solver.Sum(X[i][d][3] for d in range(D)))


# Set the objective to minimize the maximum night shifts
solver.Minimize(max_night_shifts)


# Solve the problem
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL:

    # Print the schedule
    for i in range(N):
        for d in range(D):
            val= 0
            for k in range(4):
                if X[i][d][k].solution_value() ==1:
                    # print(f'Employee {i+1} works on day {d+1} during shift {k+1}')
                    val= k+1
            print(val, end= " ")
        print()


else:
    print('No solution found.')

    """
    0 4 0 3 2 2 
    1 1 0 4 0 2 
    1 3 2 0 3 3 
    3 1 3 1 0 1 
    4 0 1 0 1 4 
    2 2 4 0 3 1 
    3 3 2 2 4 0 
    2 2 0 2 1 3 
    """
