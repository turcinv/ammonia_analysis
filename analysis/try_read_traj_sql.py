import sqlite3
import pickle
from analysis.systems import systems
import mdtraj as md
import os
def load_md_data(fp_traj, fp_topology):
    traj = md.load_xyz(fp_traj, top=fp_topology)
    topology = traj.topology
    ns = traj.top.select('name N')
    hs = traj.top.select('name H')

    data = {'traj': traj, 'topology': topology, 'ns': ns, 'hs': hs}
    return data


def write_sqlite_traj(sqlite_data, table_name):
    conn = sqlite3.connect('../svk_data/trajectories.db')
    cursor = conn.cursor()
    cursor.execute(f'''DROP TABLE IF EXISTS {table_name}''')
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS {table_name} (
                            id INTEGER PRIMARY KEY,
                            traj BLOB,
                            topology BLOB,
                            ns BLOB,
                            hs BLOB
                        )''')

    traj_bytes = pickle.dumps(sqlite_data['traj'])
    topology_bytes = pickle.dumps(sqlite_data['topology'])
    ns_bytes = pickle.dumps(sqlite_data['ns'])
    hs_bytes = pickle.dumps(sqlite_data['hs'])

    cursor.execute(f"INSERT INTO {table_name} (traj, topology, ns, hs) VALUES (?, ?, ?, ?)",
                   (sqlite3.Binary(traj_bytes), sqlite3.Binary(topology_bytes), sqlite3.Binary(ns_bytes),
                    sqlite3.Binary(hs_bytes)))

    conn.commit()
    conn.close()


def load_sqlite_traj(table_name):
    conn = sqlite3.connect('../svk_data/trajectories.db', timeout=10)
    cursor = conn.cursor()

    cursor.execute(f"SELECT traj, topology, ns, hs FROM {table_name}")
    result = cursor.fetchone()
    conn.commit()
    conn.close()

    data = {
        'traj': pickle.loads(result[0]),
        'topology': pickle.loads(result[1]),
        'ns': pickle.loads(result[2]),
        'hs': pickle.loads(result[3])
    }

    return data


if __name__ == "__main__":
    os.remove('../svk_data/trajectories.db')
    for system in systems.keys():
        fp_traj = f'{systems[system].path}/{systems[system].traj}'
        fp_tolopogy = f'{systems[system].path_pdb}/{systems[system].pdb}'

        sqlite_data = load_md_data(fp_traj, fp_tolopogy)

        write_sqlite_traj(sqlite_data, f'ammonia_{system}')

        data = load_sqlite_traj(f'ammonia_{system}')

        print(data.keys())
