from ortools.sat.python import cp_model

def shift_scheduling(N, D, A, B, leave_days):
    model = cp_model.CpModel()

    # Variables
    employees = range(1, N+1)
    days = range(1, D+1)
    shifts = range(1, 5)
    x = {}
    
    # Create the model
    for i in employees:
        for d in days:
            for s in shifts:
                x[(i, d, s)] = model.NewBoolVar(f"x_i{i}_d{d}_s{s}")

    # Constraints
    for i in employees:
        # An employee works at most one shift per day
        for d in days: 
            model.AddAtMostOne(x[(i, d, s)] for s in shifts)

        # Day off constraint
        for off_day in leave_days[i-1]:
            for s in shifts: 
                model.Add(x[(i, off_day, s)] == 0)

    for d in range(2, D+1):
        for i in employees:
            for s in shifts:
                # If the day before an employee worked the night shift, then the next day he gets the day off
                model.Add(x[(i, d, s)] == 0).OnlyEnforceIf(x[(i, d-1, 4)])
    for d in days:
        for s in shifts: 
            # Each shift in each day has at least A employee and at most B employee
            numOfEmployeePerShift = sum(x[(i, d, s)] for i in employees)
            model.Add(numOfEmployeePerShift >= A)
            model.Add(numOfEmployeePerShift <= B)
        
        
    # Objective: Minimize the maximum number of night shifts assigned to a given employee
    max_night_shifts = model.NewIntVar(0, D, 'max_night_shifts')
    for i in employees:
        model.AddMaxEquality(max_night_shifts, [sum(x[(i, d, 4)] for d in days)])
        model.Minimize(max_night_shifts)
    
    # Objective: Minimize the total number of night shifts
    total_night_shifts = model.NewIntVar(0, N * D, 'total_night_shifts')
    night_shifts_per_employee = [sum(x[(i, d, 4)] for d in days) for i in employees]
    model.Add(total_night_shifts == sum(night_shifts_per_employee))
    model.Minimize(total_night_shifts)
        
    # Solve
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
               
    # Output to terminal
    if status == cp_model.OPTIMAL:
        solution = [[[solver.Value(x[i, d, s]) * s for s in shifts] for d in days] for i in employees]
        for i in range(N):
            print(" ".join(map(str, [sum(solution[i][d-1]) for d in days])))
    else:
        print("No solution found.")

# Read input from file
with open('Planning-and-Optimization\\res\input_N_8_D_6.txt', 'r') as input_file:
    N, D, A, B = map(int, input_file.readline().split())
    leave_days = []
    for _ in range(N):
        leave_days.append(list(map(int, input_file.readline().split()[:-1])))

# Solve and print output to terminal
shift_scheduling(N, D, A, B, leave_days)
