# Version 3.00 02.12.2023
from pathlib import Path
import re
import datetime
import os
import sqlite3
from collections import namedtuple


def extract_numbers(folder_name):
    """ Extrakce obou čísel ze jména složky. """
    match = re.search(r'ammonia-(\d+)-(\d+)', folder_name)
    if match:
        return int(match.group(1)), int(match.group(2))
    else:
        return float('inf'), float('inf')  # Vrací velké číslo pro složky, které nevyhovují vzoru


def generate_systems(path: str, type_of_simulation: str):
    root = Path(f"{path}")
    folders = [folder for folder in root.iterdir() if folder.is_dir()]
    sorted_folders = sorted(folders, key=lambda x: extract_numbers(x.name))
    pdb_folder = "pdb_coordinates"
    systems = {}

    system = namedtuple("system", ["id", "no_ammonia", "id_cluster", "path", "ener", "path_pdb", "pdb", "traj"])

    try:
        for folder in sorted_folders:
            if folder.is_dir():
                try:
                    no_ammonia, id_cluster = re.findall(r'\d+', folder.name)
                    ener = 'small-clusters-1.ener'
                    path_pdb = f'ammonia-{no_ammonia}-{id_cluster}.pdb'
                    path_traj = 'small-clusters-pos-1.xyz'
                    cluster = system(int(f'{no_ammonia}{id_cluster}'), no_ammonia, id_cluster,
                                     f'{folder.name.lower()}/{type_of_simulation}',
                                     ener, pdb_folder, path_pdb, path_traj)
                    systems[int(f'{no_ammonia}{id_cluster}')] = cluster
                except ValueError:
                    pass

        for key, value in systems.items():
            conn = sqlite3.connect("systems.db")
            cursor = conn.cursor()
            table_name = f' ammonia_{key}'
            cursor.execute(f'DROP TABLE IF EXISTS {table_name}')
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {table_name}
                    (id INTEGER PRIMARY KEY ,
                    no_ammonia TEXT,
                    id_cluster TEXT,
                    path TEXT,
                    ener TEXT,
                    path_pdb TEXT,
                    pdb TEXT,
                    traj TEXT
                    )
                    ''')

            cursor.execute(f'''
                INSERT INTO {table_name} (id, no_ammonia, id_cluster, path, ener, path_pdb, pdb, traj)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                           (value.id, value.no_ammonia, value.id_cluster, value.path, value.ener, value.path_pdb,
                            value.pdb, value.traj))
            conn.commit()
            conn.close()

    except FileNotFoundError:
        print("Folder not found")


if __name__ == "__main__":
    os.remove('systems.db')
    generate_systems(path="./", type_of_simulation="production")
