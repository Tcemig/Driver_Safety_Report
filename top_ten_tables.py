import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.colors import n_colors
from statistics import mean
import datetime as dt
import json

file = "05.03-05.09 2025"

data = pd.read_csv(f'Weekly Event Worksheets\\{file}.csv')

behavior_list = [
    'aggressive',
    'failed to Stop',
    'posted speed violation',
    'speed policy violation',
    'near collision',
    'near collision - unavoidable',
    'following distance',
    'curb strike',
    'lens obstruction',
    'no seat belt',
    'drowsy',
    'handheld device',
    'inattentive',
    'red light',
    'passenger(s) in vehicle',
    'mirror use',
    'smoking',
    'too fast for conditions',
    'intersection awareness',
    'backing on a roadway',
]

data['Trigger'] = data['Trigger'].str.lower()
data['Behaviors'] = data['Behaviors'].str.lower()

data_dict = {}

for b in behavior_list:
    behavior_dict = {}
    for v in data['Vehicle'].unique():
        temp_df = data[data['Vehicle'] == v]
        behavior_count = temp_df['Behaviors'].str.contains(b).sum()
        if behavior_count == 0:
            continue

        driver_associated = temp_df['Driver'].iloc[0]
        if driver_associated == 'Driver Unassigned':
            driver_associated = v
        behavior_dict[v] = {'count': behavior_count, 'driver': driver_associated}
        behavior_dict = {k: v for k, v in behavior_dict.items() if v['count'] > 0}
        behavior_dict = dict(sorted(behavior_dict.items(), key=lambda item: item[1]['count'], reverse=True))
        # keep only top 10
        behavior_dict = {k: v for k, v in list(behavior_dict.items())[:10]}
        # add to data_df
        data_dict[b] = behavior_dict

# drop all tables with no values
data_dict = {k: v for k, v in data_dict.items() if len(v) > 0}

# sort data_dict by len of values
data_dict = dict(sorted(data_dict.items(), key=lambda item: len(item[1]), reverse=True))

fig = make_subplots(
    rows=(len(data_dict) + 2) // 3,  # Calculate rows needed for 3 columns
    cols=3,  # Set the number of columns to 3
    subplot_titles=[k.title() for k in data_dict.keys()],
    vertical_spacing=0.01,
    horizontal_spacing=0.01,
    specs=[[{'type': 'domain'} for _ in range(3)] for _ in range((len(data_dict) + 2) // 3)],  # Set all subplots to 'domain'
)

# Define a list of six light colors for table backgrounds
light_colors = ["#FFEBEE", "#E3F2FD", "#E8F5E9", "#FFF3E0", "#F3E5F5", "#E0F7FA"]

for i, (k, v) in enumerate(data_dict.items()):
    row = i // 3 + 1  # Adjust row calculation for 3 columns
    col = i % 3 + 1  # Adjust column calculation for 3 columns
    vehicles = list(v.keys())  # Vehicle names
    drivers = [v[x]['driver'] for x in v.keys()]
    counts = [v[x]['count'] for x in v.keys()]
    
    # Rotate through the light colors for each table
    table_color = light_colors[i % len(light_colors)]
    
    fig.add_trace(
        go.Table(
            header=dict(
                values=["Vehicle".title(), "Driver".title(), "Count".title()],  # Title case for headers
                align="center",
                fill_color="lightgrey",
                font=dict(color="black", size=20),
                height=40,
                line=dict(color="black", width=1),
            ),
            cells=dict(
                values=[vehicles, drivers, counts],
                align="center",
                fill_color=[
                    [table_color if j % 2 == 0 else "white" for j in range(len(vehicles))]
                ],  # Striped rows
                font=dict(color="black", size=16), 
                height=30,
                line=dict(color="black", width=1),
            ),
        ),
        row=row,
        col=col,
    )

fig.update_layout(
    height=2500,
    width=1800,
    title=dict(
        text=f"Top 10 Behaviors by Vehicle From LYTX - {file}",
        font=dict(size=24)  # Adjust the font size here
    ),
    showlegend=False,
)
fig.show()

# save fig to html
fig.write_html(f"LYTX_Top_10_Driver_Tables\\{file} top10.html")
