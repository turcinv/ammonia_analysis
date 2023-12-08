# Version 1.01 06.07.2023
from clusters.systems import systems
from pathlib import Path

for system in systems.keys():
    path_parent = Path(systems[system].path).parent
    path_dir = Path(path_parent, 'vde_frames')
    path_dir.mkdir()
