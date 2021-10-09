# DS4B 101-P: PYTHON FOR DATA SCIENCE AUTOMATION ----
# JUMPSTART (Module 1): First Sales Analysis with Python ----

# Important VSCode Set Up:
#   1. Select a Python Interpreter: ds4b_101p
#   2. Delete terminals to start a fresh Python Terminal session

# 1.0 Load Libraries ----

# Core Python Data Analysis
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Plotting
from plotnine import (  # python很常只import你要的function，不會import整個package
    ggplot, aes, geom_col,
    geom_col, geom_line, geom_smooth,
    facet_wrap,
    scale_y_continuous,
    scale_x_datetime,
    labs,
    theme, theme_minimal, theme_matplotlib
)
from mizani.breaks import date_breaks
from mizani.formatters import date_format, currency_format

# Misc
from os import mkdir, getcwd  # mkder是os的一個function(意思是，我不能再用mkdir.xxx)
# pretty 是 rich 下的一個 module。他叫module不叫function，因為他還可以用 pretty.xxx
from rich import pretty
pretty.install()  # 這只會影響目前 python console 的結果，他沒有真的安裝什麼東西
# rich這個package是用來做terminal formatting用的，讓terminal變漂亮一點
# 例如我現在重新執行 numpy 的計算，會發現結果的顏色變藍色，比較能區分 code 和 result 了
np.sum([1, 2, 3])

# 2.0 Importing Data Files ----

# help(pd.read_excel)
# - Use "q" to quit

bikes_df = pd.read_excel("./00_data_raw/bikes.xlsx", engine='openpyxl')
bikeshops_df = pd.read_excel("./00_data_raw/bikeshops.xlsx", engine='openpyxl')
orderlines_df = pd.read_excel(
    io="./00_data_raw/orderlines2.xlsx",
    engine='openpyxl',
    converters={'order.date': str}
)

orderlines_df.info()

orderlines_df

# 3.0 Examining Data ----


# 4.0 Joining Data ----


# 5.0 Wrangling Data ----

# * No copy


# * Copy


# * Handle Dates


# * Show Effect: Copy vs No Copy


# * Text Columns


# * Splitting Description into category_1, category_2, and frame_material


# * Splitting Location into City and State


# * Price Extended


# * Reorganizing


# * Renaming columns


# 6.0 Visualizing a Time Series ----


# 6.1 Total Sales by Month ----


# Quick Plot ----


# Report Plot ----


# 6.2 Sales by Year and Category 2 ----

# ** Step 1 - Manipulate ----


# Step 2 - Visualize ----


# Simple Plot


# Reporting Plot


# 7.0 Writing Files ----


# Pickle ----


# CSV ----


# Excel ----


# WHERE WE'RE GOING
# - Building a forecast system
# - Create a database to host our raw data
# - Develop Modular Functions to:
#   - Collect data
#   - Summarize data and prepare for forecast
#   - Run Automatic Forecasting for One or More Time Series
#   - Store Forecast in Database
#   - Retrieve Forecasts and Report using Templates
