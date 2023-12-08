# Version 2.00 02.12.2023
import sqlite3
import mdtraj as md
import numpy as np
from analysis.read_systems_db import get_data_from_tables, get_table_names
from analysis.traj_to_pickle import load_pickle_traj


def calculate_max_distances_center_of_mass(path):
    data = load_pickle_traj(path)
    traj = data['traj']
    ns = data['ns']
    centers = md.compute_center_of_mass(traj)

    all_distances = []

    for index, center in enumerate(centers):
        n_coords = traj.xyz[index, ns, :]
        distances = np.linalg.norm(n_coords - center, axis=1) * 10
        all_distances.append(distances)

    return all_distances


def save_max_distances_center_of_mass():
    systems = get_data_from_tables()
    table_names = get_table_names()



    for index, system in enumerate(systems.keys()):
        conn = sqlite3.connect("max_distance_cn.db")
        cursor = conn.cursor()
        cursor.execute(f"""DROP TABLE IF EXISTS {table_names[index]}""")
        cursor.execute(f"""CREATE TABLE IF NOT EXISTS {table_names[index]}(
                                    step INTEGER PRIMARY KEY,
                                    max_distance REAL
                                )""")

        distances = calculate_max_distances_center_of_mass(f"{systems[system].path}")
        max_distances = np.max(distances, axis=1)
        for step, distance in enumerate(max_distances):
            cursor.execute(f"INSERT INTO {table_names[index]} (step, max_distance) VALUES (?, ?)",
                         (step, float(distance)))

        content_to_write = "\n".join([f"{index},{distance}" for index, distance in enumerate(max_distances)])

        with open(f"./max_distance_cn/{systems[system].no_ammonia}-{systems[system].id_cluster}-cn.csv", "w") as file:
            file.write(content_to_write)

        conn.commit()
        conn.close()

if __name__ == '__main__':
    systems = get_data_from_tables()
    table_names = get_table_names()
    conn = sqlite3.connect("max_distance_cn.db")
    cursor = conn.cursor()

    for index, system in enumerate(systems.keys()):

        cursor.execute(f"""DROP TABLE IF EXISTS {table_names[index]}""")
        cursor.execute(f"""CREATE TABLE IF NOT EXISTS {table_names[index]}(
                                step INTEGER PRIMARY KEY,
                                max_distance REAL
                            )""")

        distances = calculate_max_distances_center_of_mass(f"{systems[system].path}")
        max_distances = np.max(distances, axis=1)
        for step, distance in enumerate(max_distances):
            conn.execute(f"INSERT INTO {table_names[index]} (step, max_distance) VALUES (?, ?)",
                         (step,max_distances))
            conn.commit()


        content_to_write = "\n".join([f"{index},{distance}" for index, distance in enumerate(max_distances)])

        with open(f"./max_distance_cn/{systems[system].no_ammonia}-{systems[system].id_cluster}-cn.csv", "w") as file:
            file.write(content_to_write)

    conn.close()


