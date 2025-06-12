import pandas as pd
import os
import xlwings
import re
import datetime as dt

# Following Distance: â‰¥ 1 sec to < 2 sec

# Recreating all Main CSV Files
priority_behaviors = [
    'Handheld Device', 'Posted Speed Violation', 'Following Distance: < 1 second', 'Inattentive', 'Near Collision',
    'Red Light', 'Aggressive', 'Failed to Keep an Out', 'Falling Asleep', 'Intersection Awareness', 'Late Response', 
    'Mirror Use', 'Not Scanning Roadway', 'Too Fast for Conditions'
    ]

df = pd.read_csv('AllBehaviors.csv')
df_columns = list(df['Behavior'])

df_columns.insert(0, 'Week')
df_columns.insert(1, 'Year')
df_ = pd.DataFrame(columns=df_columns)

df_.to_csv('Main_CSV_Files\\Contractor_df.csv', index=False)
df_.to_csv('Main_CSV_Files\\COV_df.csv', index=False)
df_.to_csv('Main_CSV_Files\\Linehaul_df.csv', index=False)

Contractor_df = pd.read_csv('Main_CSV_Files\\Contractor_df.csv')
Linehaul_df = pd.read_csv('Main_CSV_Files\\Linehaul_df.csv')
COV_df = pd.read_csv('Main_CSV_Files\\COV_df.csv')

df_columns = ['Unique Drivers', 'Unique COV Drivers', 'Unique Contractor Drivers', 'Unique Linehaul Drivers']
df_columns.insert(0, 'Week')
df_columns.insert(1, 'Year')
df_ = pd.DataFrame(columns=df_columns)
df_.to_csv('Main_CSV_Files\\Unique Drivers with Events.csv', index=False)

UDwE_df = pd.read_csv('Main_CSV_Files\\Unique Drivers with Events.csv')

