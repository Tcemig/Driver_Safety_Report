import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.colors import n_colors
from statistics import mean
import datetime as dt

safety_monitoring_df = pd.read_csv('Main_CSV_Files\\Safety_Monitoring.csv')
Contractor_df = pd.read_csv('Main_CSV_Files\\Contractor_df.csv')
Linehaul_df = pd.read_csv('Main_CSV_Files\\Linehaul_df.csv')
COV_df = pd.read_csv('Main_CSV_Files\\COV_df.csv')
Behaviors_df = pd.read_csv('Main_CSV_Files\\Behaviors_df.csv')
Behaviors_Totals_df = pd.read_csv('Main_CSV_Files\\Behaviors_Totals_df.csv')
NearCollisions_df = pd.read_csv('Main_CSV_Files\\NearCollision_df.csv')
NearCollision_Totals_df = pd.read_csv('Main_CSV_Files\\NearCollision_Totals_df.csv')
LYTX_Vehicles_Breakdown_df = pd.read_csv('Main_CSV_Files\\LYTX_Vehicles_BreakDown_df.csv')



drop_behaviors_list = [
    'Food or Drink',
    'Other Concern',
    'Driver Smoking',
    'Driver Tagged',
    'Following Distance: > 1 sec to < 2 sec',
    'Incomplete Stop',
    'Failed to Stop',
    'No Seat Belt',
    
    ]
NonPriority_Be_Totals_df = Behaviors_df
Behaviors_df = Behaviors_df.drop(drop_behaviors_list, axis=1)

# Overview of Program Preformance
overviewOfProgramPreformance_df = Behaviors_df[['Date', 'Week', 'Year', 'Total']] # Behaviors']]
overviewOfProgramPreformance_df['Active ERs'] = 0
for index, row in overviewOfProgramPreformance_df.iterrows():
    temp_date = overviewOfProgramPreformance_df.loc[index, "Date"][:10]
    temp_df = safety_monitoring_df[safety_monitoring_df['Week Starting'] == temp_date]
    temp_df = temp_df['Total Units #'].values
    overviewOfProgramPreformance_df.loc[index, 'Active ERs'] = temp_df
overviewOfProgramPreformance_df['Frequency'] = overviewOfProgramPreformance_df['Total'] / overviewOfProgramPreformance_df['Active ERs']


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
        
        
# COV Events % Incidents - Monthly
lastSixMonthYear = list(COV_df['Month-Year'].unique())[-5:]
SM_df = safety_monitoring_df
SM_df['Month-Year'] = ""
for index, row in SM_df.iterrows():
    SM_df.loc[index, "Month-Year"] = dt.datetime.strftime((dt.datetime.strptime(SM_df.loc[index, 'Week Starting'], "%Y-%m-%d")), "%m-%Y")
finalCovEI = pd.DataFrame(
    index= [0, 1, 2, 3, 4],
    data={
        'Month - Year': lastSixMonthYear,
        'Avg Total Units #': 0,
        'Avg Drivers w/ Events': 0,
        'Total Coachable Events': 0,
        'Total VI At Fault': 0,
        'Total VI No Fault': 0,
        'Total VI Shared Fault': 0,
        'Total Vehicle Incidents': 0,
})

SM_columns = ['Month - Year'] + list(SM_df.columns[3:9]) + ['Total Vehicle Incidents']
fCov_columns = list(finalCovEI.columns)
for index, row in finalCovEI.iterrows():
    temp_month = finalCovEI.loc[index, 'Month - Year']
    for SM_col, fCov_col in zip(SM_columns, fCov_columns):
        
        if (SM_col in SM_columns[1:3]):
            temp_df = SM_df[SM_df["Month-Year"] == temp_month]
            temp_df = temp_df.reset_index(drop=True)
            temp_df = list(temp_df[SM_col])
            temp_df = round(mean(temp_df), 0)
            finalCovEI.loc[index, fCov_col] = temp_df
        elif (SM_col in SM_columns[3:7]):
            temp_df = SM_df[SM_df["Month-Year"] == temp_month]
            temp_df = temp_df.reset_index(drop=True)
            temp_df = list(temp_df[SM_col])
            temp_df = sum(temp_df)
            finalCovEI.loc[index, fCov_col] = temp_df
        elif (SM_col == "Total Vehicle Incidents"):
            temp_df = SM_df[SM_df["Month-Year"] == temp_month]
            temp_df = temp_df.reset_index(drop=True)
            temp_df = finalCovEI.loc[index, "Total VI At Fault"] + finalCovEI.loc[index, "Total VI No Fault"] + finalCovEI.loc[index, "Total VI Shared Fault"]
            finalCovEI.loc[index, fCov_col] = temp_df

# Apply color change to table
table_col_list = list(finalCovEI.columns)[4:]
finalCovEI_Color = pd.DataFrame(
    index, finalCovEI.index, columns= finalCovEI.columns)
for index, row in finalCovEI.iterrows():
    for col in finalCovEI.columns:
        if index % 2 == 0:
            finalCovEI_Color.loc[index, col] = 'White'
        else:
            finalCovEI_Color.loc[index, col] = 'lightgray'
        if (col in table_col_list) & (index != 0):
            temp_diff = ((finalCovEI.loc[index, col] / finalCovEI.loc[index-1, col]) -1) *100
            if temp_diff < -40.0:
                finalCovEI_Color.loc[index, col] = 'rgb(42, 192, 0)'
            elif temp_diff < -20.0:
                finalCovEI_Color.loc[index, col] = 'rgb(67, 250, 11)'
            elif temp_diff < -10.0:
                finalCovEI_Color.loc[index, col] = 'rgb(142, 255, 107)'
            elif temp_diff > 40.0:
                finalCovEI_Color.loc[index, col] = 'rgb(189, 3, 3)'
            elif temp_diff > 20.0:
                finalCovEI_Color.loc[index, col] = 'rgb(255, 3, 3)'
            elif temp_diff > 10.0:
                finalCovEI_Color.loc[index, col] = 'rgb(255, 113, 113)'
                
# COV Events % Incidents - Weekly
lastFourWeeks = list(COV_df['Week'].unique())[-4:]
SM_Weekly_df = safety_monitoring_df
finalCovEI_Weekly = pd.DataFrame(
    index= [0, 1, 2, 3],
    data={
        'Week': lastFourWeeks,
        'Avg Total Units #': 0,
        'Avg Drivers w/ Events': 0,
        'Total Coachable Events': 0,
        'Total VI At Fault': 0,
        'Total VI No Fault': 0,
        'Total VI Shared Fault': 0,
        'Total Vehicle Incidents': 0,
})

SM_columns = ['Week'] + list(SM_Weekly_df.columns[3:9]) + ['Total Vehicle Incidents']
fCov_columns = list(finalCovEI_Weekly.columns)
for index, row in finalCovEI_Weekly.iterrows():
    temp_month = finalCovEI_Weekly.loc[index, 'Week']
    for SM_col, fCov_col in zip(SM_columns, fCov_columns):
        
        if (SM_col in SM_columns[1:3]):
            temp_df = SM_Weekly_df[SM_Weekly_df["Week Period"] == temp_month]
            temp_df = temp_df.reset_index(drop=True)
            temp_df = list(temp_df[SM_col])
            temp_df = round(mean(temp_df), 0)
            finalCovEI_Weekly.loc[index, fCov_col] = temp_df
        elif (SM_col in SM_columns[3:7]):
            temp_df = SM_Weekly_df[SM_Weekly_df["Week Period"] == temp_month]
            temp_df = temp_df.reset_index(drop=True)
            temp_df = list(temp_df[SM_col])
            temp_df = sum(temp_df)
            finalCovEI_Weekly.loc[index, fCov_col] = temp_df
        elif (SM_col == "Total Vehicle Incidents"):
            temp_df = SM_Weekly_df[SM_Weekly_df["Week Period"] == temp_month]
            temp_df = temp_df.reset_index(drop=True)
            temp_df = finalCovEI_Weekly.loc[index, "Total VI At Fault"] + finalCovEI_Weekly.loc[index, "Total VI No Fault"] + finalCovEI_Weekly.loc[index, "Total VI Shared Fault"]
            finalCovEI_Weekly.loc[index, fCov_col] = temp_df

# Apply color change to table
table_col_list = list(finalCovEI_Weekly.columns)[4:]
finalCovEI_Color_Weekly = pd.DataFrame(
    index, finalCovEI_Weekly.index, columns= finalCovEI_Weekly.columns)
