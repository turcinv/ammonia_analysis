# 1.04 29.11.2023
import pickle
import mdtraj as md
from analysis.systems import systems
from multiprocessing import Pool

NO_CORES = 4


def load_md_data(fp_traj, fp_topology):
    traj = md.load_xyz(fp_traj, top=fp_topology)
    topology = traj.topology
    ns = traj.top.select('name N')
    hs = traj.top.select('name H')

    data = {'traj': traj, 'topology': topology, 'ns': ns, 'hs': hs}
    return data


def write_pickle_traj(data_to_pickle, path):
    with open(f'{path}/trajectory_data.pkl', 'wb') as file:
        pickle.dump(data_to_pickle, file)


def load_pickle_traj(path):
    with open(f'{path}/trajectory_data.pkl', 'rb') as file:
        data = pickle.load(file)
    return data


def process_system(system):
    try:
        fp_traj = f'{systems[system].path}/{systems[system].traj}'
        fp_topology = f'{systems[system].path_pdb}/{systems[system].pdb}'

        # Load MD data
        traj = md.load_xyz(fp_traj, top=fp_topology)
        topology = traj.topology
        ns = traj.top.select('name N')
        hs = traj.top.select('name H')
        data_to_pickle = {'traj': traj, 'topology': topology, 'ns': ns, 'hs': hs}

        # Write to pickle
        with open(f'{systems[system].path}/trajectory_data.pkl', 'wb') as file:
            pickle.dump(data_to_pickle, file)
    except:
        print(f"error {system}")


if __name__ == "__main__":
    with Pool(NO_CORES) as pool:
        results = pool.map(process_system, systems.keys())