for DATE in os.listdir('Weekly Event Worksheets'):

    New_Row = [f"{DATE[:-9].rstrip()}", f"{DATE[12:16]}"] + [0]*41

    Contractor_df.loc[len(Contractor_df.index)] = New_Row
    Linehaul_df.loc[len(Linehaul_df.index)] = New_Row
    COV_df.loc[len(COV_df.index)] = New_Row

    New_Row_2 = [f"{DATE[:-9].rstrip()}", f"{DATE[12:16]}"] + [0]*4

    UDwE_df.loc[len(UDwE_df.index)] = New_Row_2


    LYTX_DataSet = pd.read_csv(f'Weekly Event Worksheets\\{DATE[:-4]}.csv', na_values= "")
    LYTX_DataSet = LYTX_DataSet.fillna("")
    LYTX_DataSet = LYTX_DataSet.sort_values('Date', ascending=True)
    LYTX_DataSet = LYTX_DataSet[LYTX_DataSet['Behaviors'] != ""]
    LYTX_DataSet = LYTX_DataSet[LYTX_DataSet['Behaviors'] != "*Unusual Event"]
    # LYTX_DataSet = LYTX_DataSet.rename(columns={'Following Distance: â‰¥ 1 sec to < 2 sec': 'Following Distance: > 1 sec to < 2 sec'})
    LYTX_DataSet = LYTX_DataSet.reset_index(drop=True)

    # Drops behaviors not in priority_behaviors
    LYTX_DataSet_2 = LYTX_DataSet
    for index, row in LYTX_DataSet_2.iterrows():
        B = list(re.split(',', LYTX_DataSet_2['Behaviors'][index]))
        Blen = len(B)-1
        for Bitem in B:
            if Bitem in priority_behaviors:
                break
            if (B.index(Bitem) == Blen):
                LYTX_DataSet_2 = LYTX_DataSet_2.drop(index, axis= 0)

    Unique_Names = LYTX_DataSet_2['Driver'].unique()
    Unique_Names_num = len(Unique_Names)
    UDwE_df.loc[(len(UDwE_df.index)-1, 'Unique Drivers')] = Unique_Names_num

    for col in ['COV', 'Contractor', 'LineHaul']:
        if col == 'COV':
            Unique_Names_num = LYTX_DataSet_2[LYTX_DataSet_2['Group'] != 'Contractor']
            Unique_Names_num = Unique_Names_num[Unique_Names_num['Group'] != 'LineHaul - All']
            
            # Remove rows where 'Driver' contains 'Linehaul'
            Unique_Names_num = Unique_Names_num[~Unique_Names_num['Driver'].str.contains('Linehaul')]
            # Remove rows where 'Driver' ends with 'GG'
            Unique_Names_num = Unique_Names_num[~Unique_Names_num['Driver'].str.endswith('GG')]
            # Remove rows where 'Driver' ends with 'GG'
            Unique_Names_num = Unique_Names_num[~Unique_Names_num['Driver'].str.endswith('-M')]
            
            Unique_Names_num = Unique_Names_num['Driver'].unique()
            Unique_Names_num = len(Unique_Names_num)
            UDwE_df.loc[(len(UDwE_df.index)-1, 'Unique COV Drivers')] = Unique_Names_num
        if col == 'Contractor':
            Unique_Names_num_1 = LYTX_DataSet_2[LYTX_DataSet_2['Group'] == 'Contractor']
            Unique_Names_num_2 = LYTX_DataSet_2[LYTX_DataSet_2['Driver'].str.endswith('GG')]
            Unique_Names_num_3 = LYTX_DataSet_2[LYTX_DataSet_2['Driver'].str.endswith('-M')]
            
            Unique_Names_num = pd.concat([Unique_Names_num_1, Unique_Names_num_2, Unique_Names_num_3], axis=0)
            Unique_Names_num = Unique_Names_num.drop_duplicates()
            
            Unique_Names_num = Unique_Names_num['Driver'].unique()
            Unique_Names_num = len(Unique_Names_num)
            UDwE_df.loc[(len(UDwE_df.index)-1, 'Unique Contractor Drivers')] = Unique_Names_num
        if col == 'LineHaul':
            Unique_Names_num_1 = LYTX_DataSet_2[LYTX_DataSet_2['Group'] == 'LineHaul - All']
            Unique_Names_num_2 = LYTX_DataSet_2[LYTX_DataSet_2['Driver'].str.contains('Linehaul')]
            
            Unique_Names_num = pd.concat([Unique_Names_num_1, Unique_Names_num_2], axis=0)
            Unique_Names_num = Unique_Names_num.drop_duplicates()

            Unique_Names_num = Unique_Names_num['Driver'].unique()
            Unique_Names_num = len(Unique_Names_num)
            UDwE_df.loc[(len(UDwE_df.index)-1, 'Unique Linehaul Drivers')] = Unique_Names_num

    for index, row in LYTX_DataSet.iterrows():

        if (LYTX_DataSet['Group'][index] == "LineHaul - All") or ("Linehaul" in LYTX_DataSet['Driver'][index]):

            Behaviors = LYTX_DataSet['Behaviors'][index]
            Behaviors_List = re.split('[,]', Behaviors)
            for b in Behaviors_List:
                try:
                    Linehaul_df.loc[(len(Linehaul_df.index)-1), b] += 1
                except KeyError:
                    Linehaul_df.loc[(len(Linehaul_df.index)-1), 'Following Distance: > 1 sec to < 2 sec'] += 1
                    print(index, b)

        elif (LYTX_DataSet['Group'][index] == 'Contractor') or (LYTX_DataSet['Driver'][index].endswith("GG")) or (LYTX_DataSet['Driver'][index].endswith("-M")):

            Behaviors = LYTX_DataSet['Behaviors'][index]
            Behaviors_List = re.split('[,]', Behaviors)
            for b in Behaviors_List:
                try:
                    Contractor_df.loc[(len(Contractor_df.index)-1), b] += 1
                except KeyError:
                    Contractor_df.loc[(len(Contractor_df.index)-1), 'Following Distance: > 1 sec to < 2 sec'] += 1
                    print(index, b)

        else:

            Behaviors = LYTX_DataSet['Behaviors'][index]
            Behaviors_List = re.split('[,]', Behaviors)
            for b in Behaviors_List:
                try:
                    COV_df.loc[(len(COV_df.index)-1), b] += 1
                except KeyError:
                    COV_df.loc[(len(COV_df.index)-1), 'Following Distance: > 1 sec to < 2 sec'] += 1
                    print(index, b)

# Sort COV, Contractor, Linehaul Dataframes
# for for_df in [COV_df, Contractor_df, Linehaul_df, UDwE_df]:
COV_df['Date'] = COV_df['Week'].str.split('-').str[0]
COV_df['Date'] = COV_df['Date'] + '.' + COV_df['Year']
COV_df['Date'] = pd.to_datetime(COV_df['Date'], format="%m.%d.%Y")
COV_df = COV_df.sort_values('Date', ascending=True)
COV_df.insert(0, "Date", COV_df.pop('Date'))
COV_df['Total'] = COV_df.iloc[:, 3:].sum(axis=1)
COV_df['Month-Year'] = ''
COV_df = COV_df.reset_index(drop=True)
for index, row in COV_df.iterrows():
    COV_df.loc[index, 'Month-Year'] = dt.datetime.strftime(COV_df.loc[index, 'Date'], "%m-%Y")
