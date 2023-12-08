# Version 2.00 02.12.2023
import mdtraj as md
import numpy as np
from analysis.traj_to_pickle import load_pickle_traj
import sqlite3
from analysis.read_systems_db import get_data_from_tables, get_table_names


def calculate_max_distances_nn(path):
    data = load_pickle_traj(path)
    traj = data['traj']
    topology = data['topology']
    ns = data['ns']
    pairs_nn = topology.select_pairs(ns, ns)
    distances = md.compute_distances(traj, pairs_nn)
    return distances * 10


def save_max_distances_nn():
    systems = get_data_from_tables()
    table_names = get_table_names()


    for index, system in enumerate(systems.keys()):
        conn = sqlite3.connect("max_distance_nn.db")
        cursor = conn.cursor()
        cursor.execute(f"""DROP TABLE IF EXISTS {table_names[index]}""")
        cursor.execute(f"""CREATE TABLE IF NOT EXISTS {table_names[index]}(
                                    step INTEGER PRIMARY KEY,
                                    max_distance REAL
                                )""")

        distances = calculate_max_distances_nn(f"{systems[system].path}")
        max_distances = np.max(distances, axis=1)
        for step, distance in enumerate(max_distances):
            cursor.execute(f"INSERT INTO {table_names[index]} (step, max_distance) VALUES (?, ?)",
                         (step, float(distance)))

        content_to_write = "\n".join([f"{index},{distance}" for index, distance in enumerate(max_distances)])

        with open(f"./max_distance_nn/{systems[system].no_ammonia}-{systems[system].id_cluster}-nn.csv", "w") as file:
            file.write(content_to_write)

        conn.commit()
        conn.close()


if __name__ == '__main__':
    systems = get_data_from_tables()
    table_names = get_table_names()

    for index, system in enumerate(systems.keys()):
        conn = sqlite3.connect("max_distance_nn.db")
        cursor = conn.cursor()
        cursor.execute(f"""DROP TABLE IF EXISTS {table_names[index]}""")
        cursor.execute(f"""CREATE TABLE IF NOT EXISTS {table_names[index]}(
                                step INTEGER PRIMARY KEY,
                                max_distance REAL
                            )""")

        distances = calculate_max_distances_nn(f"{systems[system].path}")
        max_distances = np.max(distances, axis=1)
        for step, distance in enumerate(max_distances):
            conn.execute(f"INSERT INTO {table_names[index]} (step, max_distance) VALUES (?, ?)",
                         (step,distance))

        conn.commit()
        conn.close()

        content_to_write = "\n".join([f"{index},{distance}" for index, distance in enumerate(max_distances)])

        with open(f"./max_distance_nn/{systems[system].no_ammonia}-{systems[system].id_cluster}-nn.csv", "w") as file:
            file.write(content_to_write)
