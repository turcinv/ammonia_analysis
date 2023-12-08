# Version 1.03 23.11.2023
import mdtraj as md
import numpy as np
from analysis.systems import systems
from multiprocessing import Pool


def calculate_distances_center_of_mass(fp_topology, fp_traj):
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

        all_distances.append(distances)

    return all_distances


def write_distances(system, fp_topology, fp_traj):
    # Wrapper funkce, která provádí výpočet a zároveň zapisuje výsledky do souboru
    distances = calculate_distances_center_of_mass(fp_topology, fp_traj)
    max_distances = [max(distance) for distance in distances]

    with open(f"{system.no_ammonia}-{system.id_cluster}-cn.csv", "w") as file:
        for index, distance in enumerate(max_distances):
            print(index, distance, sep=",", file=file)


def process_system(system):
    # Funkce, která připraví argumenty pro wrapper funkci
    fp_topology = f"pdb_coordinates/{system.pdb}"
    fp_traj = f"{system.path}/{system.traj}"
    write_distances(system, fp_topology, fp_traj)


if __name__ == "__main__":
    # Nastavení počtu jader pro paralelní zpracování
    # NO_CORES = os.cpu_count()  # nebo pevně nastavený počet, například 6

    NO_CORES = 2

    # Vytvoření seznamu systémů pro zpracování
    systems_to_process = [systems[key] for key in systems.keys()]

    # Využití Pool pro paralelní zpracování
    with Pool(NO_CORES) as pool:
        pool.map(process_system, systems_to_process)