for index, row in finalCovEI_Weekly.iterrows():
    for col in finalCovEI_Weekly.columns:
        if index % 2 == 0:
            finalCovEI_Color_Weekly.loc[index, col] = 'White'
        else:
            finalCovEI_Color_Weekly.loc[index, col] = 'lightgray'
        if (col in table_col_list) & (index != 0):
            temp_diff = ((finalCovEI_Weekly.loc[index, col] / finalCovEI_Weekly.loc[index-1, col]) -1) *100
            if temp_diff < -40.0:
                finalCovEI_Color_Weekly.loc[index, col] = 'rgb(42, 192, 0)'
            elif temp_diff < -20.0:
                finalCovEI_Color_Weekly.loc[index, col] = 'rgb(67, 250, 11)'
            elif temp_diff < -10.0:
                finalCovEI_Color_Weekly.loc[index, col] = 'rgb(142, 255, 107)'
            elif temp_diff > 40.0:
                finalCovEI_Color_Weekly.loc[index, col] = 'rgb(189, 3, 3)'
            elif temp_diff > 20.0:
                finalCovEI_Color_Weekly.loc[index, col] = 'rgb(255, 3, 3)'
            elif temp_diff > 10.0:
                finalCovEI_Color_Weekly.loc[index, col] = 'rgb(255, 113, 113)'

# Near Collisions
nearCollisionsBar_df = NearCollisions_df.iloc[-12:, :]
nearCollisionsBar_df = nearCollisionsBar_df[['Date', 'Week', 'Total Behaviors']]
nearCollisionsBar_df['Month-Year'] = ''
for index, row in nearCollisionsBar_df.iterrows():
    nearCollisionsBar_df.loc[index, 'Month-Year'] = nearCollisionsBar_df.loc[index, 'Date'][5:7] + "-" + nearCollisionsBar_df.loc[index, 'Date'][:4]

    temp_date = nearCollisionsBar_df.loc[index, "Date"][:10]
    temp_df = safety_monitoring_df[safety_monitoring_df['Week Starting'] == temp_date]
    temp_df = temp_df['Total Units #'].values
    nearCollisionsBar_df.loc[index, 'Active ERs'] = temp_df
nearCollisionsBar_df['Frequency'] = nearCollisionsBar_df['Total Behaviors'] / nearCollisionsBar_df['Active ERs']



# Near Collisions Totals
# NearCollision_Totals_df = NearCollision_Totals_df.sort_values("Frequency", ascending=True)

NearCollision_Totals_df = NearCollisions_df.iloc[-12:, :]
NearCollision_Totals_df = NearCollision_Totals_df.drop([
    'Date', 'Week', 'Year', 'Total Behaviors', 
    # 'Other Concern', 'Following Distance: > 1 sec to < 2 sec', 'Incomplete Stop',
    ], axis=1)
NearCollision_Totals_df = NearCollision_Totals_df.reset_index(drop=True)
sum_list = []
for col in NearCollision_Totals_df.columns:
    sum_list.append(NearCollision_Totals_df[col].sum())
NearCollision_Totals_df.loc[len(NearCollision_Totals_df)] = sum_list
NearCollision_Totals_df = NearCollision_Totals_df.iloc[-1:, :]

NearCollision_Totals_df = NearCollision_Totals_df.transpose()
NearCollision_Totals_df = NearCollision_Totals_df.rename(columns={NearCollision_Totals_df.columns[0]: "Frequency"})
NearCollision_Totals_df = NearCollision_Totals_df.sort_values("Frequency", ascending=True)

for index, row in NearCollision_Totals_df.iterrows():
    if NearCollision_Totals_df.loc[index, 'Frequency'] <= 5:
        NearCollision_Totals_df = NearCollision_Totals_df.drop(index)
        
# NearCollision_Totals_df = NearCollision_Totals_df.reset_index(drop=True)

# Past Near Collision Totals
PastNearCollision_Totals_df = NearCollisions_df.iloc[-24:-12, :]
PastNearCollision_Totals_df = PastNearCollision_Totals_df.drop([
    'Date', 'Week', 'Year', 'Total Behaviors', 
    ], axis=1)
PastNearCollision_Totals_df = PastNearCollision_Totals_df.reset_index(drop=True)
sum_list = []
for col in PastNearCollision_Totals_df.columns:
    sum_list.append(PastNearCollision_Totals_df[col].sum())
PastNearCollision_Totals_df.loc[len(PastNearCollision_Totals_df)] = sum_list
PastNearCollision_Totals_df = PastNearCollision_Totals_df.iloc[-1:, :]

PastNearCollision_Totals_df = PastNearCollision_Totals_df.transpose()
PastNearCollision_Totals_df = PastNearCollision_Totals_df.rename(columns={PastNearCollision_Totals_df.columns[0]: "Frequency"})
PastNearCollision_Totals_df = PastNearCollision_Totals_df.sort_values("Frequency", ascending=True)

for index, row in PastNearCollision_Totals_df.iterrows():
    if PastNearCollision_Totals_df.loc[index, 'Frequency'] <= 5:
        PastNearCollision_Totals_df = PastNearCollision_Totals_df.drop(index)

# Making Percentage Difference 12 Week Near Collision Behavior Sum
NearCollision_Totals_df['Percentage Diff'] = 'N/A'
NearCollision_Totals_df_textColors = []
NearCollision_Totals_df_text = []
for index, row in NearCollision_Totals_df.iterrows():
    current_Behavior = index
    current_Behavior_Num = int(NearCollision_Totals_df.loc[index, 'Frequency'])
    past_Behavior_Num = PastNearCollision_Totals_df.loc[current_Behavior, 'Frequency']
    percent_diff_num = 'N/A'
    try:
        past_Behavior_Num = int(past_Behavior_Num)
        percent_diff_num = round(((current_Behavior_Num/past_Behavior_Num)-1)*100, 2)
        NearCollision_Totals_df.loc[index, 'Percentage Diff'] = percent_diff_num
        NearCollision_Totals_df_text.append(f"{percent_diff_num}%")
        if percent_diff_num > 0:
            NearCollision_Totals_df_textColors.append('red')
        elif percent_diff_num < 0:
            NearCollision_Totals_df_textColors.append('green')
        else:
            NearCollision_Totals_df_textColors.append('black')
    except TypeError:
        NearCollision_Totals_df_textColors.append('black')
        NearCollision_Totals_df_text.append("N/A")  


# Behavior Totals 
Behaviors_Totals_df = Behaviors_df.iloc[-12:, :]
Behaviors_Totals_df = Behaviors_Totals_df.drop(['Month-Year', 'Date', 'Week', 'Year', 'Total', 'Total Behaviors'], axis=1)
Behaviors_Totals_df = Behaviors_Totals_df.reset_index(drop=True)
sum_list = []
for col in Behaviors_Totals_df.columns:
    sum_list.append(Behaviors_Totals_df[col].sum())
Behaviors_Totals_df.loc[len(Behaviors_Totals_df)] = sum_list
Behaviors_Totals_df = Behaviors_Totals_df.iloc[-1:, :]

Behaviors_Totals_df = Behaviors_Totals_df.transpose()
Behaviors_Totals_df = Behaviors_Totals_df.rename(columns={Behaviors_Totals_df.columns[0]: "Frequency"})
Behaviors_Totals_df = Behaviors_Totals_df.sort_values("Frequency", ascending=False)

for index, row in Behaviors_Totals_df.iterrows():
    if Behaviors_Totals_df.loc[index, 'Frequency'] <= 5:
        Behaviors_Totals_df = Behaviors_Totals_df.drop(index)

# Past Behavior Totals 
Past_Behaviors_Totals_df = Behaviors_df.iloc[-24:-12, :]
Past_Behaviors_Totals_df = Past_Behaviors_Totals_df.drop(['Month-Year', 'Date', 'Week', 'Year', 'Total', 'Total Behaviors'], axis=1)
Past_Behaviors_Totals_df = Past_Behaviors_Totals_df.reset_index(drop=True)
sum_list = []
for col in Past_Behaviors_Totals_df.columns:
    sum_list.append(Past_Behaviors_Totals_df[col].sum())
Past_Behaviors_Totals_df.loc[len(Past_Behaviors_Totals_df)] = sum_list
Past_Behaviors_Totals_df = Past_Behaviors_Totals_df.iloc[-1:, :]

Past_Behaviors_Totals_df = Past_Behaviors_Totals_df.transpose()
Past_Behaviors_Totals_df = Past_Behaviors_Totals_df.rename(columns={Past_Behaviors_Totals_df.columns[0]: "Frequency"})
Past_Behaviors_Totals_df = Past_Behaviors_Totals_df.sort_values("Frequency", ascending=False)

