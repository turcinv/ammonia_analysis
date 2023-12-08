# Version 22.06.2023
kinetic_energy = dict(
    title="<b>Kinetic energy</b>",
    add_trace=dict(
        mode='lines',
        line=dict(color='blue', width=1),
        hovertemplate='Time: %{x} fs<br>Kinetic energy: %{y} a.u.',
    ),
    update_yaxes=dict(
        title_text="Kinetic energy",
        showgrid=True, gridcolor='black',
        showline=True, linewidth=1, linecolor='black',
        zeroline=True, zerolinecolor='black',
    ),
    update_xaxes=dict(
        title_text="Time",
        rangeslider=dict(visible=True, thickness=0.05),
        showgrid=True, gridcolor='black',
        showline=True, linewidth=1, linecolor='black',
        zeroline=True, zerolinecolor='black',
    ),
)

temperature = dict(
    title="<b>Temperature</b>",
    add_trace=dict(
        mode='lines',
        line=dict(color='red', width=1),
        hovertemplate='Time: %{x} fs<br>Temperature: %{y} K',
    ),
    update_yaxes=dict(
        title_text="Temperature",
        showgrid=True, gridcolor='black',
        showline=True, linewidth=1, linecolor='black',
        zeroline=True, zerolinecolor='black',
    ),
    update_xaxes=dict(
        title_text="Time",
        rangeslider=dict(visible=True, thickness=0.05),
        showgrid=True, gridcolor='black',
        showline=True, linewidth=1, linecolor='black',
        zeroline=True, zerolinecolor='black',
    ),
)

potential_energy = dict(
    title="<b>Potential energy</b>",
    add_trace=dict(
        mode='lines',
        line=dict(color='green', width=1),
        hovertemplate='Time: %{x} fs<br>Potential energy: %{y} a.u.',
    ),
    update_yaxes=dict(
        title_text="Potential energy",
        showgrid=True, gridcolor='black',
        showline=True, linewidth=1, linecolor='black',
        zeroline=True, zerolinecolor='black',
    ),
    update_xaxes=dict(
        title_text="Time",
        rangeslider=dict(visible=True, thickness=0.05),
        showgrid=True, gridcolor='black',
        showline=True, linewidth=1, linecolor='black',
        zeroline=True, zerolinecolor='black',
    ),

)

used_time = dict(
    title="<b>Used time</b>",
    add_trace=dict(
        mode='lines',
        line=dict(color='lime', width=1),
        hovertemplate='Time: %{x} fs<br>Used time: %{y} s',
    ),
    update_yaxes=dict(
        title_text="Used time",
        showgrid=True, gridcolor='black',
        showline=True, linewidth=1, linecolor='black',
        zeroline=True, zerolinecolor='black',
    ),
    update_xaxes=dict(
        title_text="Time",
        rangeslider=dict(visible=True, thickness=0.05),
        showgrid=True, gridcolor='black',
        showline=True, linewidth=1, linecolor='black',
        zeroline=True, zerolinecolor='black',
    ),
)
