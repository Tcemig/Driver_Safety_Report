from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from plotly.colors import n_colors
from statistics import mean

drop_behaviors_list = [
    'Food or Drink',
    'Other Concern',
    'Driver Smoking',
    'Driver Tagged',
    'Following Distance: > 1 sec to < 2 sec',
    'Incomplete Stop',
    'Failed to Stop',
    'No Seat Belt',
    
    # Non-Priority Behaviors
    'Camera Issue',
    'Parked-Highway/Ramp',
    'Collision',
    'Passenger Unbelted',
    'Electronic Device - Distraction',
    'Cell Hands Free - Observed',
    'Other Communication Device - Observed',
    
    ]
how_many_rows = -24

Contractor_df = pd.read_csv('Main_CSV_Files\\Contractor_df.csv')
Linehaul_df = pd.read_csv('Main_CSV_Files\\Linehaul_df.csv')
COV_df = pd.read_csv('Main_CSV_Files\\COV_df.csv')

LYTX_Vehicles_Breakdown_df = pd.read_csv('Main_CSV_Files\\LYTX_Vehicles_BreakDown_df.csv')
Behaviors_df = pd.read_csv('Main_CSV_Files\\Behaviors_df.csv')
Behaviors_df = Behaviors_df.drop(drop_behaviors_list, axis=1)

COV_Behaviors_df = pd.read_csv('Main_CSV_Category_Files\\COV_Behaviors.csv')
COV_Behaviors_df = COV_Behaviors_df.drop(drop_behaviors_list, axis=1)
COV_Behaviors_df = COV_Behaviors_df.iloc[how_many_rows:, :]

Contractor_Behaviors_df = pd.read_csv('Main_CSV_Category_Files\\Contractor_Behaviors.csv')
Contractor_Behaviors_df = Contractor_Behaviors_df.drop(drop_behaviors_list, axis=1)
Contractor_Behaviors_df = Contractor_Behaviors_df.iloc[how_many_rows:, :]

Linehaul_Behaviors_df = pd.read_csv('Main_CSV_Category_Files\\Linehaul_Behaviors.csv')
Linehaul_Behaviors_df = Linehaul_Behaviors_df.drop(drop_behaviors_list, axis=1)
Linehaul_Behaviors_df = Linehaul_Behaviors_df.iloc[how_many_rows:, :]


# Overview of Program Preformance
COV_overviewOfProgramPreformance_df = COV_Behaviors_df[['Date', 'Week', 'Year', 'Total']] # Behaviors']]
COV_overviewOfProgramPreformance_df['Active ERs'] = 0
for index, row in COV_overviewOfProgramPreformance_df.iterrows():
    temp_date = COV_overviewOfProgramPreformance_df.loc[index, "Date"][:10]
    temp_date = f"{temp_date[5:7]}-{temp_date[:4]}"
    temp_df = LYTX_Vehicles_Breakdown_df[LYTX_Vehicles_Breakdown_df['Date'] == temp_date]
    temp_df = temp_df['COV ERs'].values
    COV_overviewOfProgramPreformance_df.loc[index, 'Active ERs'] = temp_df
COV_overviewOfProgramPreformance_df['Frequency'] = COV_overviewOfProgramPreformance_df['Total'] / COV_overviewOfProgramPreformance_df['Active ERs']

Linehaul_overviewOfProgramPreformance_df = Linehaul_Behaviors_df[['Date', 'Week', 'Year', 'Total']] # Behaviors']]
Linehaul_overviewOfProgramPreformance_df['Active ERs'] = 0
for index, row in Linehaul_overviewOfProgramPreformance_df.iterrows():
    temp_date = Linehaul_overviewOfProgramPreformance_df.loc[index, "Date"][:10]
    temp_date = f"{temp_date[5:7]}-{temp_date[:4]}"
    temp_df = LYTX_Vehicles_Breakdown_df[LYTX_Vehicles_Breakdown_df['Date'] == temp_date]
    temp_df = temp_df['Linehaul ERs'].values
    Linehaul_overviewOfProgramPreformance_df.loc[index, 'Active ERs'] = temp_df
Linehaul_overviewOfProgramPreformance_df['Frequency'] = Linehaul_overviewOfProgramPreformance_df['Total'] / Linehaul_overviewOfProgramPreformance_df['Active ERs']

Contractor_overviewOfProgramPreformance_df = Contractor_Behaviors_df[['Date', 'Week', 'Year', 'Total']] # Behaviors']]
Contractor_overviewOfProgramPreformance_df['Active ERs'] = 0
for index, row in Contractor_overviewOfProgramPreformance_df.iterrows():
    temp_date = Contractor_overviewOfProgramPreformance_df.loc[index, "Date"][:10]
    temp_date = f"{temp_date[5:7]}-{temp_date[:4]}"
    temp_df = LYTX_Vehicles_Breakdown_df[LYTX_Vehicles_Breakdown_df['Date'] == temp_date]
    temp_df = temp_df['Linehaul ERs'].values
    Contractor_overviewOfProgramPreformance_df.loc[index, 'Active ERs'] = temp_df
