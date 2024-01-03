import random
import timeit

def greedy_shift_scheduling(N, D, A, B, day_off):
    schedule = [[0] * D for _ in range(N)]  # Initialize the schedule matrix
    night_shift_count = [0] * N  # Initialize night shift count for each employee
    minimum_night_shift = 0

    for day in range(D):
        if day == 0:
            # No solution found
            if N > 4*B + sum([1 for d in day_off if d == day + 1]): return [[0] * D for _ in range(N)]
            # Least amount of night shift required
            minimum_night_shift = max(
                A, N - sum([1 for d in day_off if d == day + 1]) - B * 3
            )
            # Assign night shifts to random employees without day-off on the first day
            night_shift_assignments = random.sample(
                [i for i in range(N) if day + 1 not in day_off[i]], minimum_night_shift
            )
            for emp in night_shift_assignments:
                schedule[emp][day] = 4
                night_shift_count[emp] += 1

            # Assign remaining shifts 1, 2, 3
            remaining_employees = [i for i in range(N) if day + 1 not in day_off[i] and schedule[i][day] != 4]
            random.shuffle(remaining_employees)
            for i, emp in enumerate(remaining_employees):
                shift = (i % 3) + 1
                schedule[emp][day] = shift

        else:
            leave_count = sum([1 for d in day_off if d == day + 1])
            # Check if the day before an employee did a night shift
            for emp in range(N):
                if schedule[emp][day - 1] == 4:
                    # Let that employee take the current day off
                    schedule[emp][day] = 0
                    if day + 1  not in day_off[emp]: leave_count += 1
            # No solution found
            if N > 4*B + leave_count: return [[0] * D for _ in range(N)] 
            
            # Least amount of night shift required    
            minimum_night_shift = max(
                A, N - leave_count - B * 3
            )
            # Assign night shifts to employees with the smallest count of night shifts
            eligible_employees = [i for i in range(N) if day + 1 not in day_off[i] and schedule[i][day - 1] != 4]
            eligible_employees.sort(key=lambda emp: night_shift_count[emp])

            for i in range(1, minimum_night_shift + 1):
                emp = eligible_employees[i]
                schedule[emp][day] = 4
                night_shift_count[emp] += 1

            # Assign remaining shifts 1, 2, 3
            remaining_employees = [i for i in range(N) if day + 1 not in day_off[i] and schedule[i][day - 1] != 4 and schedule[i][day] != 4]
            random.shuffle(remaining_employees)
            for i, emp in enumerate(remaining_employees):
                shift = (i % 3) + 1
                if schedule[emp][day] == 0:
                    schedule[emp][day] = shift

    return schedule

# Read input from file
with open('res\input_N_400_D_50.txt', 'r') as f:
    N, D, A, B = map(int, f.readline().split())
    day_off = [list(map(int, line.split()[:-1])) for line in f.readlines()]

# Solve and measure runtime
start_time = timeit.default_timer()
result = greedy_shift_scheduling(N, D, A, B, day_off)
end_time = timeit.default_timer()
runtime = end_time - start_time

# Write output to file
with open('output.txt', 'w') as f:
    if result == [[0] * D for _ in range(N)]: 
        f.write('No solution found' + '\n')
    else:
        for row in result:
            f.write(' '.join(map(str, row)) + '\n')
        f.write(f'Runtime: {runtime * 1000:.5f} milliseconds\n')