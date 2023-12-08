# 1.03 29.11.2023
import pickle
import mdtraj as md
from analysis.systems import systems


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


if __name__ == "__main__":
    for system in systems.keys():
        fp_traj = f'{systems[system].path}/{systems[system].traj}'
        fp_tolopogy = f'{systems[system].path_pdb}/{systems[system].pdb}'

        data_to_pickle = load_md_data(fp_traj, fp_tolopogy)

        write_pickle_traj(data_to_pickle, systems[system].path)
