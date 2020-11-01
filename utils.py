import os

def read_file(path):
    with open(path, 'r') as f:
        file = f.read()

    return file


def write_solution(path, solution):
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))

    with open(path, 'w') as f:
        f.write(solution)