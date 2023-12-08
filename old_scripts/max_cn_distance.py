# Version 1.04 27.11.2023
import mdtraj as md
import numpy as np
from analysis.systems import systems
from analysis.traj_to_pickle import load_pickle_traj


def calculate_distances_center_of_mass(path):
    data = load_pickle_traj(path)
    traj = data['traj']
    ns = data['ns']
    centers = md.compute_center_of_mass(traj)

    all_distances = []

    for index, frame in enumerate(centers):
        distances = []
        for N in ns:
            n = np.array(traj.xyz[index, N, :])
            center = np.array(frame)
            distance = np.linalg.norm(n - center) * 10
            distances.append(distance)

        all_distances.append(distances)

    return all_distances


for system in systems.keys():
    x = calculate_distances_center_of_mass(f"{systems[system].path}")

    max_distances = []

    for index, distance in enumerate(x):
        max_distances.append(max(distance))

    with open(f"{systems[system].no_ammonia}-{systems[system].id_cluster}-cn.csv", "w") as file:
        for index, distance in enumerate(max_distances):
            print(index, distance, sep=",", file=file)
