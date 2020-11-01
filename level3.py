import os
from io import StringIO

import numpy as np
import pandas as pd

from utils import write_solution, read_file


def create_df(file):
    tokens = file.split('\n')

    num_minutes = int(tokens[0])

    arr = np.array([int(x) for x in tokens[1: num_minutes + 1]], dtype=np.int)

    tasks = tokens[num_minutes + 2:]
    str_tasks = '\n'.join(tasks)

    task_df = pd.read_csv(StringIO(str_tasks), sep=" ", names=["taskId", "power", "startInterval", "endInterval"])

    return arr, task_df


def solve_level3(arr, tasks):
    solution = f"{len(tasks)}\n"

    for idx, row in tasks.iterrows():
        print(idx, row)

        task_id = row['taskId']
        power = row['power']
        start = row['startInterval']
        end = row['endInterval'] + 1  # inclusive

        task_arr = arr[start:end]

        task_argmin = np.argmin(task_arr)
        argmin = start + task_argmin

        solution += f"{task_id} {argmin} {power}\n"

    return solution


if __name__ == '__main__':

    in_path = 'input/level3/'
    out_path = 'output/level3/'

    files = os.listdir(in_path)
    files = [f for f in files if f.endswith('.in')]

    # files = ['level3_example.in']

    for f in files:
        file = read_file(os.path.join(in_path, f))
        arr, tasks = create_df(file)
        solution = solve_level3(arr, tasks)
        print(solution)

        write_solution(os.path.join(out_path, f.replace('.in', '.out')), solution)
