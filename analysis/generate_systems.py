# Version 2.00 15.11.2023
from pathlib import Path
import re
import datetime
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

        with open(f"{path}systems.py", "w") as file:
            print(f"# Version {datetime.date.today()}", file=file)
            print('from collections import namedtuple\n', file=file)
            print('system = '
                  'namedtuple("system", ["id", "no_ammonia", "id_cluster", "path", "ener", "path_pdb", "pdb", "traj"])',
                  file=file)
            print("systems = {", file=file)
            for key, value in systems.items():
                print(f'\t{key}: {value},', file=file)
            print("}", file=file)

    except:
        print("Folder not found")


if __name__ == "__main__":
    generate_systems(path="./", type_of_simulation="production")
