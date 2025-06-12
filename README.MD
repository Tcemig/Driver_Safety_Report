# LYTX Weekly Report Analysis

This repository contains scripts and data for analyzing and reporting on LYTX safety events, driver behaviors, and vehicle performance. The project automates the extraction, processing, and visualization of LYTX data for weekly, categorical, and top-10 behavior reports.

## Directory Structure

- **Main_2.py, Main_Categories.py**  
  Core scripts for processing raw data, generating summary CSVs, and preparing data for reporting and visualization.

- **Chart_Report.py, Category_Chart_Report.py, top_ten_tables.py**  
  Scripts for generating interactive charts and tables using Plotly, including:
  - Program performance over time
  - Categorical breakdowns
  - Top 10 behaviors by vehicle

- **Lytx_API.py**  
  Utilities for pulling data from the LYTX API, including events, vehicles, drivers, and groups.

- **testing.py**  
  Utility script for extracting and saving safety monitoring data from Excel.

- **Main_CSV_Files/**  
  Contains main processed CSV files for COV, Contractor, and Linehaul groups.

- **Main_CSV_Category_Files/**  
  Contains category-specific behavior and near-collision CSVs for each group.

- **LYTX_Categorical_Results_Chart/**  
  Output directory for categorical results charts.

- **LYTX_Program_Results_Chart/**  
  Output directory for program results charts.

- **LYTX_Top_10_Driver_Tables/**  
  Output directory for top 10 driver/vehicle behavior tables.

- **DIO Groups/**  
  Contains group-specific data files.

- **Weekly Event Worksheets/**  
  Raw weekly event data exported from LYTX.

- **LYTX DATA.xlsx**  
  Main Excel file containing raw and processed data.

- **LYTX_Devices.csv, LYTX_Users.csv, LYTX_Vehicles.csv**  
  Exported reference data from LYTX.

- **AllBehaviors.csv**  
  Master list of all tracked behaviors.

- **.env**  
  Environment variables for API keys and connections (not tracked in git).

## How to Use

1. **Prepare Data**  
   - Place raw weekly event CSVs in `Weekly Event Worksheets/`.
   - Ensure reference files (`LYTX_Devices.csv`, `LYTX_Users.csv`, `LYTX_Vehicles.csv`) are up to date.

2. **Run Data Processing**  
   - Execute `Main_2.py` to generate and update summary CSVs in `Main_CSV_Files/` and `Main_CSV_Category_Files/`.

3. **Generate Reports**  
   - Run `Chart_Report.py` for program-level charts.
   - Run `Category_Chart_Report.py` for categorical breakdowns.
   - Run `top_ten_tables.py` for top 10 behavior tables.

4. **View Outputs**  
   - Charts and tables are saved in their respective output directories as HTML files for easy sharing and review.

## Requirements

- Python 3.x
- pandas, numpy, plotly, xlwings, python-dotenv, statistics

Install dependencies with:
```sh
pip install pandas numpy plotly xlwings python-dotenv
```

## Environment Variables

Create a `.env` file with your  API credentials:
```
LYTX_API_KEY=your_api_key
LYTX_HTTP_CONNECTION=your_api_connection
```

## Notes

- Output HTML files are ignored by `.gitignore`.

---

For questions or issues, please contact the project maintainer.