Contractor_overviewOfProgramPreformance_df['Frequency'] = Contractor_overviewOfProgramPreformance_df['Total'] / Contractor_overviewOfProgramPreformance_df['Active ERs']

# Region and Group Preformance
finalRGPreformance_df = pd.DataFrame()
lastThreeMonthYear = list(COV_df['Month-Year'].unique())[-3:]
rgPreformance_df_Final_index = 0
for _df_, str_df_ in zip([COV_df, Contractor_df, Linehaul_df], ['COV', 'Contractor', 'Linehaul']):
    rgPreformance_df = _df_[['Date', 'Week', 'Month-Year', 'Total']]
    for index, row in rgPreformance_df.iterrows():
        temp_date = rgPreformance_df.loc[index, "Month-Year"]
        temp_df = LYTX_Vehicles_Breakdown_df[LYTX_Vehicles_Breakdown_df['Date'] == temp_date]
        activeERs = temp_df[f'{str_df_} ERs'].values
        rgPreformance_df.loc[index, 'Active ERs'] = activeERs
    rgPreformance_df_Final = pd.DataFrame(
        index= [rgPreformance_df_Final_index], 
        data= {'Group Level': f'{str_df_}',
            'Active ERs': f"{int(activeERs)}",})
    
    for monthY in lastThreeMonthYear:
        temp_df = rgPreformance_df[rgPreformance_df['Month-Year'] == monthY]
        temp_finalNumber = sum(list(temp_df['Total'])) / mean(list(temp_df['Active ERs']))
        rgPreformance_df_Final[monthY] = round(temp_finalNumber, 2)
    rgPreformance_df_Final_index += 1
    
    finalRGPreformance_df = pd.concat([finalRGPreformance_df, rgPreformance_df_Final], axis=0)

# Apply color changing for table
finalRGPreformance_df_COLOR = pd.DataFrame(columns= finalRGPreformance_df.columns)
colors = n_colors('rgb(0, 255, 0)', 'rgb(255, 0, 0)', 9, colortype='rgb')
# Apply alternating row coloring to the first two columns
for i in range(len(finalRGPreformance_df)):
    if i % 2 == 0:
        finalRGPreformance_df_COLOR.loc[i, 'Group Level'] = 'white'
        finalRGPreformance_df_COLOR.loc[i, 'Active ERs'] = 'white'
    else:
        finalRGPreformance_df_COLOR.loc[i, 'Group Level'] = 'lightgrey'
        finalRGPreformance_df_COLOR.loc[i, 'Active ERs'] = 'lightgrey'
# Find the maximum and minimum values in the DataFrame (excluding the first two columns)
values_0 = list(finalRGPreformance_df.iloc[:, 2].values)
values_1 = list(finalRGPreformance_df.iloc[:, 3].values)
values_2 = list(finalRGPreformance_df.iloc[:, 4].values)
values = values_0 + values_1 + values_2
values.sort()
color_dic = {}
for val, color in zip(values, colors):
    color_dic[val] = color
# Apply conditional cell coloring to the last three columns
for i in range(len(finalRGPreformance_df)):
    for col in finalRGPreformance_df.columns[2:]:
        val = finalRGPreformance_df.loc[i, col]
        finalRGPreformance_df_COLOR.loc[i, col] = color_dic[val]
#################################################################################################
# WEEKLY Region and Group Preformance
WEEKLY_finalRGPreformance_df = pd.DataFrame()
lastTwelveWeeks = list(COV_df['Week'].unique())[-12:]
rgPreformance_df_Final_index = 0
for _df_, str_df_ in zip([COV_df, Contractor_df, Linehaul_df], ['COV', 'Contractor', 'Linehaul']):
    rgPreformance_df = _df_[['Date', 'Week', 'Month-Year', 'Total']]
    for index, row in rgPreformance_df.iterrows():
        temp_date = rgPreformance_df.loc[index, "Month-Year"]
        temp_df = LYTX_Vehicles_Breakdown_df[LYTX_Vehicles_Breakdown_df['Date'] == temp_date]
        activeERs = temp_df[f'{str_df_} ERs'].values
        rgPreformance_df.loc[index, 'Active ERs'] = activeERs
    rgPreformance_df_Final = pd.DataFrame(
        index= [rgPreformance_df_Final_index], 
        data= {'Group Level': f'{str_df_}',
            'Active ERs': f"{int(activeERs)}",})
    
    for monthY in lastTwelveWeeks:
        temp_df = rgPreformance_df[rgPreformance_df['Week'] == monthY]
        temp_finalNumber = sum(list(temp_df['Total'])) / mean(list(temp_df['Active ERs']))
        rgPreformance_df_Final[monthY] = round(temp_finalNumber, 2)
    rgPreformance_df_Final_index += 1
    
    WEEKLY_finalRGPreformance_df = pd.concat([WEEKLY_finalRGPreformance_df, rgPreformance_df_Final], axis=0)