for index, row in Past_Behaviors_Totals_df.iterrows():
    if Past_Behaviors_Totals_df.loc[index, 'Frequency'] <= 5:
        Past_Behaviors_Totals_df = Past_Behaviors_Totals_df.drop(index)

# Making Percentage Difference 12 Week Behavior Sum
Behaviors_Totals_df['Percentage Diff'] = 'N/A'
Behaviors_Totals_df_textColors = []
Behaviors_Totals_df_text = []
for index, row in Behaviors_Totals_df.iterrows():
    current_Behavior = index
    current_Behavior_Num = int(Behaviors_Totals_df.loc[index, 'Frequency'])
    try:
        past_Behavior_Num = Past_Behaviors_Totals_df.loc[current_Behavior, 'Frequency']
        percent_diff_num = 'N/A'
        try:
            past_Behavior_Num = int(past_Behavior_Num)
            percent_diff_num = round(((current_Behavior_Num/past_Behavior_Num)-1)*100, 2)
            Behaviors_Totals_df.loc[index, 'Percentage Diff'] = percent_diff_num
            Behaviors_Totals_df_text.append(f"{percent_diff_num}%")
            if percent_diff_num > 0:
                Behaviors_Totals_df_textColors.append('red')
            elif percent_diff_num < 0:
                Behaviors_Totals_df_textColors.append('green')
            else:
                Behaviors_Totals_df_textColors.append('black')
        except TypeError:
            Behaviors_Totals_df_textColors.append('black')
            Behaviors_Totals_df_text.append("N/A")
    except KeyError:
        Behaviors_Totals_df_textColors.append('black')
        Behaviors_Totals_df_text.append("N/A")

# Current Week Behavior Profile
currentWeekBP_df = Behaviors_df.iloc[-1, :]
currentWeekBP_df = currentWeekBP_df.reset_index(drop=False)
currentWeekBP_df = currentWeekBP_df.transpose()
new_header = currentWeekBP_df.iloc[0]
currentWeekBP_df.columns = new_header
currentWeekBP_df = currentWeekBP_df.reset_index(drop=True)
currentWeekBP_df = currentWeekBP_df.drop(['Month-Year', 'Date', 'Week', 'Year', 'Total', 'Total Behaviors'], axis=1)
for index, row in currentWeekBP_df.iterrows():
    for col in currentWeekBP_df.columns:
        try:
            if currentWeekBP_df.loc[index, col] <= 5:
                currentWeekBP_df = currentWeekBP_df.drop(col, axis=1)
        except TypeError:
            pass
currentWeekBP_df = currentWeekBP_df.transpose()
currentWeekBP_df = currentWeekBP_df.sort_values(1, ascending=True)

# Past Week Behavior Profile
pastWeekBP_df = Behaviors_df.iloc[-2, :]
pastWeekBP_df = pastWeekBP_df.reset_index(drop=False)
pastWeekBP_df = pastWeekBP_df.transpose()
new_header = pastWeekBP_df.iloc[0]
pastWeekBP_df.columns = new_header
pastWeekBP_df = pastWeekBP_df.reset_index(drop=True)
pastWeekBP_df = pastWeekBP_df.drop(['Month-Year', 'Date', 'Week', 'Year', 'Total', 'Total Behaviors'], axis=1)
for index, row in pastWeekBP_df.iterrows():
    for col in pastWeekBP_df.columns:
        try:
            if pastWeekBP_df.loc[index, col] <= 5:
                pastWeekBP_df = pastWeekBP_df.drop(col, axis=1)
        except TypeError:
            pass
pastWeekBP_df = pastWeekBP_df.transpose()
pastWeekBP_df = pastWeekBP_df.sort_values(1, ascending=True)

# Past Two Week Behavior Profile
pastTwoWeekBP_df = Behaviors_df.iloc[-3, :]
pastTwoWeekBP_df = pastTwoWeekBP_df.reset_index(drop=False)
pastTwoWeekBP_df = pastTwoWeekBP_df.transpose()
new_header = pastTwoWeekBP_df.iloc[0]
pastTwoWeekBP_df.columns = new_header
pastTwoWeekBP_df = pastTwoWeekBP_df.reset_index(drop=True)
pastTwoWeekBP_df = pastTwoWeekBP_df.drop(['Month-Year', 'Date', 'Week', 'Year', 'Total', 'Total Behaviors'], axis=1)
for index, row in pastTwoWeekBP_df.iterrows():
    for col in pastTwoWeekBP_df.columns:
        try:
            if pastTwoWeekBP_df.loc[index, col] <= 5:
                pastTwoWeekBP_df = pastTwoWeekBP_df.drop(col, axis=1)
        except TypeError:
            pass
pastTwoWeekBP_df = pastTwoWeekBP_df.transpose()
pastTwoWeekBP_df = pastTwoWeekBP_df.sort_values(1, ascending=True)

# Past Three Week Behavior Profile
pastThreeWeekBP_df = Behaviors_df.iloc[-4, :]
pastThreeWeekBP_df = pastThreeWeekBP_df.reset_index(drop=False)
pastThreeWeekBP_df = pastThreeWeekBP_df.transpose()
new_header = pastThreeWeekBP_df.iloc[0]
pastThreeWeekBP_df.columns = new_header
pastThreeWeekBP_df = pastThreeWeekBP_df.reset_index(drop=True)
pastThreeWeekBP_df = pastThreeWeekBP_df.drop(['Month-Year', 'Date', 'Week', 'Year', 'Total', 'Total Behaviors'], axis=1)
for index, row in pastThreeWeekBP_df.iterrows():
    for col in pastThreeWeekBP_df.columns:
        try:
            if pastThreeWeekBP_df.loc[index, col] <= 5:
                pastThreeWeekBP_df = pastThreeWeekBP_df.drop(col, axis=1)
        except TypeError:
            pass
pastThreeWeekBP_df = pastThreeWeekBP_df.transpose()
pastThreeWeekBP_df = pastThreeWeekBP_df.sort_values(1, ascending=True)

# Making Percentage Difference Week Behaviors
currentWeekBP_df['Percentage Diff'] = 'N/A'
currentWeekBP_textColors = []
currentWeekBP_text = []
for index, row in currentWeekBP_df.iterrows():
    current_Behavior = currentWeekBP_df.loc[index, 0]
    current_Behavior_Num = int(currentWeekBP_df.loc[index, 1])
    past_Behavior_Num = pastWeekBP_df[pastWeekBP_df[0] == current_Behavior]
    percent_diff_num = 'N/A'
    try:
        past_Behavior_Num = int(past_Behavior_Num[1])
        percent_diff_num = round(((current_Behavior_Num/past_Behavior_Num)-1)*100, 2)
        currentWeekBP_df.loc[index, 'Percentage Diff'] = percent_diff_num
        currentWeekBP_text.append(f"{percent_diff_num}%")
        if percent_diff_num > 0:
            currentWeekBP_textColors.append('red')
        elif percent_diff_num < 0:
            currentWeekBP_textColors.append('green')
        else:
            currentWeekBP_textColors.append('black')
    except TypeError:
        currentWeekBP_textColors.append('black')
        currentWeekBP_text.append("N/A")

pastWeekBP_df['Percentage Diff'] = 'N/A'
pastWeekBP_textColors = []
pastWeekBP_text = []
for index, row in pastWeekBP_df.iterrows():
    current_Behavior = pastWeekBP_df.loc[index, 0]
    current_Behavior_Num = int(pastWeekBP_df.loc[index, 1])
    past_Behavior_Num = pastTwoWeekBP_df[pastTwoWeekBP_df[0] == current_Behavior]
    percent_diff_num = 'N/A'
    try:
        past_Behavior_Num = int(past_Behavior_Num[1])
        percent_diff_num = round(((current_Behavior_Num/past_Behavior_Num)-1)*100, 2)
        pastWeekBP_df.loc[index, 'Percentage Diff'] = percent_diff_num
        pastWeekBP_text.append(f"{percent_diff_num}%")
        if percent_diff_num > 0:
            pastWeekBP_textColors.append('red')
        elif percent_diff_num < 0:
            pastWeekBP_textColors.append('green')
        else:
            pastWeekBP_textColors.append('black')
    except TypeError:
        pastWeekBP_textColors.append('black')
        pastWeekBP_text.append("N/A")
        
