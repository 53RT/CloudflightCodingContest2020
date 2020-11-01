import os
import numpy as np
import pandas as pd

from utils import write_solution, read_file


def create_df(file):
    tokens = file.split('\n')

    num_minutes = int(tokens[0])

    arr = np.array([int(x) for x in tokens[1: num_minutes + 1]], dtype=np.int)

    intervals = tokens[num_minutes + 2:]
    intervals = [int(x.split(" ")[1]) for x in intervals if len(x)]

    return arr, intervals


def solve_level2(arr, intervals):
    solution = f"{len(intervals)}\n"

    for idx, ival in enumerate(intervals):
        pd_df = pd.Series(arr).rolling(window=ival).mean().iloc[ival - 1:].values
        argmin = np.argmin(pd_df)

        solution += f"{idx + 1} {argmin}\n"

    return solution


if __name__ == '__main__':

    in_path = 'input/level2/'
    out_path = 'output/level2/'

    files = os.listdir(in_path)
    files = [f for f in files if f.endswith('.in')]

    # files = ['level2_example.in']

    for f in files:
        file = read_file(os.path.join(in_path, f))
        df, intervals = create_df(file)
        solution = solve_level2(df, intervals)
        print(solution)

        write_solution(os.path.join(out_path, f.replace('.in', '.out')), solution)