# Apply color changing for table
WEEKLY_finalRGPreformance_df_COLOR = pd.DataFrame(columns= WEEKLY_finalRGPreformance_df.columns)
colors = n_colors('rgb(0, 255, 0)', 'rgb(255, 0, 0)', 36, colortype='rgb')
# Apply alternating row coloring to the first two columns
for i in range(len(WEEKLY_finalRGPreformance_df)):
    if i % 2 == 0:
        WEEKLY_finalRGPreformance_df_COLOR.loc[i, 'Group Level'] = 'white'
        WEEKLY_finalRGPreformance_df_COLOR.loc[i, 'Active ERs'] = 'white'
    else:
        WEEKLY_finalRGPreformance_df_COLOR.loc[i, 'Group Level'] = 'lightgrey'
        WEEKLY_finalRGPreformance_df_COLOR.loc[i, 'Active ERs'] = 'lightgrey'
# Find the maximum and minimum values in the DataFrame (excluding the first two columns)
values_0 = list(WEEKLY_finalRGPreformance_df.iloc[:, 2].values)
values_1 = list(WEEKLY_finalRGPreformance_df.iloc[:, 3].values)
values_2 = list(WEEKLY_finalRGPreformance_df.iloc[:, 4].values)
values_3 = list(WEEKLY_finalRGPreformance_df.iloc[:, 5].values)
values_4 = list(WEEKLY_finalRGPreformance_df.iloc[:, 6].values)
values_5 = list(WEEKLY_finalRGPreformance_df.iloc[:, 7].values)
values_6 = list(WEEKLY_finalRGPreformance_df.iloc[:, 8].values)
values_7 = list(WEEKLY_finalRGPreformance_df.iloc[:, 9].values)
values_8 = list(WEEKLY_finalRGPreformance_df.iloc[:, 10].values)
values_9 = list(WEEKLY_finalRGPreformance_df.iloc[:, 11].values)
values_10 = list(WEEKLY_finalRGPreformance_df.iloc[:, 12].values)
values_11 = list(WEEKLY_finalRGPreformance_df.iloc[:, 13].values)
values = values_0 + values_1 + values_2 + values_3 + values_4 + values_5 + values_6 + values_7 + values_8 + values_9 + values_10 + values_11
values.sort()
color_dic = {}
for val, color in zip(values, colors):
    color_dic[val] = color
# Apply conditional cell coloring to the last three columns
for i in range(len(WEEKLY_finalRGPreformance_df)):
    for col in WEEKLY_finalRGPreformance_df.columns[2:]:
        val = WEEKLY_finalRGPreformance_df.loc[i, col]
        WEEKLY_finalRGPreformance_df_COLOR.loc[i, col] = color_dic[val]
        
New_Weekly_Columns = [x.replace('-', ' - ') for x in list(WEEKLY_finalRGPreformance_df.columns)]
WEEKLY_finalRGPreformance_df.columns = New_Weekly_Columns


#############################################################################################################

temp_behaviors_df = Behaviors_df.iloc[-8:, :]
temp_behaviors_df = temp_behaviors_df.drop(['Month-Year', 'Date', 'Year', 'Total'], axis=1)
drop_list = []
for col in temp_behaviors_df.columns[1:]:
    temp_list = sum(list(temp_behaviors_df[col]))
    if temp_list == 0:
        drop_list.append(col)
        
temp_cov_df = COV_Behaviors_df.iloc[-8:, :]
temp_cov_df = temp_cov_df.drop(['Month-Year', 'Date', 'Year', 'Total'], axis=1)
temp_cov_df = temp_cov_df.drop(drop_list, axis=1)

temp_contractor_df = Contractor_Behaviors_df.iloc[-8:, :]
temp_contractor_df = temp_contractor_df.drop(['Month-Year', 'Date', 'Year', 'Total'], axis=1)
temp_contractor_df = temp_contractor_df.drop(drop_list, axis=1)

temp_linehaul_df = Linehaul_Behaviors_df.iloc[-8:, :]
temp_linehaul_df = temp_linehaul_df.drop(['Month-Year', 'Date', 'Year', 'Total'], axis=1)
temp_linehaul_df = temp_linehaul_df.drop(drop_list, axis=1)

len_cols = len(temp_cov_df.columns)

first_temp_cov_df = temp_cov_df.drop(temp_cov_df.columns[int(len_cols/2):], axis=1)
first_temp_contractor_df = temp_contractor_df.drop(temp_contractor_df.columns[int(len_cols/2):], axis=1)
first_temp_linehaul_df = temp_linehaul_df.drop(temp_linehaul_df.columns[int(len_cols/2):], axis=1)