pastTwoWeekBP_df['Percentage Diff'] = 'N/A'
pastTwoWeekBP_textColors = []
pastTwoWeekBP_text = []
for index, row in pastTwoWeekBP_df.iterrows():
    current_Behavior = pastTwoWeekBP_df.loc[index, 0]
    current_Behavior_Num = int(pastTwoWeekBP_df.loc[index, 1])
    past_Behavior_Num = pastThreeWeekBP_df[pastThreeWeekBP_df[0] == current_Behavior]
    percent_diff_num = 'N/A'
    try:
        past_Behavior_Num = int(past_Behavior_Num[1])
        percent_diff_num = round(((current_Behavior_Num/past_Behavior_Num)-1)*100, 2)
        pastTwoWeekBP_df.loc[index, 'Percentage Diff'] = percent_diff_num
        pastTwoWeekBP_text.append(f"{percent_diff_num}%")
        if percent_diff_num > 0:
            pastTwoWeekBP_textColors.append('red')
        elif percent_diff_num < 0:
            pastTwoWeekBP_textColors.append('green')
        else:
            pastTwoWeekBP_textColors.append('black')
    except TypeError:
        pastTwoWeekBP_textColors.append('black')
        pastTwoWeekBP_text.append('N/A')


# Behavior Trends
Trends_list = list(currentWeekBP_df.iloc[-6:, 0])
Trends_list = Trends_list[::-1]

behavior1_df = Behaviors_df[['Date', 'Week', Trends_list[0]]]
behavior1_df = behavior1_df.iloc[-12:, :]
behavior1_df = behavior1_df.reset_index(drop=True)

behavior2_df = Behaviors_df[['Date', 'Week', Trends_list[1]]]
behavior2_df = behavior2_df.iloc[-12:, :]
behavior2_df = behavior2_df.reset_index(drop=True)

behavior3_df = Behaviors_df[['Date', 'Week', Trends_list[2]]]
behavior3_df = behavior3_df.iloc[-12:, :]
behavior3_df = behavior3_df.reset_index(drop=True)

behavior4_df = Behaviors_df[['Date', 'Week', Trends_list[3]]]
behavior4_df = behavior4_df.iloc[-12:, :]
behavior4_df = behavior4_df.reset_index(drop=True)

behavior5_df = Behaviors_df[['Date', 'Week', Trends_list[4]]]
behavior5_df = behavior5_df.iloc[-12:, :]
behavior5_df = behavior5_df.reset_index(drop=True)

behavior6_df = Behaviors_df[['Date', 'Week', Trends_list[5]]]
behavior6_df = behavior6_df.iloc[-12:, :]
behavior6_df = behavior6_df.reset_index(drop=True)


Past_NonPriority_Be_Totals_df = NonPriority_Be_Totals_df.iloc[-24:-12, :]
# Non-Priority Behavior Profile: Sum 12 Weeks
# Behavior Totals 
NonPriority_Be_Totals_df = NonPriority_Be_Totals_df.iloc[-12:, :]
NonPriority_Behaviors_df = NonPriority_Be_Totals_df
NonPriority_Be_Totals_df = NonPriority_Be_Totals_df.drop(['Month-Year', 'Date', 'Week', 'Year', 'Total', 'Total Behaviors'], axis=1)
NonPriority_Be_Totals_df = NonPriority_Be_Totals_df[drop_behaviors_list]
NonPriority_Be_Totals_df = NonPriority_Be_Totals_df.reset_index(drop=True)
sum_list = []
for col in NonPriority_Be_Totals_df.columns:
    sum_list.append(NonPriority_Be_Totals_df[col].sum())
NonPriority_Be_Totals_df.loc[len(NonPriority_Be_Totals_df)] = sum_list
NonPriority_Be_Totals_df = NonPriority_Be_Totals_df.iloc[-1:, :]

NonPriority_Be_Totals_df = NonPriority_Be_Totals_df.transpose()
NonPriority_Be_Totals_df = NonPriority_Be_Totals_df.rename(columns={NonPriority_Be_Totals_df.columns[0]: "Frequency"})
NonPriority_Be_Totals_df = NonPriority_Be_Totals_df.sort_values("Frequency", ascending=False)

for index, row in NonPriority_Be_Totals_df.iterrows():
    if NonPriority_Be_Totals_df.loc[index, 'Frequency'] <= 5:
        NonPriority_Be_Totals_df = NonPriority_Be_Totals_df.drop(index)
        
# Past Non-Priority Behavior Totals
Past_NonPriority_Be_Totals_df = Past_NonPriority_Be_Totals_df.drop(['Month-Year', 'Date', 'Week', 'Year', 'Total', 'Total Behaviors'], axis=1)
Past_NonPriority_Be_Totals_df = Past_NonPriority_Be_Totals_df[drop_behaviors_list]
Past_NonPriority_Be_Totals_df = Past_NonPriority_Be_Totals_df.reset_index(drop=True)
sum_list = []
for col in Past_NonPriority_Be_Totals_df.columns:
    sum_list.append(Past_NonPriority_Be_Totals_df[col].sum())
Past_NonPriority_Be_Totals_df.loc[len(Past_NonPriority_Be_Totals_df)] = sum_list
Past_NonPriority_Be_Totals_df = Past_NonPriority_Be_Totals_df.iloc[-1:, :]

Past_NonPriority_Be_Totals_df = Past_NonPriority_Be_Totals_df.transpose()
Past_NonPriority_Be_Totals_df = Past_NonPriority_Be_Totals_df.rename(columns={Past_NonPriority_Be_Totals_df.columns[0]: "Frequency"})
Past_NonPriority_Be_Totals_df = Past_NonPriority_Be_Totals_df.sort_values("Frequency", ascending=False)

for index, row in Past_NonPriority_Be_Totals_df.iterrows():
    if Past_NonPriority_Be_Totals_df.loc[index, 'Frequency'] <= 5:
        Past_NonPriority_Be_Totals_df = Past_NonPriority_Be_Totals_df.drop(index)
        
# Making Percentage Difference 12 Week Non-Priority Behavior Sum
NonPriority_Be_Totals_df['Percentage Diff'] = 'N/A'
NonPriority_Be_Totals_df_textColors = []
NonPriority_Be_Totals_df_text = []
for index, row in NonPriority_Be_Totals_df.iterrows():
    current_Behavior = index
    current_Behavior_Num = int(NonPriority_Be_Totals_df.loc[index, 'Frequency'])
    try:
        past_Behavior_Num = Past_NonPriority_Be_Totals_df.loc[current_Behavior, 'Frequency']
        percent_diff_num = 'N/A'
        try:
            past_Behavior_Num = int(past_Behavior_Num)
            percent_diff_num = round(((current_Behavior_Num/past_Behavior_Num)-1)*100, 2)
            NonPriority_Be_Totals_df.loc[index, 'Percentage Diff'] = percent_diff_num
            NonPriority_Be_Totals_df_text.append(f"{percent_diff_num}%")
            if percent_diff_num > 0:
                NonPriority_Be_Totals_df_textColors.append('red')
            elif percent_diff_num < 0:
                NonPriority_Be_Totals_df_textColors.append('green')
            else:
                NonPriority_Be_Totals_df_textColors.append('black')
        except TypeError:
            NonPriority_Be_Totals_df_textColors.append('black')
            NonPriority_Be_Totals_df_text.append("N/A")
    except KeyError:
        NonPriority_Be_Totals_df_textColors.append('black')
        NonPriority_Be_Totals_df_text.append("N/A")

# Current Week Non-Priority Behavior Profile
currentWeekNonBP_df = NonPriority_Behaviors_df.iloc[-1, :]
currentWeekNonBP_df = currentWeekNonBP_df.reset_index(drop=False)
currentWeekNonBP_df = currentWeekNonBP_df.transpose()
new_header = currentWeekNonBP_df.iloc[0]
currentWeekNonBP_df.columns = new_header
currentWeekNonBP_df = currentWeekNonBP_df.reset_index(drop=True)
currentWeekNonBP_df = currentWeekNonBP_df.drop(['Month-Year', 'Date', 'Week', 'Year', 'Total', 'Total Behaviors'], axis=1)
currentWeekNonBP_df = currentWeekNonBP_df[drop_behaviors_list]
currentWeekNonBP_df = currentWeekNonBP_df.transpose()
currentWeekNonBP_df = currentWeekNonBP_df.sort_values(1, ascending=True)