COV_df.insert(0, "Month-Year", COV_df.pop('Month-Year'))

Contractor_df['Date'] = Contractor_df['Week'].str.split('-').str[0]
Contractor_df['Date'] = Contractor_df['Date'] + '.' + Contractor_df['Year']
Contractor_df['Date'] = pd.to_datetime(Contractor_df['Date'], format="%m.%d.%Y")
Contractor_df = Contractor_df.sort_values('Date', ascending=True)
Contractor_df.insert(0, "Date", Contractor_df.pop('Date'))
Contractor_df['Total'] = Contractor_df.iloc[:, 3:].sum(axis=1)
Contractor_df['Month-Year'] = ''
Contractor_df = Contractor_df.reset_index(drop=True)
for index, row in Contractor_df.iterrows():
    Contractor_df.loc[index, 'Month-Year'] = dt.datetime.strftime(Contractor_df.loc[index, 'Date'], "%m-%Y")
Contractor_df.insert(0, "Month-Year", Contractor_df.pop('Month-Year'))

Linehaul_df['Date'] = Linehaul_df['Week'].str.split('-').str[0]
Linehaul_df['Date'] = Linehaul_df['Date'] + '.' + Linehaul_df['Year']
Linehaul_df['Date'] = pd.to_datetime(Linehaul_df['Date'], format="%m.%d.%Y")
Linehaul_df = Linehaul_df.sort_values('Date', ascending=True)
Linehaul_df.insert(0, "Date", Linehaul_df.pop('Date'))
Linehaul_df['Total'] = Linehaul_df.iloc[:, 3:].sum(axis=1)
Linehaul_df['Month-Year'] = ''
Linehaul_df = Linehaul_df.reset_index(drop=True)
for index, row in Linehaul_df.iterrows():
    Linehaul_df.loc[index, 'Month-Year'] = dt.datetime.strftime(Linehaul_df.loc[index, 'Date'], "%m-%Y")
Linehaul_df.insert(0, "Month-Year", Linehaul_df.pop('Month-Year'))

UDwE_df['Date'] = UDwE_df['Week'].str.split('-').str[0]
UDwE_df['Date'] = UDwE_df['Date'] + '.' + UDwE_df['Year']
UDwE_df['Date'] = pd.to_datetime(UDwE_df['Date'], format="%m.%d.%Y")
UDwE_df = UDwE_df.sort_values('Date', ascending=True)
UDwE_df.insert(0, "Date", UDwE_df.pop('Date'))
UDwE_df['Month-Year'] = ''
UDwE_df = UDwE_df.reset_index(drop=True)
for index, row in UDwE_df.iterrows():
    UDwE_df.loc[index, 'Month-Year'] = dt.datetime.strftime(UDwE_df.loc[index, 'Date'], "%m-%Y")
UDwE_df.insert(0, "Month-Year", UDwE_df.pop('Month-Year'))

skip=1

# Making Top 20 behavior profile
cols = list(COV_df.columns)
Behaviors_df = pd.DataFrame(columns= cols)
for index, row in COV_df.iterrows():
    temp_monthYear = COV_df.loc[index, 'Month-Year']
    temp_week = COV_df.loc[index, 'Week']
    temp_year = COV_df.loc[index, 'Year']
    temp_date = COV_df.loc[index, 'Date']
    
    temp_cov_df = COV_df[COV_df['Week'] == temp_week]
    temp_contractor_df = Contractor_df[Contractor_df['Week'] == temp_week]
    temp_linehaul_df = Linehaul_df[Linehaul_df['Week'] == temp_week]
    temp_week_df = pd.concat([temp_cov_df, temp_contractor_df, temp_linehaul_df], axis=0)
    sum_list = [temp_monthYear, temp_date, temp_week, temp_year]
    for col in (Behaviors_df.columns)[4:]:
        sum_list.append(temp_week_df[col].sum())
    temp_week_df.loc[len(temp_week_df)] = sum_list 
    temp_week_df = temp_week_df.iloc[-1:, :]
    temp_week_df = temp_week_df.reset_index(drop=True)
    
    Behaviors_df.loc[len(Behaviors_df)] = list(temp_week_df.iloc[0, :])

