# Version 2.00 27.11.2023
from multiprocessing import Pool
from analysis.systems import systems
import mdtraj as md
import numpy as np
import logging
import datetime
import sqlite3
import os
from analysis.traj_to_pickle import load_pickle_traj

NO_CORES = 4


def calculate_distances_generic(path, cluster, distance_function, cluster_name_prefix):
    try:
        data = load_pickle_traj(path)

        distances = distance_function(data['traj'])

        conn = sqlite3.connect("average_distance.db")
        cursor = conn.cursor()

        cluster_name = f'{cluster_name_prefix}_{cluster}'
        cursor.execute(f'DROP TABLE IF EXISTS {cluster_name}')
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {cluster_name} (
                id INTEGER PRIMARY KEY,
                step INTEGER,
                distance REAL
            )
        ''')

        for index, distance_avg in enumerate(distances):
            cursor.execute(f'''
                INSERT INTO {cluster_name} (step, distance)
                VALUES (?, ?)
            ''', (index, distance_avg))

        conn.commit()
        conn.close()
    except:
        pass


def calculate_distances_nn(traj):
    try:
        ns = traj.top.select('name N')
        pairs_nn = traj.topology.select_pairs(ns, ns)
        distances = md.compute_distances(traj, pairs_nn)
        return [np.average(step) * 10 for step in distances]
    except:
        pass


def calculate_distances_center_of_mass(traj):
    try:
        ns = traj.top.select('name N')
        centers = md.compute_center_of_mass(traj)

        all_distances = []
        for index, frame in enumerate(centers):
            distances = []
            for N in ns:
                n = np.array(traj.xyz[index, N, :])
                center = np.array(frame)
                distances.append(np.linalg.norm(n - center) * 10)
            all_distances.append(np.average(distances))
        return all_distances
    except:
        pass


def calculate_wrapper(args, distance_function, cluster_name_prefix):
    path, cluster = args
    calculate_distances_generic(path, cluster, distance_function, cluster_name_prefix)


if __name__ == "__main__":
    try:
        os.remove("average_distance.db")
    except FileNotFoundError:
        pass

    systems_values = [[f"{systems[system].path}",
                       system] for system in systems.keys()]

    with Pool(NO_CORES) as pool:
        pool.starmap(calculate_wrapper, [(system, calculate_distances_nn, 'nn_ammonia') for system in systems_values])
        pool.starmap(calculate_wrapper,
                     [(system, calculate_distances_center_of_mass, 'cn_ammonia') for system in systems_values])