# Past Week Non-Priority Behavior Profile
pastWeekNonBP_df = NonPriority_Behaviors_df.iloc[-2, :]
pastWeekNonBP_df = pastWeekNonBP_df.reset_index(drop=False)
pastWeekNonBP_df = pastWeekNonBP_df.transpose()
new_header = pastWeekNonBP_df.iloc[0]
pastWeekNonBP_df.columns = new_header
pastWeekNonBP_df = pastWeekNonBP_df.reset_index(drop=True)
pastWeekNonBP_df = pastWeekNonBP_df.drop(['Month-Year', 'Date', 'Week', 'Year', 'Total', 'Total Behaviors'], axis=1)
pastWeekNonBP_df = pastWeekNonBP_df[drop_behaviors_list]
pastWeekNonBP_df = pastWeekNonBP_df.transpose()
pastWeekNonBP_df = pastWeekNonBP_df.sort_values(1, ascending=True)

# Past Two Week Non-Priority Behavior Profile
pastTwoWeekNonBP_df = NonPriority_Behaviors_df.iloc[-3, :]
pastTwoWeekNonBP_df = pastTwoWeekNonBP_df.reset_index(drop=False)
pastTwoWeekNonBP_df = pastTwoWeekNonBP_df.transpose()
new_header = pastTwoWeekNonBP_df.iloc[0]
pastTwoWeekNonBP_df.columns = new_header
pastTwoWeekNonBP_df = pastTwoWeekNonBP_df.reset_index(drop=True)
pastTwoWeekNonBP_df = pastTwoWeekNonBP_df.drop(['Month-Year', 'Date', 'Week', 'Year', 'Total', 'Total Behaviors'], axis=1)
pastTwoWeekNonBP_df = pastTwoWeekNonBP_df[drop_behaviors_list]
pastTwoWeekNonBP_df = pastTwoWeekNonBP_df.transpose()
pastTwoWeekNonBP_df = pastTwoWeekNonBP_df.sort_values(1, ascending=True)

# Past Three Week Non-Priority Behavior Profile
pastThreeWeekNonBP_df = NonPriority_Behaviors_df.iloc[-4, :]
pastThreeWeekNonBP_df = pastThreeWeekNonBP_df.reset_index(drop=False)
pastThreeWeekNonBP_df = pastThreeWeekNonBP_df.transpose()
new_header = pastThreeWeekNonBP_df.iloc[0]
pastThreeWeekNonBP_df.columns = new_header
pastThreeWeekNonBP_df = pastThreeWeekNonBP_df.reset_index(drop=True)
pastThreeWeekNonBP_df = pastThreeWeekNonBP_df.drop(['Month-Year', 'Date', 'Week', 'Year', 'Total', 'Total Behaviors'], axis=1)
pastThreeWeekNonBP_df = pastThreeWeekNonBP_df[drop_behaviors_list]
pastThreeWeekNonBP_df = pastThreeWeekNonBP_df.transpose()
pastThreeWeekNonBP_df = pastThreeWeekNonBP_df.sort_values(1, ascending=True)

# Making Percentage Difference Week Behaviors
currentWeekNonBP_df['Percentage Diff'] = 'N/A'
currentWeekNonBP_textColors = []
currentWeekNonBP_text = []
for index, row in currentWeekNonBP_df.iterrows():
    current_Behavior = currentWeekNonBP_df.loc[index, 0]
    current_Behavior_Num = int(currentWeekNonBP_df.loc[index, 1])
    past_Behavior_Num = pastWeekNonBP_df[pastWeekNonBP_df[0] == current_Behavior]
    percent_diff_num = 'N/A'
    try:
        past_Behavior_Num = int(past_Behavior_Num[1])
        percent_diff_num = round(((current_Behavior_Num/past_Behavior_Num)-1)*100, 2)
        currentWeekNonBP_df.loc[index, 'Percentage Diff'] = percent_diff_num
        currentWeekNonBP_text.append(f"{percent_diff_num}%")
        if percent_diff_num > 0:
            currentWeekNonBP_textColors.append('red')
        elif percent_diff_num < 0:
            currentWeekNonBP_textColors.append('green')
        else:
            currentWeekNonBP_textColors.append('black')
    except TypeError:
        currentWeekNonBP_textColors.append('black')
        currentWeekNonBP_text.append("N/A")
    except ZeroDivisionError:
        currentWeekNonBP_textColors.append('black')
        currentWeekNonBP_text.append("N/A")

pastWeekNonBP_df['Percentage Diff'] = 'N/A'
pastWeekNonBP_textColors = []
pastWeekNonBP_text = []
for index, row in pastWeekNonBP_df.iterrows():
    current_Behavior = pastWeekNonBP_df.loc[index, 0]
    current_Behavior_Num = int(pastWeekNonBP_df.loc[index, 1])
    past_Behavior_Num = pastTwoWeekNonBP_df[pastTwoWeekNonBP_df[0] == current_Behavior]
    percent_diff_num = 'N/A'
    try:
        past_Behavior_Num = int(past_Behavior_Num[1])
        percent_diff_num = round(((current_Behavior_Num/past_Behavior_Num)-1)*100, 2)
        pastWeekNonBP_df.loc[index, 'Percentage Diff'] = percent_diff_num
        pastWeekNonBP_text.append(f"{percent_diff_num}%")
        if percent_diff_num > 0:
            pastWeekNonBP_textColors.append('red')
        elif percent_diff_num < 0:
            pastWeekNonBP_textColors.append('green')
        else:
            pastWeekNonBP_textColors.append('black')
    except TypeError:
        pastWeekNonBP_textColors.append('black')
        pastWeekNonBP_text.append("N/A")
    except ZeroDivisionError:
        pastWeekNonBP_textColors.append('black')
        pastWeekNonBP_text.append("N/A")
        
pastTwoWeekNonBP_df['Percentage Diff'] = 'N/A'
pastTwoWeekNonBP_textColors = []
pastTwoWeekNonBP_text = []
for index, row in pastTwoWeekNonBP_df.iterrows():
    current_Behavior = pastTwoWeekNonBP_df.loc[index, 0]
    current_Behavior_Num = int(pastTwoWeekNonBP_df.loc[index, 1])
    past_Behavior_Num = pastThreeWeekNonBP_df[pastThreeWeekNonBP_df[0] == current_Behavior]
    percent_diff_num = 'N/A'
    try:
        past_Behavior_Num = int(past_Behavior_Num[1])
        percent_diff_num = round(((current_Behavior_Num/past_Behavior_Num)-1)*100, 2)
        pastTwoWeekNonBP_df.loc[index, 'Percentage Diff'] = percent_diff_num
        pastTwoWeekNonBP_text.append(f"{percent_diff_num}%")
        if percent_diff_num > 0:
            pastTwoWeekNonBP_textColors.append('red')
        elif percent_diff_num < 0:
            pastTwoWeekNonBP_textColors.append('green')
        else:
            pastTwoWeekNonBP_textColors.append('black')
    except TypeError:
        pastTwoWeekNonBP_textColors.append('black')
        pastTwoWeekNonBP_text.append('N/A')
    except ZeroDivisionError:
        pastTwoWeekNonBP_textColors.append('black')
        pastTwoWeekNonBP_text.append('N/A')

