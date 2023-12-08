# Version 1.07 23.11.2023
from multiprocessing import Pool
from analysis.systems import systems
import mdtraj as md
import numpy as np
import logging
import datetime
import sqlite3
import os

NO_CORES = 6


def setup_logging(filename):
    logging.basicConfig(filename=filename, level=logging.INFO)


def log_info(cluster, status):
    logging.info(f"\t\t{cluster}\t\t{status}\t\t{datetime.datetime.now().strftime('%d/%m/%Y, %H:%M:%S')}")


def calculate_distances_generic(fp_topology, fp_traj, cluster, distance_function, cluster_name_prefix):
    log_info(cluster, "started")

    traj = md.load_xyz(fp_traj, top=md.load(fp_topology))
    distances = distance_function(traj)

    conn = sqlite3.connect("../svk_data/average_distance.db")
    cursor = conn.cursor()

    cluster_name = f'{cluster_name_prefix}_{cluster}'
    cursor.execute(f'DROP TABLE IF EXISTS {cluster_name}')
    cursor.execute(f'''
        CREATE TABLE {cluster_name} (
            cluster TEXT,
            step INTEGER,
            distance REAL
        )
    ''')

    for index, distance_avg in enumerate(distances):
        cursor.execute(f'''
            INSERT INTO {cluster_name} (cluster, step, distance)
            VALUES (?, ?, ?)
        ''', (cluster, index, distance_avg))

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
    fp_topology, fp_traj, cluster = args
    calculate_distances_generic(fp_topology, fp_traj, cluster, distance_function, cluster_name_prefix)


if __name__ == "__main__":
    for file in ["average_distance.db", "CN_logger_db.log", "NN_logger_db.log"]:
        try:
            os.remove(file)
        except FileNotFoundError:
            pass

    setup_logging("../svk_data/CN_logger_db.log")
    systems_values = [[f"pdb_coordinates/ammonia-{systems[system].no_ammonia}-{systems[system].id_cluster}.pdb",
                       f"ammonia-{systems[system].no_ammonia}-{systems[system].id_cluster}/production/small-clusters-pos-1.xyz",
                       system] for system in systems.keys()]

    with Pool(NO_CORES) as pool:
        pool.starmap(calculate_wrapper, [(system, calculate_distances_nn, 'nn_ammonia') for system in systems_values])
        pool.starmap(calculate_wrapper,
                     [(system, calculate_distances_center_of_mass, 'cn_ammonia') for system in systems_values])
