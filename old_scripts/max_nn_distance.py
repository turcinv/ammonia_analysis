# Version 1.01 20.11.2023
import mdtraj as md
from analysis.systems import systems
from analysis.traj_to_pickle import load_pickle_traj


def calculate_distances_nn(path):
    data = load_pickle_traj(path)
    traj = data['traj']
    topology = data['topology']
    ns = traj.top.select('name N')
    pairs_nn = topology.select_pairs(ns, ns)
    distances = md.compute_distances(traj, pairs_nn)
    for index, step in enumerate(distances):
        distances[index] = step * 10

    return distances


for system in systems.keys():
    x = calculate_distances_nn(f"{systems[system].path}")

    max_distances = []

    for index, distance in enumerate(x):
        max_distances.append(max(distance))

    with open(f"{systems[system].no_ammonia}-{systems[system].id_cluster}-nn.csv", "w") as file:
        for index, distance in enumerate(max_distances):
            print(index, distance, sep=",", file=file)
