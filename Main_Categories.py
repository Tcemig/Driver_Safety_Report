import pandas as pd
import os
import re
import numpy as np

COV_df = pd.read_csv('Main_CSV_Files\\COV_df.csv')


for cat in ['Contractor', 'COV', 'Linehaul']:
    
    df = pd.read_csv(f'Main_CSV_Files\\{cat}_df.csv')
    # Making Top 20 behavior profile
    cols = list(COV_df.columns)
    Behaviors_df = pd.DataFrame(columns= cols)
    for index, row in COV_df.iterrows():
        temp_monthYear = COV_df.loc[index, 'Month-Year']
        temp_week = COV_df.loc[index, 'Week']
        temp_year = COV_df.loc[index, 'Year']
        temp_date = COV_df.loc[index, 'Date']
        
        temp_cat_df = df[df['Week'] == temp_week]
        sum_list = [temp_monthYear, temp_date, temp_week, temp_year]
        for col in (Behaviors_df.columns)[4:]:
            sum_list.append(temp_cat_df[col].sum())
        temp_cat_df.loc[len(temp_cat_df)] = sum_list 
        temp_cat_df = temp_cat_df.iloc[-1:, :]
        temp_cat_df = temp_cat_df.reset_index(drop=True)
        
        Behaviors_df.loc[len(Behaviors_df)] = list(temp_cat_df.iloc[0, :])

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

    Behaviors_df.to_csv(f'Main_CSV_Category_Files\\{cat}_Behaviors.csv', index=False)
    NearCollisions_df.to_csv(f'Main_CSV_Category_Files\\{cat}_NearCollisions.csv', index=False)

