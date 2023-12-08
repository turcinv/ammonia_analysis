from analysis.systems import systems
from analysis.traj_to_pickle import load_pickle_traj


def check_bounce(system, max_box=2.49):
    data = load_pickle_traj(f'{systems[system].path}')
    traj = data['traj']
    ns = traj.top.select('name N or name H')

    x = traj.xyz[:, ns, 0]
    y = traj.xyz[:, ns, 1]
    z = traj.xyz[:, ns, 2]

    xyz = [x, y, z]

    xyz_indexes = {
        0: "x",
        1: "y",
        2: "z",
    }

    for i, coord in enumerate(xyz):
        for index, dist in enumerate(coord):
            max_dist = max(dist)
            min_dist = min(dist)
            if max_dist >= max_box:
                print(f"System {system} - 0draz 25 A: Snímek {index}, Osa {xyz_indexes[i]}")
            elif min_dist <= 0:
                print(f"System {system} - Odraz 0 A: Snímek {index}, Osa {xyz_indexes[i]}")
            else:
                pass