# start chart construction
fig = make_subplots(
    rows=13, 
    cols=3, 
    start_cell="top-left",
    vertical_spacing= 0.04,
    horizontal_spacing= 0.06,
    column_widths= [1, 1, 1],
    
    specs=[
        [{"colspan": 3, "rowspan": 2}, None, None],
        [None, None, None],
        [{"colspan": 3}, None, None],
        [{"colspan": 1, 'type': 'table', "rowspan": 1}, {"colspan": 1, "type": 'table', "rowspan": 1}, {"colspan": 1, "type": 'table', "rowspan": 1}],
        [{"colspan": 1}, {"colspan": 2}, None],
        [{"rowspan": 3, "colspan": 1}, {"colspan": 2}, None],
        [None, {"colspan": 2}, None],
        [None, {"colspan": 2}, None],
        [{}, {}, {}],
        [{}, {}, {}],
        [{"rowspan": 3, "colspan": 1}, {"colspan": 2}, None],
        [None, {"colspan": 2}, None],
        [None, {"colspan": 2}, None],
    ],
    subplot_titles=(
        "<span style='text-decoration: underline; font-weight: bold; color: black;'>Overview of Program Performance - Frequency</span>",
        "",
        "<span style='text-decoration: underline; font-weight: bold; color: black;'>Region and Group Performance</span>",
        "<span style='text-decoration: underline; font-weight: bold; color: black;'>COV Events & Incidents Monthly</span>",
        "<span style='text-decoration: underline; font-weight: bold; color: black;'>COV Events & Incidents Weekly</span>",
        "<span style='text-decoration: underline; font-weight: bold; color: black;'>Near Collisions - Trend</span>",
        "<span style='text-decoration: underline; font-weight: bold; color: black;'>Near Collisions - Behaviors - Past 12 Weeks</span>",
        "<span style='text-decoration: underline; font-weight: bold; color: black;'>Behavior Profile: Sum 12 Weeks</span>",         
        f"<span style='text-decoration: underline; font-weight: bold; color: black;'>{Behaviors_df.loc[len(Behaviors_df)-3, 'Week']} Behavior Profile</span>",
        f"<span style='text-decoration: underline; font-weight: bold; color: black;'>{Behaviors_df.loc[len(Behaviors_df)-2, 'Week']} Behavior Profile</span>",
        f"<span style='text-decoration: underline; font-weight: bold; color: black;'>{Behaviors_df.loc[len(Behaviors_df)-1, 'Week']} Behavior Profile</span>",
        f"<span style='text-decoration: underline; font-weight: bold; color: black;'>{Trends_list[0]} Trend</span>",
        f"<span style='text-decoration: underline; font-weight: bold; color: black;'>{Trends_list[1]} Trend</span>",
        f"<span style='text-decoration: underline; font-weight: bold; color: black;'>{Trends_list[2]} Trend</span>",
        f"<span style='text-decoration: underline; font-weight: bold; color: black;'>{Trends_list[3]} Trend</span>",
        f"<span style='text-decoration: underline; font-weight: bold; color: black;'>{Trends_list[4]} Trend</span>",
        f"<span style='text-decoration: underline; font-weight: bold; color: black;'>{Trends_list[5]} Trend</span>",
        f"<span style='text-decoration: underline; font-weight: bold; color: black;'>Non-Priority Behavior Profile: Sum 12 Weeks</span>",
        f"<span style='text-decoration: underline; font-weight: bold; color: black;'>{Behaviors_df.loc[len(Behaviors_df)-3, 'Week']} Non-Priority Behavior Profile</span>",
        f"<span style='text-decoration: underline; font-weight: bold; color: black;'>{Behaviors_df.loc[len(Behaviors_df)-2, 'Week']} Non-Priority Behavior Profile</span>",
        f"<span style='text-decoration: underline; font-weight: bold; color: black;'>{Behaviors_df.loc[len(Behaviors_df)-1, 'Week']} Non-Priority Behavior Profile</span>",
        
        )
    )

# Chart: ROW 1, COL 1
row_num, col_num = 1, 1
fig.add_trace(go.Scatter(
    x= overviewOfProgramPreformance_df['Date'],
    y= overviewOfProgramPreformance_df['Frequency'],
    mode= 'lines+markers',
    name= 'Frequency Scored Events',
    ), row= row_num, col= col_num)
fig.update_xaxes(
    showticklabels = False,
    nticks= 20,
    showline=True, linewidth=2, linecolor='black', mirror=True, # Adds Lines around border of chart
    showgrid=True, gridwidth=1, gridcolor='lightgray', # Adds custom grid in chart
    
    row= row_num, col= col_num)
fig.update_yaxes(
    title_text= "Frequency Per Vehicle",
    showline=True, linewidth=2, linecolor='black', mirror=True, # Adds Lines around border of chart
    showgrid=True, gridwidth=1, gridcolor='lightgray', # Adds custom grid in chart
    
    row= row_num, col= col_num)

slope, intercept = np.polyfit(overviewOfProgramPreformance_df.index, overviewOfProgramPreformance_df['Frequency'], 1)
line_of_best_fit = slope * np.array(overviewOfProgramPreformance_df.index) + intercept
fig.add_trace(go.Scatter(
    x= overviewOfProgramPreformance_df['Date'],
    y= line_of_best_fit,
    mode= 'lines',
    name= 'Line of Best Fit',
    line= dict(color='black'),
    ), row= row_num, col= col_num)

start_date = dt.datetime.strptime(overviewOfProgramPreformance_df.loc[0, 'Date'][:10], "%Y-%m-%d")
end_date = dt.datetime.strptime(overviewOfProgramPreformance_df.loc[len(overviewOfProgramPreformance_df)-1, 'Date'][:10], "%Y-%m-%d")
month_Diff = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
line_of_best_fit_Diff = round(((list(line_of_best_fit)[-1] / list(line_of_best_fit)[0]) -1) *100, 2)
if line_of_best_fit_Diff > 0:
    annotation_text = f"Behavior frequency per vehicles has increased <span style='color: red;'>{line_of_best_fit_Diff}%</span> on average over the past {month_Diff} months."
else:
    annotation_text = f"Behavior frequency per vehicles has decreased <span style='color: green;'>{line_of_best_fit_Diff}%</span> on average over the past {month_Diff} months."
