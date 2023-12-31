import random

def greedy_shift_scheduling(N, D, A, B, day_off):
    schedule = [[0] * D for _ in range(N)]  # Initialize the schedule matrix
    night_shift_count = [0] * N  # Initialize night shift count for each employee

    for day in range(D):
        if day == 0:
            # Assign night shifts to random employees without day-off on the first day
            night_shift_assignments = random.sample(
                [i for i in range(N) if day + 1 not in day_off[i]], A
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
            # Check if the day before an employee did a night shift
            for emp in range(N):
                if schedule[emp][day - 1] == 4:
                    # Let that employee take the current day off
                    schedule[emp][day] = 0

            # Assign night shifts to employees with the smallest count of night shifts
            eligible_employees = [i for i in range(N) if day + 1 not in day_off[i] and schedule[i][day - 1] != 4]
            eligible_employees.sort(key=lambda emp: night_shift_count[emp])

            for i in range(1, A+1):
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

# Input
N, D, A, B = map(int, input().split())
day_off = [list(map(int, input().split()[:-1])) for _ in range(N)]

# Solve and output the result
result = greedy_shift_scheduling(N, D, A, B, day_off)
for row in result:
    print(*row)