Behaviors_df = Behaviors_df.sort_values('Date', ascending=True)

NearCollisions_df = Behaviors_df[[
        "Date",
        "Week",
        "Year",
        "Failed to Keep an Out",
        "Mirror Use",
        "Intersection Awareness",
        "Late Response",
        "Red Light",
        "Drowsy",
        "Following Distance: < 1 second",
        "Failed to Stop",
    ]]

Behaviors_df = Behaviors_df.iloc[:, :]
Behaviors_df = Behaviors_df.reset_index(drop=True)
sum_list = ["0", "0", "0"]
for col in (Behaviors_df.columns)[3:]:
    if col == "Date":
        sum_list.append("0")
    else:
        sum_list.append(Behaviors_df[col].sum())
Behaviors_df.loc[len(Behaviors_df)] = sum_list
Behaviors_Totals_df = Behaviors_df.iloc[-1:, :]
Behaviors_Totals_df = Behaviors_Totals_df.drop(['Date', 'Year', 'Week', 'Month-Year', 'Total'], axis=1)
Behaviors_Totals_df = Behaviors_Totals_df.transpose()
Behaviors_Totals_df = Behaviors_Totals_df.rename(columns={Behaviors_Totals_df.columns[0]: "Frequency"})
Behaviors_Totals_df = Behaviors_Totals_df.sort_values("Frequency", ascending=False)

Behaviors_df = Behaviors_df.iloc[:-1, :]
Behaviors_df['Total Behaviors'] = Behaviors_df.iloc[:, 4:].sum(axis=1)

# Near Collisions Behaviors profile
NearCollisions_df = NearCollisions_df.reset_index(drop=True)
sum_list = ["0", "0", "0"]
for col in (NearCollisions_df.columns)[3:]:
    if col == "Date":
        sum_list.append("0")
    else:
        sum_list.append(NearCollisions_df[col].sum())
NearCollisions_df.loc[len(NearCollisions_df)] = sum_list
NearCollision_Totals_df = NearCollisions_df.iloc[-1:, :]
NearCollision_Totals_df = NearCollision_Totals_df.drop(['Date', 'Year', 'Week'], axis=1)
NearCollision_Totals_df = NearCollision_Totals_df.transpose()
NearCollision_Totals_df = NearCollision_Totals_df.rename(columns={NearCollision_Totals_df.columns[0]:"Frequency"})
NearCollision_Totals_df = NearCollision_Totals_df.sort_values("Frequency", ascending=False)

NearCollisions_df = NearCollisions_df.iloc[:-1, :]
NearCollisions_df['Total Behaviors'] = NearCollisions_df.iloc[:, 4:].sum(axis=1)

LYTX_Users_df = pd.read_csv("LYTX_Users.csv")
LYTX_Users_df.columns = LYTX_Users_df.columns.str.strip()  # Strip whitespace from column names
LYTX_Users_df.rename(columns={LYTX_Users_df.columns[0]: 'Name'}, inplace=True)  # Rename the first column to 'Name'

# LYTX_Users_df = LYTX_Users_df[LYTX_Users_df['Login'] != 'Disabled']
LYTX_Vehicles_df = pd.read_csv("LYTX_Vehicles.csv")
for index, row in LYTX_Vehicles_df.iterrows():
    temp_user = LYTX_Vehicles_df.loc[index, "Driver"]
    users_group = LYTX_Users_df[LYTX_Users_df['Name'] == temp_user]
    users_group = users_group.reset_index(drop=True)
    try:
        users_group = users_group.loc[0, "Roles (Group)"]
        if "Contractor" in users_group:
            LYTX_Vehicles_df.loc[index, "Group"] = "Contractor"
    except KeyError:
        pass

LYTX_Vehicles_df = LYTX_Vehicles_df.dropna(subset=['Last Check In'])
LYTX_Vehicles_df = LYTX_Vehicles_df.reset_index(drop=True)
for index, row in LYTX_Vehicles_df.iterrows():
    temp_date = re.split("[,]", LYTX_Vehicles_df.loc[index, "Last Check In"])
    temp_date = temp_date[0] + "," + temp_date[1]
    temp_date = dt.datetime.strptime(temp_date, "%b %d, %Y")
    temp_date = dt.datetime.strftime(temp_date, "%m-%Y")
    temp_date = dt.datetime.strptime(temp_date, "%m-%Y")
    LYTX_Vehicles_df.loc[index, "Last Check In"] = temp_date
    
    skip=1
    
