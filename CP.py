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



# Create the solver
model = cp_model.CpModel()

# Define the variables and constraints
X = []
for i in range(N):
    X.append([])
    for d in range(D):
        X[i].append([])
        if d+1 in list_off[i]:
            for k in range(4):  # 4 shifts per day
                X[i][d].append(model.NewIntVar(0, 0, f'X[{i}][{d}][{k}]'))
        else:
            for k in range(4):  # 4 shifts per day
                X[i][d].append(model.NewIntVar(0, 1, f'X[{i}][{d}][{k}]'))

for i in range(N):
    for d in range(D):
        model.Add(sum(X[i][d][k] for k in range(4)) <= 1)

# Constraint 2: If an employee works the night shift on day d, they must have a day off on the entire next day (d+1)
for d in range(0, D-1):  # Start from the second day, as there is no "tomorrow" for the last day
    for i in range(N):
        model.Add(X[i][d][3] + X[i][d+1][0] <= 1)
        model.Add(X[i][d][3] + X[i][d+1][1] <= 1)
        model.Add(X[i][d][3] + X[i][d+1][2] <= 1)
        model.Add(X[i][d][3] + X[i][d+1][3] <= 1)

# Constraint 1: Each day must have shifts for at least A and at most B employees
for d in range(D):
    for k in range(4):
        model.Add(sum(X[i][d][k] for i in range(N)) >= A)
        model.Add(sum(X[i][d][k] for i in range(N)) <= B)


# Objective: Minimize the maximum number of night shifts assigned to any employee
max_night_shifts = model.NewIntVar(0, D, 'max_night_shifts')
for i in range(N):
    model.Add(max_night_shifts >= sum(X[i][d][3] for d in range(D)))


# Set the objective to minimize the maximum night shifts
model.Minimize(max_night_shifts)

solver = cp_model.CpSolver()
solver.parameters.linearization_level = 0
# Enumerate all solutions.
solver.parameters.enumerate_all_solutions = True

status = solver.Solve(model)
# Print the solution
if status == cp_model.OPTIMAL:

    # Print the schedule
    for i in range(N):
        for d in range(D):
            val= 0
            for k in range(4):
                if solver.Value(X[i][d][k]) ==1:
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
