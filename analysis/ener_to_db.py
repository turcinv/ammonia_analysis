# Version 1.00 20.11.2023
from analysis.systems import systems
from analysis.ammonia import Ammonia

for system in systems.keys():
    Ammonia(system).save_ener_to_database()