fig.add_annotation(
    xref="x domain", yref="y",
    x=0.0, y=2.0,
    text= annotation_text,
    showarrow=False,
    font=dict(
        size=16,
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


# Chart: ROW 3, COL 1
row_num, col_num = 3, 1
fig.add_trace(go.Scatter(
    x= overviewOfProgramPreformance_df['Date'],
    y= overviewOfProgramPreformance_df['Active ERs'],
    mode= 'lines+markers',
    name= 'Active ERs',
    ), row= row_num, col= col_num)
fig.update_xaxes(
    title_text= "Month/Year",
    nticks= 20,
    showline=True, linewidth=2, linecolor='black', mirror=True, # Adds Lines around border of chart
    showgrid=True, gridwidth=1, gridcolor='lightgray', # Adds custom grid in chart
    
    row= row_num, col= col_num)
fig.update_yaxes(
    title_text= "Active ERs",
    showline=True, linewidth=2, linecolor='black', mirror=True, # Adds Lines around border of chart
    showgrid=True, gridwidth=1, gridcolor='lightgray', # Adds custom grid in chart
    
    row= row_num, col= col_num)

# Table: ROW 4, COL 1
row_num, col_num = 4, 1
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
fig.update_traces(domain_x=[0,0.30], domain_y=[0.70,0.758], selector=dict(type='table'), row= row_num, col= col_num)

# Table: ROW 4, COL 2
row_num, col_num = 4, 2
cell_values_2 = []
cell_headers_2 = []
for cell_v in finalCovEI.columns:
    cell_values_2.append(finalCovEI[f"{cell_v}"])
    cell_headers_2.append(f"<b>{cell_v}</b>")
fig.add_trace(go.Table(
    header= dict(
        values= cell_headers_2,
        fill_color= 'lightgray',
        align= 'center',
        line_color='darkslategray',
        font= dict(color='black', size=10)
        ),
    cells= dict(
        values= cell_values_2, 
        fill_color= [finalCovEI_Color[k].tolist() for k in finalCovEI_Color.columns],
        align= 'center',
        line_color='darkslategray',
        font= dict(color='black'),
        ),
), row= row_num, col= col_num)
fig.update_traces(domain_x=[0.31,0.66], domain_y=[0.69,0.758], selector=dict(type='table'), row= row_num, col= col_num)

# Table: ROW 4, COL 3
row_num, col_num = 4, 3
cell_values_2 = []
cell_headers_2 = []
for cell_v in finalCovEI_Weekly.columns:
    cell_values_2.append(finalCovEI_Weekly[f"{cell_v}"])
    cell_headers_2.append(f"<b>{cell_v}</b>")
fig.add_trace(go.Table(
    header= dict(
        values= cell_headers_2,
        fill_color= 'lightgray',
        align= 'center',
        line_color='darkslategray',
        font= dict(color='black', size=10)
        ),
    cells= dict(
        values= cell_values_2, 
        fill_color= [finalCovEI_Color_Weekly[k].tolist() for k in finalCovEI_Color_Weekly.columns],
        align= 'center',
        line_color='darkslategray',
        font= dict(color='black'),
        ),
    columnwidth= [120, 100, 100, 100, 100, 100, 100, 100],
), row= row_num, col= col_num)
fig.update_traces(domain_x=[0.67,1.0], domain_y=[0.69,0.758], selector=dict(type='table'), row= row_num, col= col_num)


# Chart: ROW 5, COL 1
row_num, col_num = 5, 1
fig.add_trace(go.Bar(
    x= nearCollisionsBar_df['Week'],
    y= nearCollisionsBar_df['Frequency'],
    name= '',
    ), row= row_num, col= col_num)
fig.update_xaxes(
    title_text= "Weeks",
    showline=True, linewidth=2, linecolor='black', mirror=True, # Adds Lines around border of chart
    showgrid=True, gridwidth=1, gridcolor='lightgray', # Adds custom grid in chart
    
    row= row_num, col= col_num)
fig.update_yaxes(
    title_text= "Behavior / Active ERs",
    showline=True, linewidth=2, linecolor='black', mirror=True, # Adds Lines around border of chart
    showgrid=True, gridwidth=1, gridcolor='lightgray', # Adds custom grid in chart
    
    row= row_num, col= col_num)

# Calculate linear regression line
slope, intercept = np.polyfit(nearCollisionsBar_df.index, nearCollisionsBar_df['Frequency'], 1)
line_of_best_fit = slope * np.array(nearCollisionsBar_df.index) + intercept
fig.add_trace(go.Scatter(
    x= nearCollisionsBar_df['Week'],
    y= line_of_best_fit,
    mode= 'lines',
    name= 'Line of Best Fit',
    line= dict(color='black'),
    ), row= row_num, col= col_num)

fig.add_annotation(
    xref="x domain", yref="y",
    x=0.0, y=0.20,
    text= "Near Collisions frequency per vehicles has",
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

line_of_best_fit_Diff = round(((list(line_of_best_fit)[-1] / list(line_of_best_fit)[0]) -1) *100, 2)
if line_of_best_fit_Diff > 0:
    annotation_text = f"increased <span style='color: red;'>{line_of_best_fit_Diff}%</span> on average over the past 12 weeks."
else:
    annotation_text = f"decreased <span style='color: green;'>{line_of_best_fit_Diff}%</span> on average over the past 12 weeks."
fig.add_annotation(
    xref="x domain", yref="y",
    x=0.0, y=0.05,
    text= annotation_text,
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

# Chart: ROW 5, COL 2
row_num, col_num = 5, 2
fig.add_trace(go.Bar(
    x= NearCollision_Totals_df['Frequency'],
    y= NearCollision_Totals_df.index,
    name= '',
    orientation='h',
    text= NearCollision_Totals_df_text,
    textfont= dict(color=NearCollision_Totals_df_textColors),
    ), row= row_num, col= col_num)
fig.update_traces(
    textposition= 'outside',
    row= row_num, col= col_num)
fig.update_xaxes(
    # title_text= "",
    showline=True, linewidth=2, linecolor='black', mirror=True, # Adds Lines around border of chart
    showgrid=True, gridwidth=1, gridcolor='lightgray', # Adds custom grid in chart
    
    row= row_num, col= col_num)
fig.update_yaxes(
    title_text= "",
    showline=True, linewidth=2, linecolor='black', mirror=True, # Adds Lines around border of chart
    showgrid=True, gridwidth=1, gridcolor='lightgray', # Adds custom grid in chart
    
    row= row_num, col= col_num)

fig.add_annotation(
    x=1.015,
    y=0.675,
    xref="paper",
    yref="paper",
    text="Coachable Behaviors",
    showarrow=False,
    font=dict(size=14, color='black'),
    textangle= -90
)

# Chart: ROW 6, COL 1
row_num, col_num = 6, 1
fig.add_trace(go.Bar(
    x= Behaviors_Totals_df.index,
    y= Behaviors_Totals_df['Frequency'],
    name= '',
    ), row= row_num, col= col_num)
fig.update_traces(
    textposition= 'auto',
    textangle= 270,
    row= row_num, col= col_num)
fig.update_xaxes(
    showline=True, linewidth=2, linecolor='black', mirror=True,
    showgrid=True, gridwidth=1, gridcolor='lightgray',
    
    row= row_num, col= col_num)
fig.update_yaxes(
    title_text= "Count",
    showline=True, linewidth=2, linecolor='black', mirror=True, 
    showgrid=True, gridwidth=1, gridcolor='lightgray',
    
    row= row_num, col= col_num)

for i, txt in enumerate(Behaviors_Totals_df_text):
    fig.add_annotation(
        x=Behaviors_Totals_df.index[i],
        y=Behaviors_Totals_df['Frequency'][i] + 135,
        text=txt,
        showarrow=False,
        textangle= 270,
        font=dict(
            size=11,
            color=Behaviors_Totals_df_textColors[i]
        ), row= row_num, col= col_num
    )

# Chart: ROW 8, COL 2
row_num, col_num = 8, 2
fig.add_trace(go.Bar(
    x= currentWeekBP_df[1],
    y= currentWeekBP_df[0],
    name= '',
    orientation='h',
    text= currentWeekBP_text,
    textfont= dict(color=currentWeekBP_textColors),
    ), row= row_num, col= col_num)
fig.update_traces(
    textposition= 'outside',
    row= row_num, col= col_num)
fig.update_xaxes(
    showline=True, linewidth=2, linecolor='black', mirror=True,
    showgrid=True, gridwidth=1, gridcolor='lightgray',
    
    row= row_num, col= col_num)
fig.update_yaxes(
    title_text= "",
    showline=True, linewidth=2, linecolor='black', mirror=True,
    showgrid=True, gridwidth=1, gridcolor='lightgray',
    tickfont=dict(size=9),
    
    row= row_num, col= col_num)

fig.add_annotation(
    x=1.015,
    y=0.57,
    xref="paper",
    yref="paper",
    text="Coachable Behaviors",
    showarrow=False,
    font=dict(size=14, color='black'),
    textangle= -90
)

# Chart: ROW 7, COL 2
row_num, col_num = 7, 2
fig.add_trace(go.Bar(
    x= pastWeekBP_df[1],
    y= pastWeekBP_df[0],
    name= '',
    orientation='h',
    text= pastWeekBP_text,
    textfont= dict(color= pastWeekBP_textColors),
    ), row= row_num, col= col_num)
fig.update_traces(
    textposition= 'outside',
    row= row_num, col= col_num)
fig.update_xaxes(
    showline=True, linewidth=2, linecolor='black', mirror=True,
    showgrid=True, gridwidth=1, gridcolor='lightgray',
    
    row= row_num, col= col_num)
fig.update_yaxes(
    title_text= "",
    showline=True, linewidth=2, linecolor='black', mirror=True,
    showgrid=True, gridwidth=1, gridcolor='lightgray',
    tickfont=dict(size=10),
    
    row= row_num, col= col_num)

fig.add_annotation(
    x=1.015,
    y=0.49,
    xref="paper",
    yref="paper",
    text="Coachable Behaviors",
    showarrow=False,
    font=dict(size=14, color='black'),
    textangle= -90
)

# Chart: ROW 6, COL 2
row_num, col_num = 6, 2
fig.add_trace(go.Bar(
    x= pastTwoWeekBP_df[1],
    y= pastTwoWeekBP_df[0],
    name= '',
    orientation='h',
    text= pastTwoWeekBP_text,
    textfont= dict(color= pastTwoWeekBP_textColors),
    ), row= row_num, col= col_num)
fig.update_traces(
    textposition= 'outside',
    row= row_num, col= col_num)
fig.update_xaxes(
    showline=True, linewidth=2, linecolor='black', mirror=True,
    showgrid=True, gridwidth=1, gridcolor='lightgray',
    
    row= row_num, col= col_num)
fig.update_yaxes(
    title_text= "",
    showline=True, linewidth=2, linecolor='black', mirror=True,
    showgrid=True, gridwidth=1, gridcolor='lightgray',
    
    row= row_num, col= col_num)

fig.add_annotation(
    x=1.015,
    y=0.415,
    xref="paper",
    yref="paper",
    text="Coachable Behaviors",
    showarrow=False,
    font=dict(size=14, color='black'),
    textangle= -90
)

fig.add_annotation(
    xref="x domain", yref="y",
    x=1.0, y=0.25,
    text="% = previous weeks behavior / current weeks behavior",
    showarrow=False,
    font=dict(
        size=14,
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

# Chart: ROW 9-10, COL 1-3
row_num, col_num = 9, 1
for beh_df in [behavior1_df, behavior2_df, behavior3_df, behavior4_df, behavior5_df, behavior6_df]:
    
    if col_num == 4:
        row_num, col_num = 10, 1

    fig.add_trace(go.Bar(
        x= beh_df['Week'],
        y= beh_df.iloc[:, -1],
        name= '',
        ), row= row_num, col= col_num)
    fig.update_xaxes(
        title_text= "",
        showline=True, linewidth=2, linecolor='black', mirror=True,
        showgrid=True, gridwidth=1, gridcolor='lightgray',
        
        row= row_num, col= col_num)
    fig.update_yaxes(
        title_text= "Count",
        showline=True, linewidth=2, linecolor='black', mirror=True,
        showgrid=True, gridwidth=1, gridcolor='lightgray',
        
        row= row_num, col= col_num)
    
    # Calculate linear regression line
    slope, intercept = np.polyfit(beh_df.index, beh_df.iloc[:, -1], 1)
    line_of_best_fit = slope * np.array(beh_df.index) + intercept
    fig.add_trace(go.Scatter(
        x= beh_df['Week'],
        y= line_of_best_fit,
        mode= 'lines',
        name= 'Line of Best Fit',
        line= dict(color='black')
        ), row= row_num, col= col_num)
    
    # Add custom annotation to the bar chart
    line_of_best_fit_Diff = round(((list(abs(line_of_best_fit))[-1] / list(abs(line_of_best_fit))[0]) -1) *100, 2)
    if line_of_best_fit_Diff > 0:
        annotation_text = f"Behavior has increased by <span style='color: red;'>{line_of_best_fit_Diff}%</span> on average over the past 12 weeks."
    else:
        annotation_text = f"Behavior has decreased by <span style='color: green;'>{line_of_best_fit_Diff}%</span> on average over the past 12 weeks."
    fig.add_annotation(
        xref="x domain", yref="y",
        x=0.01, y=0.0,
        text= annotation_text,
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
    
    col_num += 1
    
# Annotation Titles the 6 dynamic charts below
fig.add_annotation(
    x=0.5,
    y=0.375,
    xref="paper",
    yref="paper",
    text="<span style='text-decoration: underline; font-weight: bold;'>Charts below represent the 6 highest behaviors for last week</span>",
    showarrow=False,
    font=dict(size=22, color='black'),
)

# Chart: ROW 11, COL 1
row_num, col_num = 11, 1
fig.add_trace(go.Bar(
    x= NonPriority_Be_Totals_df.index,
    y= NonPriority_Be_Totals_df['Frequency'],
    name= '',
    text= NonPriority_Be_Totals_df_text,
    textfont= dict(color= NonPriority_Be_Totals_df_textColors, size=14),
    ), row= row_num, col= col_num)
fig.update_traces(
    textposition= 'outside',
    row= row_num, col= col_num)
fig.update_xaxes(
    showline=True, linewidth=2, linecolor='black', mirror=True,
    showgrid=True, gridwidth=1, gridcolor='lightgray',
    
    row= row_num, col= col_num)
fig.update_yaxes(
    title_text= "Coachable Behavior Count",
    showline=True, linewidth=2, linecolor='black', mirror=True,
    showgrid=True, gridwidth=1, gridcolor='lightgray',

    row= row_num, col= col_num)

# Chart: ROW 13, COL 2
row_num, col_num = 13, 2
fig.add_trace(go.Bar(
    x= currentWeekNonBP_df[1],
    y= currentWeekNonBP_df[0],
    name= '',
    orientation='h',
    text= currentWeekNonBP_text,
    textfont= dict(color=currentWeekNonBP_textColors),
    ), row= row_num, col= col_num)
fig.update_traces(
    textposition= 'outside',
    row= row_num, col= col_num)
fig.update_xaxes(
    showline=True, linewidth=2, linecolor='black', mirror=True,
    showgrid=True, gridwidth=1, gridcolor='lightgray',
    
    row= row_num, col= col_num)
fig.update_yaxes(
    title_text= "",
    showline=True, linewidth=2, linecolor='black', mirror=True,
    showgrid=True, gridwidth=1, gridcolor='lightgray',
    
    row= row_num, col= col_num)

fig.add_annotation(
    x=1.015,
    y=-0.007,
    xref="paper",
    yref="paper",
    text="Coachable Behaviors",
    showarrow=False,
    font=dict(size=14, color='black'),
    textangle= -90
)


# Chart: ROW 12, COL 2
row_num, col_num = 12, 2
fig.add_trace(go.Bar(
    x= pastWeekNonBP_df[1],
    y= pastWeekNonBP_df[0],
    name= '',
    orientation='h',
    text= pastWeekNonBP_text,
    textfont= dict(color= pastWeekNonBP_textColors),
    ), row= row_num, col= col_num)
fig.update_traces(
    textposition= 'outside',
    row= row_num, col= col_num)
fig.update_xaxes(
    showline=True, linewidth=2, linecolor='black', mirror=True,
    showgrid=True, gridwidth=1, gridcolor='lightgray',
    
    row= row_num, col= col_num)
fig.update_yaxes(
    title_text= "",
    showline=True, linewidth=2, linecolor='black', mirror=True,
    showgrid=True, gridwidth=1, gridcolor='lightgray',
    
    row= row_num, col= col_num)

fig.add_annotation(
    x=1.015,
    y=0.064,
    xref="paper",
    yref="paper",
    text="Coachable Behaviors",
    showarrow=False,
    font=dict(size=14, color='black'),
    textangle= -90
)

# Chart: ROW 11, COL 2
row_num, col_num = 11, 2
fig.add_trace(go.Bar(
    x= pastTwoWeekNonBP_df[1],
    y= pastTwoWeekNonBP_df[0],
    name= '',
    orientation='h',
    text= pastTwoWeekNonBP_text,
    textfont= dict(color= pastTwoWeekNonBP_textColors),
    ), row= row_num, col= col_num)
fig.update_traces(
    textposition= 'outside',
    row= row_num, col= col_num)
fig.update_xaxes(
    showline=True, linewidth=2, linecolor='black', mirror=True,
    showgrid=True, gridwidth=1, gridcolor='lightgray',
    
    row= row_num, col= col_num)
fig.update_yaxes(
    title_text= "",
    showline=True, linewidth=2, linecolor='black', mirror=True,
    showgrid=True, gridwidth=1, gridcolor='lightgray',
    
    row= row_num, col= col_num)
# Add custom annotation to the bar chart
fig.add_annotation(
    xref="x domain", yref="y",
    x=1.0, y=0.25,
    text="% = previous weeks behavior / current weeks behavior",
    showarrow=False,
    font=dict(
        size=14,
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
    x=1.015,
    y=0.145,
    xref="paper",
    yref="paper",
    text="Coachable Behaviors",
    showarrow=False,
    font=dict(size=14, color='black'),
    textangle= -90
)



fig.update_layout(
    showlegend=False,
    height= 3200,
    width=1850,
    title_text=f"<span style='font-size: 24px; font-weight: bold; color: black;'>LYTX Program Results Week: {Behaviors_df.loc[len(Behaviors_df)-1, 'Week']} {Behaviors_df.loc[len(Behaviors_df)-1, 'Year']}</span>",
    
    # Overview of Program Performance - Frequency
    xaxis= dict(domain= [0.0, 1.0]),
    yaxis= dict(domain= [0.84, 0.998]),
    
    # Near Collisions - Trend
    yaxis3= dict(domain= [0.64, 0.679]),
    
    # Near Collisions - Behaviors - Past 12 Weeks
    xaxis4= dict(domain= [0.47, 1.0]),
    yaxis4= dict(domain= [0.62, 0.679]),

    # Behavior Profile: Sum 12 Weeks
    yaxis5= dict(domain= [0.44, 0.599]),

    # Current Week Behavior Profile
    xaxis6= dict(domain= [0.47, 1.00]),
    yaxis6= dict(domain= [0.54, 0.599]),

    # Past Week Behavior Profile
    xaxis7= dict(domain= [0.47, 1.00]),
    yaxis7= dict(domain= [0.458, 0.518]),

    # Past 2 Week Behavior Profile
    xaxis8= dict(domain= [0.47, 1.00]),
    yaxis8= dict(domain= [0.39, 0.439]),
    
    # First row of dynamic updating charts
    yaxis9= dict(domain=[0.32, 0.358]),
    yaxis10= dict(domain=[0.32, 0.358]),
    yaxis11= dict(domain=[0.32, 0.358]),
    
    # Second row of dynamic updating charts
    yaxis12= dict(domain=[0.24, 0.278]),
    yaxis13= dict(domain=[0.24, 0.278]),
    yaxis14= dict(domain=[0.24, 0.278]),
    
    # Non-Priority Behavior Profile: Sum 12 Weeks
    yaxis15= dict(domain=[0.0, 0.198]),
    
    # Current Week Non-Priority Behavior Profile
    xaxis16= dict(domain= [0.47, 1.00]),
    yaxis16= dict(domain= [0.14, 0.198]),

    # Past Week Non-Priority Behavior Profile
    xaxis17= dict(domain= [0.47, 1.00]),
    yaxis17= dict(domain= [0.06, 0.118]),

    # Past 2 Week Non-Priority Behavior Profile
    xaxis18= dict(domain= [0.47, 1.00]),
    yaxis18= dict(domain= [0.0, 0.038]),
)
fig.show()

# save_week = Behaviors_df.loc[len(Behaviors_df)-1, 'Week']
# save_year = Behaviors_df.loc[len(Behaviors_df)-1, 'Year']
# fig.write_html(f'LYTX_Program_Results_Chart\\{save_year} {save_week} company.html')