second_temp_cov_df = temp_cov_df.drop(temp_cov_df.columns[1:-(int(len_cols/2))], axis=1)
second_temp_contractor_df = temp_contractor_df.drop(temp_contractor_df.columns[1:-(int(len_cols/2))], axis=1)
second_temp_linehaul_df = temp_linehaul_df.drop(temp_linehaul_df.columns[1:-(int(len_cols/2))], axis=1)





#############################################################################################################

# start chart construction
fig = make_subplots(
    rows=16, 
    cols=3, 
    start_cell="top-left",
    vertical_spacing= 0.01,
    horizontal_spacing= 0.03,
    row_heights=[3, 1.5, 4, 4, 0.15, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # Adjust these values as needed

    column_widths= [1, 1, 1],
    
    specs=[
        [{"colspan": 3, "rowspan": 1}, None, None],
        [{"colspan": 1, "rowspan": 1, 'type': 'table'}, {"colspan": 2, "rowspan": 1, 'type': 'table'}, None],
        [{"colspan": 3, "rowspan": 1, 'type': 'table'}, None, None],
        [{"colspan": 3, "rowspan": 1, 'type': 'table'}, None, None],
        [{}, {}, {}],
        [{"colspan": 1, "rowspan": 1}, {"colspan": 1, "rowspan": 1}, {"colspan": 1, "rowspan": 1}],
        [{"colspan": 1, "rowspan": 1}, {"colspan": 1, "rowspan": 1}, {"colspan": 1, "rowspan": 1}],
        [{"colspan": 1, "rowspan": 1}, {"colspan": 1, "rowspan": 1}, {"colspan": 1, "rowspan": 1}],
        [{"colspan": 1, "rowspan": 1}, {"colspan": 1, "rowspan": 1}, {"colspan": 1, "rowspan": 1}],
        [{"colspan": 1, "rowspan": 1}, {"colspan": 1, "rowspan": 1}, {"colspan": 1, "rowspan": 1}],
        [{"colspan": 1, "rowspan": 1}, {"colspan": 1, "rowspan": 1}, {"colspan": 1, "rowspan": 1}],
        [{"colspan": 1, "rowspan": 1}, {"colspan": 1, "rowspan": 1}, {"colspan": 1, "rowspan": 1}],
        [{"colspan": 1, "rowspan": 1}, {"colspan": 1, "rowspan": 1}, {"colspan": 1, "rowspan": 1}],
        [{"colspan": 1, "rowspan": 1}, {"colspan": 1, "rowspan": 1}, {"colspan": 1, "rowspan": 1}],
        [{"colspan": 1, "rowspan": 1}, {"colspan": 1, "rowspan": 1}, {"colspan": 1, "rowspan": 1}],
        [{"colspan": 1, "rowspan": 1}, {"colspan": 1, "rowspan": 1}, {"colspan": 1, "rowspan": 1}],
    ],
    subplot_titles=(
        "<span style='text-decoration: underline; font-weight: bold; color: black;'>Infraction Frequency per Category</span>",
        # "<span style='text-decoration: underline; font-weight: bold; color: black; '>Monthly Region and Group Performance</span>",
        # "<span style='text-decoration: underline; font-weight: bold; color: black; '>Weekly Region and Group Performance</span>",
        )
    )
###################################################################################################
row_num, col_num = 1, 1
for cat_df, cat_text in zip([COV_overviewOfProgramPreformance_df, Contractor_overviewOfProgramPreformance_df, Linehaul_overviewOfProgramPreformance_df], ['COV', 'Contractor', 'Linehaul']):
    fig.add_trace(go.Scatter(
        x= cat_df['Date'],
        y= cat_df['Frequency'],
        mode= 'lines+markers',
        name= f'{cat_text}',
        line=dict(color='green' if cat_text == 'COV' else 'blue' if cat_text == 'Contractor' else 'red'),  # Set the color of the line
        showlegend= True,
        ), row= row_num, col= col_num)
fig.update_xaxes(
    nticks= 20,
    showline=True, linewidth=2, linecolor='black', mirror=True, # Adds Lines around border of chart
    showgrid=True, gridwidth=1, gridcolor='lightgray', # Adds custom grid in chart
    
    row= row_num, col= col_num)
fig.update_yaxes(
    title_text= "Frequency Per Vehicle",
    showline=True, linewidth=2, linecolor='black', mirror=True, # Adds Lines around border of chart
    showgrid=True, gridwidth=1, gridcolor='lightgray', # Adds custom grid in chart
    
    row= row_num, col= col_num)

###################################################################################################

# Table: ROW 2, COL 1
row_num, col_num = 2, 1
cell_values = []
cell_headers = []
for cell_v in finalRGPreformance_df.columns:
    cell_values.append(finalRGPreformance_df[f"{cell_v}"])
    cell_headers.append(f"<b>{cell_v}</b>")
fig.add_trace(go.Table(
    header= dict(
        values= cell_headers,
        fill_color= 'lightgray',
        align= 'center',
        line_color='darkslategray',
        font= dict(color='black')
        ),
    cells= dict(
        values= cell_values, #[finalRGPreformance_df[col] for col in finalRGPreformance_df.columns],
        fill_color= [finalRGPreformance_df_COLOR[k].tolist() for k in finalRGPreformance_df_COLOR.columns],
        align= 'center',
        line_color='darkslategray',
        font= dict(color='black'),
        ),
), row= row_num, col= col_num)
fig.update_traces(domain_x=[0,0.30], domain_y=[0.75,0.865], selector=dict(type='table'), row= row_num, col= col_num)

fig.add_annotation(
    x=0.047,
    y=0.875,
    xref="paper",
    yref="paper",
    text="<span style='text-decoration: underline; font-weight: bold; '>Monthly Region and Group Performance</span>",
    showarrow=False,
    font=dict(size=16, color='black'),
    textangle= 0
)
###################################################################################################

# Table: ROW 2, COL 2
row_num, col_num = 2, 2
cell_values = []
cell_headers = []
for cell_v in WEEKLY_finalRGPreformance_df.columns:
    cell_values.append(WEEKLY_finalRGPreformance_df[f"{cell_v}"])
    cell_headers.append(f"<b>{cell_v}</b>")
fig.add_trace(go.Table(
    header= dict(
        values= cell_headers,
        fill_color= 'lightgray',
        align= 'center',
        line_color='darkslategray',
        font= dict(color='black')
        ),
    cells= dict(
        values= cell_values, #[finalRGPreformance_df[col] for col in finalRGPreformance_df.columns],
        fill_color= [WEEKLY_finalRGPreformance_df_COLOR[k].tolist() for k in WEEKLY_finalRGPreformance_df_COLOR.columns],
        align= 'center',
        line_color='darkslategray',
        font= dict(color='black'),
        ),
), row= row_num, col= col_num)
fig.update_traces(domain_x=[0.34, 1.00], domain_y=[0.75,0.865], selector=dict(type='table'), row= row_num, col= col_num)

fig.add_annotation(
    x=0.78,
    y=0.875,
    xref="paper",
    yref="paper",
    text="<span style='text-decoration: underline; font-weight: bold; '>Weekly Region and Group Performance</span>",
    showarrow=False,
    font=dict(size=16, color='black'),
    textangle= 0
)
###################################################################################################
fig.add_annotation(
    x=0.50,
    y=0.82,
    xref="paper",
    yref="paper",
    text="<span style='text-decoration: underline; font-weight: bold; '>Infractions Totals and per Category</span>",
    showarrow=False,
    font=dict(size=16, color='black'),
    textangle= 0
)

# Table: ROW 3, COL 1
row_num, col_num = 3, 1
cell_values = []
cell_headers = []
for cell_v in first_temp_cov_df.columns:
    if cell_v == 'Week':
        cell_values.append(first_temp_cov_df[f'{cell_v}'])
        cell_headers.append(f"<b>{cell_v}</b>")
    else:
        temp_cov = first_temp_cov_df[f'{cell_v}'].values
        temp_cov = [f"{str(x)} " for x in temp_cov]

        temp_contractor = first_temp_contractor_df[f'{cell_v}'].values
        temp_contractor = [f" {str(x)} " for x in temp_contractor]
        
        temp_linehaul = first_temp_linehaul_df[f'{cell_v}'].values
        temp_linehaul = [f" {str(x)}" for x in temp_linehaul]
        
        temp_all = []
        for i in range(len(temp_cov)):
            temp_total = int(temp_cov[i]) + int(temp_contractor[i]) + int(temp_linehaul[i])
            past_total = int(temp_cov[i-1]) + int(temp_contractor[i-1]) + int(temp_linehaul[i-1])
            
            try:
                if (past_total == 0) and (temp_total == 0):
                    total_diff = 0
                else:
                    total_diff = ((temp_total / past_total) - 1) * 100
            except ZeroDivisionError:
                total_diff = 100
            try:
                if (int(temp_cov[i-1]) == 0) and (int(temp_cov[i]) == 0):
                    cov_diff = 0
                else:
                    cov_diff = ((int(temp_cov[i]) / int(temp_cov[i-1])) - 1) * 100
            except ZeroDivisionError:
                cov_diff = 100
            try:
                if (int(temp_contractor[i-1]) == 0) and (int(temp_contractor[i]) == 0):
                    contractor_diff = 0
                else:
                    contractor_diff = ((int(temp_contractor[i]) / int(temp_contractor[i-1])) - 1) * 100
            except ZeroDivisionError:
                contractor_diff = 100
            try:
                if (int(temp_linehaul[i-1]) == 0) and (int(temp_linehaul[i]) == 0):
                    linehaul_diff = 0
                else:
                    linehaul_diff = ((int(temp_linehaul[i]) / int(temp_linehaul[i-1])) - 1) * 100
            except ZeroDivisionError:
                linehaul_diff = 100
            
            diff_dict = {}
            
            for key, key_text, temp_int in zip([total_diff, cov_diff, contractor_diff, linehaul_diff], ['Total', 'COV', 'Contractor', 'Linehaul'], [temp_total, temp_cov[i], temp_contractor[i], temp_linehaul[i]]):
                if key < -40.00:
                    diff_text = f"<span style='color: darkgreen; font-weight: bold;'>{temp_int}</span>"
                elif key < -20.00:
                    diff_text = f"<span style='color: green; font-weight: bold;'>{temp_int}</span>"
                elif key < -10.00:
                    diff_text = f"<span style='color: lightgreen; font-weight: bold;'>{temp_int}</span>"
                elif key > 40.00:
                    diff_text = f"<span style='color: darkred; font-weight: bold;'>{temp_int}</span>"
                elif key > 20.00:
                    diff_text = f"<span style='color: red; font-weight: bold;'>{temp_int}</span>"
                elif key > 10.00:
                    diff_text = f"<span style='color: lightcoral; font-weight: bold;'>{temp_int}</span>"
                else:
                    diff_text = f"{temp_int}"
                    
                diff_dict[key_text] = diff_text
                
            interal_temp_all = f"         {diff_dict['Total']}<br>{diff_dict['COV']} | {diff_dict['Contractor']} | {diff_dict['Linehaul']}"
            
            temp_all.append(interal_temp_all)
        
        cell_values.append(temp_all)
        cell_headers.append(f"<b>{cell_v}</b>")
        
fig.add_trace(go.Table(
    header= dict(
        values= cell_headers,
        fill_color= 'lightgray',
        align= 'center',
        line_color='darkslategray',
        font= dict(color='black')
        ),
    cells= dict(
        values= cell_values, #[finalRGPreformance_df[col] for col in finalRGPreformance_df.columns],
        fill_color= 'white', # [WEEKLY_finalRGPreformance_df_COLOR[k].tolist() for k in WEEKLY_finalRGPreformance_df_COLOR.columns],
        align= 'center',
        line_color='darkslategray',
        font= dict(color='black'),
        ),
), row= row_num, col= col_num)
fig.update_traces(domain_x=[0.0, 1.00], domain_y=[0.65,0.81], selector=dict(type='table'), row= row_num, col= col_num)

######################################################################################################

# Table: ROW 4, COL 1
row_num, col_num = 4, 1
cell_values = []
cell_headers = []
for cell_v in second_temp_cov_df.columns:
    if cell_v == 'Week':
        cell_values.append(second_temp_cov_df[f'{cell_v}'])
        cell_headers.append(f"<b>{cell_v}</b>")
    elif cell_v == 'Total Behaviors': # Numbers for Total Behaviors
        temp_cov = second_temp_cov_df[f'{cell_v}'].values
        temp_cov = [f"{str(x)}" for x in temp_cov]

        temp_contractor = second_temp_contractor_df[f'{cell_v}'].values
        temp_contractor = [f"{str(x)}" for x in temp_contractor]
        
        temp_linehaul = second_temp_linehaul_df[f'{cell_v}'].values
        temp_linehaul = [f"{str(x)}" for x in temp_linehaul]
        
        temp_all = []
        for i in range(len(temp_cov)):
            temp_total = int(temp_cov[i]) + int(temp_contractor[i]) + int(temp_linehaul[i])
            past_total = int(temp_cov[i-1]) + int(temp_contractor[i-1]) + int(temp_linehaul[i-1])
            
            try:
                if (past_total == 0) and (temp_total == 0):
                    total_diff = 0
                else:
                    total_diff = ((temp_total / past_total) - 1) * 100
            except ZeroDivisionError:
                total_diff = 100
            try:
                if (int(temp_cov[i-1]) == 0) and (int(temp_cov[i]) == 0):
                    cov_diff = 0
                else:
                    cov_diff = ((int(temp_cov[i]) / int(temp_cov[i-1])) - 1) * 100
            except ZeroDivisionError:
                cov_diff = 100
            try:
                if (int(temp_contractor[i-1]) == 0) and (int(temp_contractor[i]) == 0):
                    contractor_diff = 0
                else:
                    contractor_diff = ((int(temp_contractor[i]) / int(temp_contractor[i-1])) - 1) * 100
            except ZeroDivisionError:
                contractor_diff = 100
            try:
                if (int(temp_linehaul[i-1]) == 0) and (int(temp_linehaul[i]) == 0):
                    linehaul_diff = 0
                else:
                    linehaul_diff = ((int(temp_linehaul[i]) / int(temp_linehaul[i-1])) - 1) * 100
            except ZeroDivisionError:
                linehaul_diff = 100
            
            diff_dict = {}
            
            for key, key_text, temp_int in zip([total_diff, cov_diff, contractor_diff, linehaul_diff], ['Total', 'COV', 'Contractor', 'Linehaul'], [temp_total, temp_cov[i], temp_contractor[i], temp_linehaul[i]]):
                if key < -40.00:
                    diff_text = f"<span style='color: darkgreen; font-weight: bold;'>{temp_int}</span>"
                elif key < -20.00:
                    diff_text = f"<span style='color: green; font-weight: bold;'>{temp_int}</span>"
                elif key < -10.00:
                    diff_text = f"<span style='color: lightgreen; font-weight: bold;'>{temp_int}</span>"
                elif key > 40.00:
                    diff_text = f"<span style='color: darkred; font-weight: bold;'>{temp_int}</span>"
                elif key > 20.00:
                    diff_text = f"<span style='color: red; font-weight: bold;'>{temp_int}</span>"
                elif key > 10.00:
                    diff_text = f"<span style='color: lightcoral; font-weight: bold;'>{temp_int}</span>"
                else:
                    diff_text = f"{temp_int}"
                    
                diff_dict[key_text] = diff_text
                
            interal_temp_all = f"         {diff_dict['Total']}<br>{diff_dict['COV']} | {diff_dict['Contractor']} | {diff_dict['Linehaul']}"
            
            temp_all.append(interal_temp_all)
        
        cell_values.append(temp_all)
        cell_headers.append(f"<b>{cell_v}</b>")
    else: # Numbers for All Behaviors
        temp_cov = second_temp_cov_df[f'{cell_v}'].values
        temp_cov = [f"{str(x)} " for x in temp_cov]

        temp_contractor = second_temp_contractor_df[f'{cell_v}'].values
        temp_contractor = [f" {str(x)} " for x in temp_contractor]
        
        temp_linehaul = second_temp_linehaul_df[f'{cell_v}'].values
        temp_linehaul = [f" {str(x)}" for x in temp_linehaul]
        
        temp_all = []
        for i in range(len(temp_cov)):
            temp_total = int(temp_cov[i]) + int(temp_contractor[i]) + int(temp_linehaul[i])
            past_total = int(temp_cov[i-1]) + int(temp_contractor[i-1]) + int(temp_linehaul[i-1])
            
            try:
                if (past_total == 0) and (temp_total == 0):
                    total_diff = 0
                else:
                    total_diff = ((temp_total / past_total) - 1) * 100
            except ZeroDivisionError:
                total_diff = 100
            try:
                if (int(temp_cov[i-1]) == 0) and (int(temp_cov[i]) == 0):
                    cov_diff = 0
                else:
                    cov_diff = ((int(temp_cov[i]) / int(temp_cov[i-1])) - 1) * 100
            except ZeroDivisionError:
                cov_diff = 100
            try:
                if (int(temp_contractor[i-1]) == 0) and (int(temp_contractor[i]) == 0):
                    contractor_diff = 0
                else:
                    contractor_diff = ((int(temp_contractor[i]) / int(temp_contractor[i-1])) - 1) * 100
            except ZeroDivisionError:
                contractor_diff = 100
            try:
                if (int(temp_linehaul[i-1]) == 0) and (int(temp_linehaul[i]) == 0):
                    linehaul_diff = 0
                else:
                    linehaul_diff = ((int(temp_linehaul[i]) / int(temp_linehaul[i-1])) - 1) * 100
            except ZeroDivisionError:
                linehaul_diff = 100
            
            diff_dict = {}
            
            for key, key_text, temp_int in zip([total_diff, cov_diff, contractor_diff, linehaul_diff], ['Total', 'COV', 'Contractor', 'Linehaul'], [temp_total, temp_cov[i], temp_contractor[i], temp_linehaul[i]]):
                if key < -40.00:
                    diff_text = f"<span style='color: darkgreen; font-weight: bold;'>{temp_int}</span>"
                elif key < -20.00:
                    diff_text = f"<span style='color: green; font-weight: bold;'>{temp_int}</span>"
                elif key < -10.00:
                    diff_text = f"<span style='color: lightgreen; font-weight: bold;'>{temp_int}</span>"
                elif key > 40.00:
                    diff_text = f"<span style='color: darkred; font-weight: bold;'>{temp_int}</span>"
                elif key > 20.00:
                    diff_text = f"<span style='color: red; font-weight: bold;'>{temp_int}</span>"
                elif key > 10.00:
                    diff_text = f"<span style='color: lightcoral; font-weight: bold;'>{temp_int}</span>"
                else:
                    diff_text = f"{temp_int}"
                    
                diff_dict[key_text] = diff_text
                
            interal_temp_all = f"         {diff_dict['Total']}<br>{diff_dict['COV']} | {diff_dict['Contractor']} | {diff_dict['Linehaul']}"
            
            temp_all.append(interal_temp_all)
        
        cell_values.append(temp_all)
        cell_headers.append(f"<b>{cell_v}</b>")
fig.add_trace(go.Table(
    header= dict(
        values= cell_headers,
        fill_color= 'lightgray',
        align= 'center',
        line_color='darkslategray',
        font= dict(color='black')
        ),
    cells= dict(
        values= cell_values, #[finalRGPreformance_df[col] for col in finalRGPreformance_df.columns],
        fill_color= 'white', # [WEEKLY_finalRGPreformance_df_COLOR[k].tolist() for k in WEEKLY_finalRGPreformance_df_COLOR.columns],
        align= 'center',
        line_color='darkslategray',
        font= dict(color='black'),
        ),
), row= row_num, col= col_num)
fig.update_traces(domain_x=[0.0, 1.00], domain_y=[0.515,0.666], selector=dict(type='table'), row= row_num, col= col_num)

######################################################################################################

row_num, col_num = 5, 1

fig.add_annotation(
    x=0.50,
    y=0.505,
    xref="paper",
    yref="paper",
    text= f"Infraction Frequency per Behavior",
    showarrow=False,
    font=dict(size=30, color='black'),
    textangle= 0
)

fig.add_annotation(
    x=1.00,
    y=0.82,
    xref="paper",
    yref="paper",
    text= f"Legend: COV | Contractor | Linehaul",
    showarrow=False,
    font=dict(size=15, color='black'),
    textangle= 0,
    bordercolor="black",
    borderwidth=2,
    borderpad=4
)

###################################################################################################

row_num, col_num = 6, 1

temp_df = Behaviors_df.iloc[how_many_rows:, :]
temp_df = temp_df.transpose()
temp_df = temp_df.iloc[4:-2, :]
temp_df['Totals'] = temp_df.sum(axis=1)
temp_df['Totals'] = temp_df['Totals'].astype(int)
temp_df = temp_df[temp_df['Totals'] >= 10]
temp_df = temp_df.sort_values('Totals', ascending=False)
sorted_behaviors = list(temp_df.index)

for col in sorted_behaviors:
    
    total_cov = COV_Behaviors_df[col].sum()
    total_contractor = Contractor_Behaviors_df[col].sum()
    total_linehaul = Linehaul_Behaviors_df[col].sum()
    
    for cat_df, cat_text in zip([COV_Behaviors_df, Contractor_Behaviors_df, Linehaul_Behaviors_df], ['COV', 'Contractor', 'Linehaul']):

        fig.add_trace(go.Scatter(
            x= cat_df['Date'],
            y= cat_df[f'{col}'],
            mode= 'lines+markers',
            name= f'{cat_text}',
            line=dict(color='green' if cat_text == 'COV' else 'blue' if cat_text == 'Contractor' else 'red'),  # Set the color of the line
            showlegend= False,
            ), row= row_num, col= col_num)
        
    fig.update_xaxes(
        showticklabels = False,
        nticks= 20,
        showline=True, linewidth=2, linecolor='black', mirror=True, # Adds Lines around border of chart
        showgrid=True, gridwidth=1, gridcolor='lightgray', # Adds custom grid in chart
        
        row= row_num, col= col_num)
    if col_num == 1:
        fig.update_yaxes(
            title_text= "Total Infractions",
            showline=True, linewidth=2, linecolor='black', mirror=True, # Adds Lines around border of chart
            showgrid=True, gridwidth=1, gridcolor='lightgray', # Adds custom grid in chart
            
            row= row_num, col= col_num)
    else:
        fig.update_yaxes(
            title_text= "",
            showline=True, linewidth=2, linecolor='black', mirror=True, # Adds Lines around border of chart
            showgrid=True, gridwidth=1, gridcolor='lightgray', # Adds custom grid in chart
            
            row= row_num, col= col_num)

    fig.add_annotation(
        xref="x domain", yref="y domain",
        x=0.0, y=1.0,
        text= f"{col}",
        showarrow=False,
        font=dict(
            size=12,
            color="black"
        ),
        align="center",
        bordercolor="black",
        borderwidth=1,
        borderpad=2,
        bgcolor="white",
        opacity=0.9,
        row= row_num, col= col_num
    )
    
    fig.add_annotation(
        xref="x domain", yref="y domain",
        x=0.0, y=0.0,
        text= f"COV: {total_cov}<br>Contractor: {total_contractor}<br>Linehaul: {total_linehaul}",
        showarrow=False,
        font=dict(
            size=12,
            color="black"
        ),
        align="left",
        bordercolor="black",
        borderwidth=1,
        borderpad=2,
        bgcolor="white",
        opacity=0.9,
        row= row_num, col= col_num
    )
    
    col_num += 1
    
    if col_num == 4:
        row_num += 1
        col_num = 1
        
###################################################################################################


fig.update_layout(
    # showlegend=False,
    height= 3200,
    width=1850,
    title_text=f"<span style='font-size: 24px; font-weight: bold; color: black;'>LYTX Categorical Results Week: {Behaviors_df.loc[len(Behaviors_df)-1, 'Week']} {Behaviors_df.loc[len(Behaviors_df)-1, 'Year']}</span>",
)

fig.show()

# save_week = Behaviors_df.loc[len(Behaviors_df)-1, 'Week']
# save_year = Behaviors_df.loc[len(Behaviors_df)-1, 'Year']
# fig.write_html(f'LYTX_Categorical_Results_Chart\\{save_year} {save_week} category.html')

