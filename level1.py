import os
import numpy as np

from utils import read_file, write_solution


def create_df(file_in):
    tokens = file_in.split('\n')
    num_minutes = int(tokens[0])

    arr = np.array([int(x) for x in tokens[1:1 + num_minutes]], dtype=np.int)

    return arr


def solve_level1(arr):
    return str(np.argmin(arr))


if __name__ == '__main__':

    in_path = 'input/level1/'
    out_path = 'output/level1/'

    files = os.listdir(in_path)
    files = [f for f in files if f.endswith('.in')]

    # files = ['level1_example.in']

    for f in files:
        file = read_file(os.path.join(in_path, f))
        df = create_df(file)
        solution = solve_level1(df)
        print(solution)

        write_solution(os.path.join(out_path, f.replace('.in', '.out')), solution)
