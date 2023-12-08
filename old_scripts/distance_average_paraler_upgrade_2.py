# Version 1.08 27.11.2023
from multiprocessing import Pool
from analysis.systems import systems
import mdtraj as md
import numpy as np
import logging
import datetime
import sqlite3
import os
from analysis.try_read_traj_sql import load_sqlite_traj

NO_CORES = 2


def setup_logging(filename):
    logging.basicConfig(filename=filename, level=logging.INFO)


def log_info(cluster, status):
    logging.info(f"\t\t{cluster}\t\t{status}\t\t{datetime.datetime.now().strftime('%d/%m/%Y, %H:%M:%S')}")


def calculate_distances_generic(system, cluster, distance_function, cluster_name_prefix):
    log_info(cluster, "started")

    table_name = f'ammonia_{system}'

    data = load_sqlite_traj(table_name)

    distances = distance_function(data['traj'])

    conn = sqlite3.connect("../svk_data/average_distance.db", timeout=40)
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
    log_info(cluster, "finished")

def calculate_distances_nn(traj):
    ns = traj.top.select('name N')
    pairs_nn = traj.topology.select_pairs(ns, ns)
    distances = md.compute_distances(traj, pairs_nn)
    return [np.average(step) * 10 for step in distances]


def calculate_distances_center_of_mass(traj):
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


def calculate_wrapper(args, distance_function, cluster_name_prefix):
    system, cluster = args
    calculate_distances_generic(system, cluster, distance_function, cluster_name_prefix)


if __name__ == "__main__":
    for file in ["average_distance.db", "CN_logger_db.log", "NN_logger_db.log"]:
        try:
            os.remove(file)
        except FileNotFoundError:
            pass

    setup_logging("../svk_data/CN_logger_db.log")
    systems_values = [[system,
                       system] for system in systems.keys()]

    with Pool(NO_CORES) as pool:
        pool.starmap(calculate_wrapper, [(system, calculate_distances_nn, 'nn_ammonia') for system in systems_values])
        pool.starmap(calculate_wrapper,
                     [(system, calculate_distances_center_of_mass, 'cn_ammonia') for system in systems_values])
