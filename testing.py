import pandas as pd
import os
import re
import xlwings

wb = xlwings.Book("LYTX DATA.xlsx")

sheet = wb.sheets["Van Program - Safety Monitoring"]

used_range = sheet.used_range
data = used_range.value
df = pd.DataFrame(data[1:], columns=data[0])
df['Week Starting'] = pd.to_datetime(df['Week Starting'])
df.to_csv('Main_CSV_Files\\Safety_Monitoring.csv', index=False)
wb.save()
