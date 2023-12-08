# Version 1.00 02.12.2023
import sqlite3
from collections import namedtuple


def get_table_names():
    table_names = []
    conn = sqlite3.connect('systems.db')
    cursor = conn.cursor()
    cursor.execute("""SELECT name FROM sqlite_master 
    WHERE type='table';""")

    for i in cursor.fetchall():
        table_names.append(i[0])

    conn.close()

    return table_names


def get_data_from_tables():
    table_names = get_table_names()
    system = namedtuple("system", ["id", "no_ammonia", "id_cluster", "path", "ener", "path_pdb", "pdb", "traj"])
    systems = {}
    for table in table_names:
        conn = sqlite3.connect('systems.db')
        cursor = conn.cursor()
        cursor.execute(f"""SELECT * FROM {table}""")
        system_table = cursor.fetchone()
        conn.commit()
        conn.close()
        systems[system_table[0]] = system(id=system_table[0],
                                          no_ammonia=system_table[1],
                                          id_cluster=system_table[2],
                                          path=system_table[3],
                                          ener=system_table[4],
                                          path_pdb=system_table[5],
                                          pdb=system_table[6],
                                          traj=system_table[7])

    return systems


def get_id_from_tables():
    table_names = get_table_names()
    systems = []
    for table in table_names:
        conn = sqlite3.connect('systems.db')
        cursor = conn.cursor()
        cursor.execute(f"""SELECT * FROM {table}""")
        system_table = cursor.fetchone()
        conn.commit()
        conn.close()
        systems.append(str(system_table[0]))

    return systems