Month_Year_List = list(COV_df['Month-Year'].unique())
LYTX_Vehicles_BreakDown = pd.DataFrame(
    data= {
        "Date": Month_Year_List,
        "Total ERs": [0]*len(Month_Year_List),
        "COV ERs": [0]*len(Month_Year_List),
        "Contractor ERs": [0]*len(Month_Year_List),
        "Linehaul ERs": [0]*len(Month_Year_List),
    }
)
LYTX_Vehicles_BreakDown = LYTX_Vehicles_BreakDown.reset_index(drop=True)
for index, row in LYTX_Vehicles_BreakDown.iterrows():
    temp_date = LYTX_Vehicles_BreakDown.loc[index, "Date"]
    temp_df = LYTX_Vehicles_df[LYTX_Vehicles_df['Last Check In'] >= dt.datetime.strptime(temp_date, "%m-%Y")]
    temp_df = temp_df[temp_df['Group'] != 'Default']
    LYTX_Vehicles_BreakDown.loc[index, "Total ERs"] = len(list(temp_df['Group']))
    for col in ['COV', 'Linehaul', 'Contractor']:
        if col == 'COV':
            temp_cov_df = temp_df[~temp_df['Group'].isin(['Contractor', 'LineHaul - All', 'LineHaul', 'TCN', 'Red-Cross'])]
            temp_cov_df = len(list(temp_cov_df['Group']))
            LYTX_Vehicles_BreakDown.loc[index, 'COV ERs'] = temp_cov_df
        elif col == 'Linehaul':
            temp_linehaul_df = temp_df[temp_df['Group'].isin(['LineHaul - All', 'LineHaul'])]
            temp_linehaul_df = len(list(temp_linehaul_df['Group']))
            LYTX_Vehicles_BreakDown.loc[index, 'Linehaul ERs'] = temp_linehaul_df
        elif col == 'Contractor':
            temp_contractor_df = temp_df[temp_df['Group'].isin(['Contractor', 'TCN', 'Red-Cross'])]
            temp_contractor_df = len(list(temp_contractor_df['Group']))
            LYTX_Vehicles_BreakDown.loc[index, 'Contractor ERs'] = temp_contractor_df


#############################################################################
Contractor_df.to_csv('Main_CSV_Files\\Contractor_df.csv', index=False)
Linehaul_df.to_csv('Main_CSV_Files\\Linehaul_df.csv', index=False)
COV_df.to_csv('Main_CSV_Files\\COV_df.csv', index=False)
Behaviors_df.to_csv('Main_CSV_Files\\Behaviors_df.csv', index=False)
Behaviors_Totals_df.to_csv('Main_CSV_Files\\Behaviors_Totals_df.csv', index=True)
NearCollisions_df.to_csv('Main_CSV_Files\\NearCollision_df.csv', index=False)
NearCollision_Totals_df.to_csv('Main_CSV_Files\\NearCollision_Totals_df.csv', index=True)
LYTX_Vehicles_BreakDown.to_csv('Main_CSV_Files\\LYTX_Vehicles_Breakdown_df.csv', index=False)

COV_df = COV_df.drop(['Month-Year', 'Date'], axis=1)
Contractor_df = Contractor_df.drop(['Month-Year', 'Date'], axis=1)
Linehaul_df = Linehaul_df.drop(['Month-Year', 'Date'], axis=1)
UDwE_df = UDwE_df.drop(['Month-Year', 'Date'], axis=1)
wb = xlwings.Book("LYTX DATA.xlsx")

COV_Sheet = wb.sheets["COV DataFrame"]
Contractor_Sheet = wb.sheets["Contractor DataFrame"]
Linehaul_Sheet = wb.sheets["Linehaul DataFrame"]
BehaviorsProfile_Sheet = wb.sheets['Behavior Profile']

Total_Drivers_Sheet = wb.sheets["Unique Drivers DataFrame"]

COV_Sheet.range(1,1).value = COV_df

Contractor_Sheet.range(1,1).value = Contractor_df

Linehaul_Sheet.range(1,1).value = Linehaul_df

Total_Drivers_Sheet.range(1,1).value = UDwE_df

BehaviorsProfile_Sheet.range(2,1).value = Behaviors_df
BehaviorsProfile_Sheet.range(2,4).value = NearCollision_Totals_df
BehaviorsProfile_Sheet.range(2,7).value = NearCollisions_df

wb.save()
# wb.close()









