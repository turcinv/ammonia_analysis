# Version 2.02 03.12.2023

# Normal modules
from pathlib import Path, PurePosixPath
import pandas as pd
import sqlite3
import plotly.graph_objs as go
import plotly.subplots
import datetime
from collections import namedtuple
from typing import NoReturn
# My scripts
from analysis.systems import systems
from analysis.config import kinetic_energy, temperature, potential_energy, used_time


class Ammonia:
    def __init__(self, system_id: int) -> NoReturn:
        """

        :param system_id:
        """
        self.system: namedtuple = systems[system_id]
        self.system_id: int = system_id
        self.no_ammonia: int = int(self.system.no_ammonia)
        self.id_cluster: int = self.system.id_cluster

        self.path: Path = Path(self.system.path)
        self.file_ener: PurePosixPath = PurePosixPath(self.path,
                                                      Path(self.system.ener))

        self.path_pdb: PurePosixPath = PurePosixPath(Path(self.system.path_pdb),
                                                     Path(self.system.pdb))

        self.path_traj: PurePosixPath = PurePosixPath(Path(self.system.path),
                                                      Path(self.system.ener))

    def save_ener_to_database(self) -> NoReturn:
        """
        # TODO
        :return:
        """
        data_ener: pd.DataFrame = pd.read_csv(self.file_ener,
                                              sep='\s+',
                                              skiprows=1,
                                              header=None)
        data_ener: pd.DataFrame = data_ener.rename(columns={0: "step",
                                                            1: "time",
                                                            2: "kin",
                                                            3: "temp",
                                                            4: "pot",
                                                            5: "cons",
                                                            6: "used_time",
                                                            }
                                                   )
        conn: sqlite3.connect = sqlite3.connect("ener_database.db")
        cursor = conn.cursor()
        cluster_name: str = f'ammonia_{self.system_id}'
        cursor.execute(f'''
                    CREATE TABLE IF NOT EXISTS {cluster_name} (
                        step INTEGER,
                        time REAL,
                        kin REAL,
                        temp REAL,
                        pot REAL,
                        cons REAL,
                        used_time REAL
                    )
                ''')

        data_ener.to_sql(cluster_name, conn, if_exists='replace', index=False)

        conn.commit()
        conn.close()

    def load_ener_from_database(self) -> pd.DataFrame:
        """

        :return:
        """
        data_name: str = f"ammonia_{self.system_id}"
        conn: sqlite3.connect = sqlite3.connect('ener_database.db')
        query_ener: str = f'SELECT * FROM {data_name}'
        data_ener: pd.read_sql_query = pd.read_sql_query(query_ener, conn)
        conn.close()

        return data_ener

    def generate_ener_figure(self) -> plotly.subplots.make_subplots:
        """

        :return:
        """
        fig: plotly.subplots.make_subplots = plotly.subplots.make_subplots(rows=2, cols=2, subplot_titles=(
            kinetic_energy["title"], temperature["title"], potential_energy["title"], used_time["title"]), )
        time = self.load_ener_from_database()["time"]
        fig.add_trace(
            go.Scatter(x=time, y=self.load_ener_from_database()["kin"], name="<b>Kinetic energy</b>",
                       **kinetic_energy["add_trace"]), row=1, col=1)
        fig.add_trace(go.Scatter(x=time, y=self.load_ener_from_database()["temp"], name="<b>Temperature</b>",
                                 **temperature["add_trace"]), row=1, col=2)
        fig.add_trace(
            go.Scatter(x=time, y=self.load_ener_from_database()["pot"], name="<b>Potential energy</b>",
                       **potential_energy["add_trace"]), row=2, col=1)
        fig.add_trace(go.Scatter(x=time, y=self.load_ener_from_database()["used_time"], name="<b>Used time</b>",
                                 **used_time["add_trace"]), row=2, col=2)

        fig.update_yaxes(**kinetic_energy["update_yaxes"], row=1, col=1)
        fig.update_yaxes(**temperature["update_yaxes"], row=1, col=2)
        fig.update_yaxes(**potential_energy["update_yaxes"], row=2, col=1)
        fig.update_yaxes(**used_time["update_yaxes"], row=2, col=2)

        fig.update_xaxes(**kinetic_energy["update_xaxes"], row=1, col=1)
        fig.update_xaxes(**temperature["update_xaxes"], row=1, col=2)
        fig.update_xaxes(**potential_energy["update_xaxes"], row=2, col=1)
        fig.update_xaxes(**used_time["update_xaxes"], row=2, col=2)

        fig.update_layout(
            title={'text': self.name(),
                   'x': 0.5,
                   'y': 0.95,
                   'font': dict(size=25),
                   },
            width=1650,
            height=1000,
            showlegend=True,
            plot_bgcolor='white',
            paper_bgcolor='lightgray',
            annotations=[
                dict(
                    text="<b>Kinetic energy</b>",
                    font=dict(size=18),
                    x=0.25, y=1.03,
                    showarrow=False,
                    xref="paper", yref="paper",
                ),
                dict(
                    text="<b>Temperature</b>",
                    font=dict(size=18),
                    x=0.75, y=1.03,
                    showarrow=False,
                    xref="paper", yref="paper",
                ),
                dict(
                    text="<b>Potential energy</b>",
                    font=dict(size=18),
                    x=0.25, y=0.40,
                    showarrow=False,
                    xref="paper", yref="paper",
                ),
                dict(
                    text="<b>Used time</b>",
                    font=dict(size=18),
                    x=0.75, y=0.40,
                    showarrow=False,
                    xref="paper", yref="paper",
                )
            ]
        )
        return fig

    def vde_mp2_fig(self):
        data = pd.read_csv(systems[self].mp2, delimiter=',', header=None)
        data = data.rename(columns={0: 'frames',
                                    1: 'electron',
                                    2: 'neutral',
                                    }
                           )
        VDE = []
        for index, frame in enumerate(data['frames']):
            VDE.append((data['electron'][index] - data['neutral'][index]) * 27.211324570273)

        data['VDE'] = VDE

        fig = plotly.subplots.make_subplots(rows=1, cols=1)
        fig.add_trace(
            go.Scatter(x=data['frames'], y=data['VDE'], name="<b>Test</b>",
                       mode='lines', line=dict(color='blue', width=1),
                       hovertemplate='Time: %{x} fs<br>VDE: %{y} eV')

        )
        fig.update_xaxes(title_text="<b>Time (fs)</b>",
                         title_font=dict(color='black'),
                         rangeslider=dict(visible=True, thickness=0.1),
                         showgrid=True, gridcolor='black',
                         showline=True, linewidth=1, linecolor='black',
                         zeroline=True, zerolinecolor='black',
                         tickfont=dict(color='black'), )

        fig.update_yaxes(title_text="<b>VDE (eV)</b>",
                         title_font=dict(color='black'),
                         showgrid=True, gridcolor='black',
                         showline=True, linewidth=1, linecolor='black',
                         zeroline=True, zerolinecolor='black',
                         tickfont=dict(color='black'), )

        fig.update_layout(
            title="<b>VDE in time</b>",
            title_font=dict(color='black'),
            title_x=0.5,
            width=1000,
            height=500,
            showlegend=True,
            legend=dict(
                font=dict(color='black'),
            ),
            plot_bgcolor='white',
            paper_bgcolor='lightgray',
        )

        return fig

    def name(self) -> str:
        """

        :return:
        """
        return f"<b>Ammonia {self.no_ammonia}-{self.id_cluster}</b>"

    def save_figure(self) -> NoReturn:
        """

        :return:
        """
        self.generate_ener_figure().write_html(f'{self.path}/{datetime.datetime.now().strftime("%d-%m-%Y")}-'
                                               f'{self.no_ammonia}-{self.id_cluster}.html')

    def __str__(self) -> str:
        """

        :return:
        """
        return f"Ammonia {self.no_ammonia}-{self.id_cluster}"
