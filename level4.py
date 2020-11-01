import os
from io import StringIO

import numpy as np
import pandas as pd

from utils import write_solution, read_file


def create_df(file):

    tokens = file.split('\n')
    max_power = int(tokens[0])
    max_bill = int(tokens[1])
    num_minutes = int(tokens[2])

    energy_arr = np.array([int(x) for x in tokens[3: num_minutes + 3]], dtype=np.int)

    tasks = tokens[num_minutes + 4:]

    str_tasks = '\n'.join(tasks)

    task_df = pd.read_csv(StringIO(str_tasks), sep=" ", names=["taskId", "power", "startInterval", "endInterval"])

    return energy_arr, task_df, max_power, max_bill


def solve_level4(energy, tasks, max_power, max_bill):
    solution = ""

    energy_df = pd.DataFrame(energy, columns=["energy"])
    energy_df["power_left"] = max_power

    tasks = tasks.sort_values(by='power')

    for idx, row in tasks.iterrows():

        task_id = row['taskId']
        power = row['power']
        start = row['startInterval']
        end = row['endInterval'] + 1  # inclusive

        energy_df_selection = energy_df.iloc[start:end]
        energy_df_sorted = energy_df_selection.sort_values(by='energy')

        current_idx = 0
        power_drawn = 0
        energy_bill = 0

        solution += f"{task_id} "

        while power_drawn < power:
            power_needed = power - power_drawn

            if power_needed >= max_power:
                power_needed = max_power

            power_available = energy_df_sorted.iloc[current_idx, 1]

            if power_available < power_needed:
                power_needed = power_available

            power_drawn += power_needed
            energy_bill += power_needed * energy_df_sorted.iloc[current_idx, 0]

            power_idx = energy_df_sorted.iloc[current_idx].name

            energy_df_sorted.iloc[current_idx, 1] -= power_needed
            energy_df.iloc[power_idx, 1] -= power_needed
            if power_needed > 0:
                solution += f"{power_idx} {power_needed} "
            current_idx += 1

        print(f"ENERGY BILL: {energy_bill}")
        solution += "\n"

    return solution


if __name__ == '__main__':

    in_path = 'input/level4/'
    out_path = 'output/level4/'

    files = os.listdir(in_path)
    files = [f for f in files if f.endswith('.in')]

    # files = ['level4_example.in']

    for f in files:
        file = read_file(os.path.join(in_path, f))
        energy, tasks, max_power, max_bill = create_df(file)
        solution = solve_level4(energy, tasks, max_power, max_bill)
        print(solution)

        write_solution(os.path.join(out_path, f.replace('.in','.out')), solution)
