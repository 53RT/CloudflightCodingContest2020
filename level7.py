import os
from io import StringIO

import numpy as np
import pandas as pd

from utils import write_solution, read_file


def create_df(file):
    tokens = file.split('\n')

    max_power = int(tokens[0])
    max_bill = int(tokens[1])
    max_concurrent_tasks = int(tokens[2])

    num_minutes = int(tokens[3])  # N
    num_houses = int(tokens[num_minutes + 4])  # H

    energy_arr = np.array([int(x) for x in tokens[4: num_minutes + 4]], dtype=np.int)

    task_list = []
    intervals_list = []

    tokens = tokens[num_minutes + 5:]

    for i in range(num_houses):
        num_intervals = int(tokens[0])  # M
        tasks = tokens[1:num_intervals + 1]
        str_tasks = '\n'.join(tasks)

        task_df = pd.read_csv(StringIO(str_tasks), sep=" ", names=["taskId", "power", "startInterval", "endInterval"])

        task_list.append(task_df)
        intervals_list.append(num_intervals)

        tokens = tokens[num_intervals + 1:]

    return energy_arr, task_list, max_power, max_bill, max_concurrent_tasks, num_houses


def solve_level7(energy, task_list, max_power, max_bill, max_concurrent_tasks, num_houses):
    solution = f"{num_houses}\n"

    energy_df = pd.DataFrame(energy, columns=["energy"])
    energy_df["power_left"] = max_power
    energy_df["task_drawn"] = max_concurrent_tasks

    energy_bill = 0

    for house_idx in range(num_houses):

        tasks = task_list[house_idx]

        tasks = tasks.sort_values(by="power")

        solution += f"{house_idx + 1}\n"
        solution += f"{len(tasks) + 1}\n"

        for idx, row in tasks.iterrows():

            taskId = row['taskId']
            power = row['power']
            start = row['startInterval']
            end = row['endInterval'] + 1  # inclusive

            energy_df_selection = energy_df.iloc[start:end]
            energy_df_sorted = energy_df_selection.sort_values(by=['energy', 'task_drawn', 'power_left'],
                                                               ascending=[True, False, False])

            current_idx = 0
            power_drawn = 0

            solution += f"{taskId} "

            while power_drawn < power:

                if current_idx >= len(energy_df_sorted):
                    current_idx = 0

                power_needed = power - power_drawn

                if power_needed >= max_power:
                    power_needed = max_power

                power_available = energy_df_sorted.iloc[current_idx, 1]
                minute_available = energy_df_sorted.iloc[current_idx, 2]

                if minute_available <= 0:
                    current_idx += 1
                    continue

                if power_available < power_needed:
                    power_needed = power_available

                power_drawn += power_needed

                energy_price = energy_df_sorted.iloc[current_idx, 0] * (1 + (power_needed / max_power))
                energy_df_sorted.iloc[current_idx, 0] = energy_price

                energy_bill += power_needed * energy_price

                power_idx = energy_df_sorted.iloc[current_idx].name

                energy_df_sorted.iloc[current_idx, 1] -= power_needed
                energy_df.iloc[power_idx, 1] -= power_needed

                # Reduce Concurrent Task Counter
                energy_df_sorted.iloc[current_idx, 2] -= 1
                energy_df.iloc[power_idx, 2] -= 1

                # Overwrite Prices
                energy_df_sorted.iloc[current_idx, 0] = energy_price
                energy_df.iloc[power_idx, 0] = energy_price

                if power_needed > 0:
                    solution += f"{power_idx} {power_needed} "
                current_idx += 1

                if current_idx > np.random.randint(3, len(energy_df_sorted) - 1):
                    energy_df_sorted = energy_df_selection.sort_values(by=['power_left', 'task_drawn', 'energy', ],
                                                                       ascending=[False, False, True])
                    current_idx = 0

            print(f"ENERGY BILL:", {energy_bill})
            solution += "\n"

            if energy_bill > max_bill:
                raise ValueError("BILL EXCEEDED")

    return solution


if __name__ == '__main__':
    print("Start")

    in_path = 'input/level7/'
    out_path = 'output/level7/'

    files = os.listdir(in_path)
    files = [f for f in files if f.endswith('.in')]

    # files = ['level7_example.in']
    files = ['level7_1.in']

    for f in files:
        file = read_file(os.path.join(in_path, f))
        energy, task_list, max_power, max_bill, max_concurrent_tasks, num_houses = create_df(file)
        solution = solve_level7(energy, task_list, max_power, max_bill, max_concurrent_tasks, num_houses)
        print(solution)

        write_solution(os.path.join(out_path, f.replace('.in', '.out')), solution)
