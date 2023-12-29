import random
import numpy as np

def generate_random_solution(N, D, A, B, days_off):
  X = np.zeros((N, D), dtype=int)
  for i in range(N):
    for d in range(D):
      if d+1 not in days_off[i]:
        X[i][d] = random.randint(0, 4)
  return X

def evaluate_solution(X):
  max_night_shifts = 0
  for i in range(X.shape[0]):
    max_night_shifts = max(max_night_shifts, sum(X[i] == 4))
  return max_night_shifts

def greedy_construction(X, N, D, A, B, days_off):
  for i in range(N):
    for d in range(D):
      if X[i][d] == 0 and d+1 not in days_off[i]:
        # Try all possible shifts for the employee
        for k in range(1, 5):
          X_temp = np.copy(X)
          X_temp[i][d] = k
          if is_feasible(X_temp, N, D, A, B):
            X = X_temp
            break
  return X

def is_feasible(X, N, D, A, B):
  # Check if each employee is assigned to at least one shift per day
  for i in range(N):
    if sum(X[i]) == 0:
      return False

  # Check if each shift has at least A and at most B employees
  for d in range(D):
    for k in range(1, 5):
      if sum(X[:, d] == k) < A or sum(X[:, d] == k) > B:
        return False

  return True

def local_search(X, N, D, A, B, days_off):
  for _ in range(1000):
    i, j = random.randint(0, N-1), random.randint(0, D-1)
    k, l = random.randint(1, 4), random.randint(1, 4)
    if i != j or k != l:
      X_temp = np.copy(X)
      X_temp[i][j], X_temp[i][l] = X_temp[i][l], X_temp[i][j]
      if is_feasible(X_temp, N, D, A, B):
        X = X_temp

  return X

def print_solution(X):
  for row in X:
    for val in row:
      print(val, end=" ")
    print()
    
def read_input_from_file(file_path):
    with open(file_path, 'r') as file:
        N, D, A, B = map(int, file.readline().split())
        days_off = []

        for _ in range(N):
            days = list(map(int, file.readline().split()))[:-1]
            days_off.append(days)
    return N, D, A, B, days_off

file_path = 'Planning-and-Optimization\\res\input_N_8_D_6.txt'  
N, D, A, B, list_off = read_input_from_file(file_path)

# def read_input():
#   N, D, A, B = map(int, input().split())
#   days_off = []

#   for _ in range(N):
#     days = list(map(int, input().split()))[:-1]
#     days_off.append(days)
#   return N, D, A, B, days_off
# N, D, A, B, list_off = read_input()

X = generate_random_solution(N, D, A, B, list_off)
X = greedy_construction(X, N, D, A, B, list_off)
# X = local_search(X, N, D, A, B, list_off)
print_solution(X)