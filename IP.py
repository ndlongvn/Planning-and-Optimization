from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model
import numpy as np
# N, D, A, B = list(map(int, input().split()))
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

# list_off= []
# for i in range(N):
#     mn= list(map(int, input().split()))
#     list_off.append(mn[:-1])
N, D, A, B = 8, 6, 1, 3
list_off= [[1], [3], [4], [5], [2, 4], [], [], [3]]

# Create a solver
solver = pywraplp.Solver.CreateSolver('SCIP')


# Create binary decision variables X[i][d][k] for deciding whether employee i works on day d during shift k
X = []
for i in range(N):
    X.append([])
    for d in range(D):
        X[i].append([])
        if d+1 in list_off[i]:
            for k in range(4):  # 4 shifts per day
                X[i][d].append(solver.IntVar(0, 0, f'X[{i}][{d}][{k}]'))
        else:
            for k in range(4):  # 4 shifts per day
                X[i][d].append(solver.IntVar(0, 1, f'X[{i}][{d}][{k}]'))

for i in range(N):
    for d in range(D):
        solver.Add(solver.Sum(X[i][d][k] for k in range(4)) <= 1)

# Constraint 2: If an employee works the night shift on day d, they must have a day off on the entire next day (d+1)
for d in range(0, D-1):  # Start from the second day, as there is no "tomorrow" for the last day
    for i in range(N):

        solver.Add(X[i][d][3] + X[i][d+1][0] <= 1)
        solver.Add(X[i][d][3] + X[i][d+1][1] <= 1)
        solver.Add(X[i][d][3] + X[i][d+1][2] <= 1)
        solver.Add(X[i][d][3] + X[i][d+1][3] <= 1)

# Constraint 1: Each day must have shifts for at least A and at most B employees
for d in range(D):
    for k in range(4):
        solver.Add(solver.Sum(X[i][d][k] for i in range(N)) >= A)
        solver.Add(solver.Sum(X[i][d][k] for i in range(N)) <= B)
# for n in range(N):
#     for d in range(D):
#         solver.Add(sum(X[n][d][k] for d in range(D) for k in range(4)) >= A)
#         solver.Add(sum(X[n][d][k] for d in range(D) for k in range(4)) <= B)





# Constraint 3: Days off for each employee based on their preferences
# for i in range(N):
#     if len(list_off[i])==0:
#         continue
#     for d in list_off[i]:
#         for k in range(4):
#             solver.Add(X[i][d-1][k] == 0)

# Constraint 4: Each employee must work max 1 shift a day


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
