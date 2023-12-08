# Version 1.06 23.11.2023
from multiprocessing import Pool
from analysis.systems import systems
import mdtraj as md
import numpy as np
import logging
import datetime
import sqlite3
import os

NO_CORES = 6


def calculate_distances_nn(fp_topology, fp_traj, cluster):
    logging.basicConfig(filename="NN_logger_db.log", level=logging.INFO)
    logging.info(f"\t\t{cluster}\t\tstarted\t\t{datetime.datetime.now().strftime('%d/%m/%Y, %H:%M:%S')}")

    traj = md.load_xyz(fp_traj, top=md.load(fp_topology))
    topology = traj.topology
    ns = traj.top.select('name N')
    pairs_nn = topology.select_pairs(ns, ns)
    distances = md.compute_distances(traj, pairs_nn)
    distances_avg = []
    for step in distances:
        distances_avg.append(np.average(step) * 10)

    conn = sqlite3.connect("../svk_data/average_distance.db")
    cursor = conn.cursor()

    cluster_name = f'nn_ammonia_{cluster}'

    cursor.execute(f'''
        DROP TABLE IF EXISTS {cluster_name}''')

    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {cluster_name} (
            cluster TEXT,
            step INTEGER,
            distance REAL
        )
    ''')

    for index, distance_avg in enumerate(distances_avg):
        cursor.execute(f'''
                INSERT INTO {cluster_name} (cluster, step, distance)
                VALUES (?, ?, ?)
            ''', (cluster, index, distance_avg))

    conn.commit()
    conn.close()

    logging.info(f"\t\t{cluster}\t\tfinished\t{datetime.datetime.now().strftime('%d/%m/%Y, %H:%M:%S')}")


def calculate_distances_center_of_mass(fp_topology, fp_traj, cluster):
    logging.basicConfig(filename="../svk_data/CN_logger_db.log", level=logging.INFO)
    logging.info(f"\t\t{cluster}\t\tstarted\t\t{datetime.datetime.now().strftime('%d/%m/%Y, %H:%M:%S')}")
    traj = md.load_xyz(fp_traj, top=md.load(fp_topology))
    ns = traj.top.select('name N')
    centers = md.compute_center_of_mass(traj)

    all_distances = []

    for index, frame in enumerate(centers):
        distances = []
        for N in ns:
            n = np.array(traj.xyz[index, N, :])
            center = np.array(frame)
            distance = np.linalg.norm(n - center) * 10
            distances.append(distance)
        average_dist = np.average(distances)
        all_distances.append(average_dist)

    conn = sqlite3.connect("../svk_data/average_distance.db")
    cursor = conn.cursor()

    cluster_name = f'cn_ammonia_{cluster}'

    cursor.execute(f'''
            DROP TABLE IF EXISTS {cluster_name}''')

    cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {cluster_name} (
                cluster TEXT,
                step INTEGER,
                distance REAL
            )
        ''')

    for index, distance_avg in enumerate(all_distances):
        cursor.execute(f'''
                    INSERT INTO {cluster_name} (cluster, step, distance)
                    VALUES (?, ?, ?)
                ''', (cluster, index, distance_avg))

    conn.commit()
    conn.close()

    logging.info(f"\t\t{cluster}\t\tfinished\t{datetime.datetime.now().strftime('%d/%m/%Y, %H:%M:%S')}")


def calculate_distances_nn_wrapper(args):
    fp_topology, fp_traj, cluster = args
    calculate_distances_nn(fp_topology, fp_traj, cluster)


def calculate_distances_center_of_mass_wrapper(args):
    fp_topology, fp_traj, cluster = args
    calculate_distances_center_of_mass(fp_topology, fp_traj, cluster)


if __name__ == "__main__":
    try:
        os.remove("../svk_data/average_distance.db")
        os.remove("../svk_data/CN_logger_db.log")
        os.remove("NN_logger_db.log")

    except FileNotFoundError:
        pass

    system_id_NN = {}
    system_id_CN = {}
    for system in systems.keys():
        system_id_NN[system] = [
            f"pdb_coordinates/ammonia-{systems[system].no_ammonia}-{systems[system].id_cluster}.pdb",
            f"ammonia-{systems[system].no_ammonia}-{systems[system].id_cluster}/production/small-clusters-pos-1.xyz",
            system,
        ]
    for system in systems.keys():
        system_id_CN[system] = [
            f"pdb_coordinates/ammonia-{systems[system].no_ammonia}-{systems[system].id_cluster}.pdb",
            f"ammonia-{systems[system].no_ammonia}-{systems[system].id_cluster}/production/small-clusters-pos-1.xyz",
            system,
        ]

    with Pool(NO_CORES) as pool:
        pool.map(calculate_distances_nn_wrapper, system_id_NN.values())

    with Pool(NO_CORES) as pool:
        pool.map(calculate_distances_center_of_mass_wrapper, system_id_CN.values())
