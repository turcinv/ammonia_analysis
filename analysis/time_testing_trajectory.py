import pickle
import mdtraj as md
import timeit
import sqlite3

from analysis.systems import systems

setup = "gc.enable()"
fp_traj = f'{systems[22].path}/{systems[22].traj}'
fp_tolopogy = f'{systems[22].path_pdb}/{systems[22].pdb}'


def md_time():
    start_time = timeit.default_timer()

    traj = md.load_xyz(fp_traj, top=fp_tolopogy)
    topology = traj.topology
    ns = traj.top.select('name N')
    end_time = timeit.default_timer()
    elapsed_time = end_time - start_time

    data = {'traj': traj, 'topology': topology, 'ns': ns, 'load_time': elapsed_time}
    return data


def pickle_time():
    start_time = timeit.default_timer()

    with open('trajectory_data.pkl', 'wb') as file:
        pickle.dump(data_to_pickle, file)

    end_time = timeit.default_timer()
    dump_time = end_time - start_time

    start_time = timeit.default_timer()

    with open('trajectory_data.pkl', 'rb') as file:
        data = pickle.load(file)

    end_time = timeit.default_timer()
    load_time = end_time - start_time

    data['dump_time'] = dump_time
    data['load_time'] = load_time

    return data


def sqlite_time():
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()

    cursor.execute('''DROP TABLE IF EXISTS my_table''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS my_table (
                        id INTEGER PRIMARY KEY,
                        traj BLOB,
                        topology BLOB,
                        ns BLOB
                    )''')

    # Serializace dat do bajtů
    traj_bytes = pickle.dumps(sqlite_data['traj'])
    topology_bytes = pickle.dumps(sqlite_data['topology'])
    ns_bytes = pickle.dumps(sqlite_data['ns'])

    # Uložení serializovaných dat do databáze
    start_time = timeit.default_timer()

    cursor.execute("INSERT INTO my_table (traj, topology, ns) VALUES (?, ?, ?)",
                   (sqlite3.Binary(traj_bytes), sqlite3.Binary(topology_bytes), sqlite3.Binary(ns_bytes)))

    conn.commit()

    end_time = timeit.default_timer()
    insert_time = end_time - start_time

    # Načtení serializovaných dat z databáze
    start_time = timeit.default_timer()

    cursor.execute("SELECT traj, topology, ns FROM my_table")
    result = cursor.fetchone()

    end_time = timeit.default_timer()
    select_time = end_time - start_time

    # Deserializace dat
    loaded_data = {
        'traj': pickle.loads(result[0]),
        'topology': pickle.loads(result[1]),
        'ns': pickle.loads(result[2])
    }

    conn.close()

    data = {
        'insert_time': insert_time,
        'select_time': select_time,
        'data': loaded_data
    }

    return data


if __name__ == "__main__":
    data_to_pickle = md_time()
    sqlite_data = md_time()
    print(md_time().keys())
    print(pickle_time().keys())
    print(sqlite_time().keys())

    md_time_results = timeit.repeat(md_time, setup=setup, repeat=10, number=1)
    print("\nmd_time():")
    for i, result in enumerate(md_time_results):
        print(f"Měření {i + 1}: {result} sekund")

    pickle_time_results = timeit.repeat(pickle_time, setup=setup, repeat=10, number=1)
    print("\npickle_time():")
    for i, result in enumerate(pickle_time_results):
        print(f"Měření {i + 1}: {result} sekund")

    sqlite_time_result = timeit.repeat(sqlite_time, setup=setup, repeat=10, number=1)
    print("\nsqlite_time():")
    for i, result in enumerate(sqlite_time_result):
        print(f"Měření {i + 1}: {result} sekund")

    pickle_data = pickle_time()
    print(f"\nPickle load_time: {pickle_data['load_time']} sekund")
    print(f"Pickle dump_time: {pickle_data['dump_time']} sekund")

    sqlite_data = sqlite_time()
    print(f"\nInsert time: {sqlite_data['insert_time']} sekund")
    print(f"Select time: {sqlite_data['select_time']} sekund")
