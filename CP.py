from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model
import numpy as np


def read_input():
    N, D, A, B = map(int, input().split())
    days_off = []

    for _ in range(N):
        days = list(map(int, input().split()))[:-1]
        days_off.append(days)
    return N, D, A, B, days_off


N, D, A, B, list_off = read_input()

# Create the solver
model = cp_model.CpModel()

# Define the variables and constraints
X = []
for i in range(N):
    X.append([])
    for d in range(D):
        X[i].append([])
        for k in range(4):  # 4 shifts per day
            X[i][d].append(model.NewBoolVar(f"X[{i}][{d}][{k}]"))

# Constraint 1: Employee can take the next day off if they work night shift today
# Constraint 2: Each employee only work at max 1 shift per day
# Constraint 3: Employee doesn't work night shift on the night before their day off
for i in range(N):
    for d in range(D):
        if d >= 1:
            model.Add(sum(X[i][d][k] for k in range(4)) == 0).OnlyEnforceIf(
                X[i][d - 1][3]
            )
            if d + 1 not in list_off[i]:
                model.Add(sum(X[i][d][k] for k in range(4)) == 1).OnlyEnforceIf(
                    X[i][d - 1][3].Not()
                )
        else:
            if d + 1 not in list_off[i]:
                model.Add(sum(X[i][d][k] for k in range(4)) == 1)

# Contraint 4: Every shift in every day have minimum A and maximum 4 employees
for d in range(D):
    for k in range(4):
        model.Add(sum(X[i][d][k] for i in range(N)) >= A)
        model.Add(sum(X[i][d][k] for i in range(N)) <= B)

# Contraint 5: List of employee's day off
for i in range(N):
    for d in range(D):
        if d + 1 in list_off[i]:
            model.Add(sum(X[i][d][k] for k in range(4)) == 0)

# Objective: Minimize the maximum number of night shifts assigned to any employee
max_night_shifts = model.NewIntVar(0, D, "max_night_shifts")
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
            val = 0
            for k in range(4):
                if solver.Value(X[i][d][k]) == 1:
                    # print(f'Employee {i+1} works on day {d+1} during shift {k+1}')
                    val = k + 1
            print(val, end=" ")
        print()


else:
    print("No solution found.")
