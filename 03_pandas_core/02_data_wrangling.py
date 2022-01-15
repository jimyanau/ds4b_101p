# DS4B 101-P: PYTHON FOR DATA SCIENCE AUTOMATION ----
# Week 2 (Data Wrangling): Data Wrangling ----

# IMPORTS

from plotnine import (
    ggplot, aes, geom_col, facet_wrap,
    coord_flip,
    theme_minimal
)
from mizani.formatters import dollar_format
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.core import groupby
from pandas.core.frame import DataFrame

from my_pandas_extensions.database import collect_data


df['category_2'].value_counts()


# Binning


df[['model', 'price']] \
    .drop_duplicates() \
    .assign(price_group=lambda x: pd.cut(x.price, bins=3)) \
    .pivot(
        index='model',
        columns='price_group',
        values='price'
) \
    .style.background_gradient(cmap='Blues')


df[['model', 'price']] \
    .drop_duplicates() \
    .assign(price_group=lambda x: pd.qcut(x.price, q=3)) \
    .pivot(
        index='model',
        columns='price_group',
        values='price'
) \
    .style.background_gradient(cmap='Blues')

# 5.0 GROUPING  ----


# Common Summaries

df['model'].value_counts()
df[['model', 'category_1']].value_counts()

df.nunique()
df.isna().sum()


# Detecting NA

summary_df_1.columns

summary_df_1.isna().sum()


# 5.3 Groupby + Transform (Apply)
# - Note: Groupby + Assign does not work. No assign method for groups.


summary_df_3 \
    .set_index('order_date') \
    .groupby('category_2') \
    .apply(lambda x: (x.total_price - x.total_price.mean()) / x.total_price.std()) \
    .reset_index() \
    .pivot(
        index="order_date",
        columns="category_2",
        values="total_price"
    ) \
    .plot()


summary_df_3 \
    .set_index(['order_date', 'category_2']) \
    .groupby('category_2') \
    .apply(lambda x: (x - x.mean()) / x.std()) \
    .reset_index()


# 5.4 Groupby + Filter (Apply)

df.tail(5)

summary_df_3 \
    .groupby('category_2') \
    .tail(5)

summary_df_3 \
    .groupby('category_2') \
    .apply(lambda x: x.iloc[:20])


# 6.0 RENAMING ----

# Single Index

summary_df_2 \
    .rename(columns=dict(category_1="Category 1"))

summary_df_2.columns.str.replace("_", " ").str.title()

summary_df_2 \
    .rename(columns=lambda x: x.replace("_", " ").title())


# Targeting specific columns

summary_df_2 \
    .rename(columns={'total_price': 'Revenue'})

# - Mult-Index

summary_df_1.columns

"_".join(('total_price', 'median'))

["_".join(col).rstrip("_") for col in summary_df_1.columns.tolist()]

summary_df_1 \
    .set_axis(
        ["_".join(col).rstrip("_") for col in summary_df_1.columns.tolist()],
        axis=1
    )


# 7.0 RESHAPING (MELT & PIVOT_TABLE) ----

# Aggregate Revenue by Bikeshop by Category 1

bikeshop_revenue_df = df[['bikeshop_name', 'category_1', 'total_price']] \
    .groupby(['bikeshop_name', 'category_1']) \
    .sum() \
    .reset_index() \
    .sort_values('total_price', ascending=False) \
    .rename(columns=lambda x: x.replace("_", " ").title())

bikeshop_revenue_df

# 7.1 Pivot & Melt

# Pivot (Pivot Wider)

bikeshop_revenue_wide_df = bikeshop_revenue_df \
    .pivot(
        index=['Bikeshop Name'],
        columns=['Category 1'],
        values=['Total Price']
    ) \
    .reset_index() \
    .set_axis(
        ["Bikeshop Name", 'Mountain', "Road"],
        axis=1
    )

bikeshop_revenue_wide_df \
    .sort_values("Mountain") \
    .plot(
        x="Bikeshop Name",
        y=["Mountain", "Road"],
        kind="barh"
    )


usd = dollar_format(prefix="$", digits=0, big_mark=",")
usd([1000])[0]


bikeshop_revenue_wide_df \
    .sort_values("Mountain", ascending=False) \
    .style \
    .highlight_max() \
    .format(
        {
            "Mountain": lambda x: usd([x])[0],
            "Road": lambda x: usd([x])[0]
        }
    ) \
    .to_excel("03_pandas_core/bikeshop_revenue_wide.xlsx")


# Melt (Pivoting Longer)

bikeshop_revenue_long_df = pd.read_excel("03_pandas_core/bikeshop_revenue_wide.xlsx") \
    .iloc[:, 1:] \
    .melt(
        value_vars=["Mountain", "Road"],
        var_name="Category 1",
        value_name="Revenue",
        id_vars="Bikeshop Name"
)

bikeshop_order = bikeshop_revenue_long_df \
    .groupby("Bikeshop Name") \
    .sum() \
    .sort_values("Revenue") \
    .index \
    .tolist()


bikeshop_revenue_long_df["Bikeshop Name"] = pd.Categorical(
    bikeshop_revenue_long_df['Bikeshop Name'], categories=bikeshop_order)

bikeshop_revenue_long_df.info()

ggplot(
    mapping=aes(x="Bikeshop Name", y="Revenue", fill="Category 1"),
    data=bikeshop_revenue_long_df
) + \
    geom_col() + \
    coord_flip() + \
    facet_wrap("Category 1") + \
    theme_minimal()


# 7.2 Pivot Table (Pivot + Summarization, Excel Pivot Table)

df \
    .pivot_table(
        columns=None,
        values="total_price",
        index="category_1",
        aggfunc=np.sum
    )

df \
    .pivot_table(
        columns="frame_material",
        values="total_price",
        index="category_1",
        aggfunc=np.sum
    )

df \
    .pivot_table(
        columns=None,
        values="total_price",
        index=["category_1", "frame_material"],
        aggfunc=np.sum
    )

sales_by_cat1_cat2_year_df = df \
    .assign(year=lambda x: x.order_date.dt.year) \
    .pivot_table(
        columns="year",
        aggfunc=np.sum,
        index=["category_1", "category_2"],
        values=['total_price']
    )

# 7.3 Stack & Unstack ----

# Unstack - Pivots Wider 1 Level (Pivot)

sales_by_cat1_cat2_year_df \
    .unstack(
        level=0,
        fill_value=0
    )

sales_by_cat1_cat2_year_df \
    .unstack(
        level="category_2",
        fill_value=0
    )

# Stack - Pivots Longer 1 Level (Melt)

sales_by_cat1_cat2_year_df \
    .stack(
        level="year"
    )

sales_by_cat1_cat2_year_df \
    .stack(
        level='year'
    ) \
    .unstack(
        level=["category_1", "category_2"]
    )

# 8.0 JOINING DATA ----

orderlines_df = pd.read_excel("00_data_raw/orderlines.xlsx")
bikes_df = pd.read_excel("00_data_raw/bikes.xlsx")

# Merge (Joining)

pd.merge(
    left=orderlines_df,
    right=bikes_df,
    left_on="product.id",
    right_on="bike.id"
)

# Concatenate (Binding)

# Rows

df_1 = df.head(5)
df_2 = df.tail(5)

pd.concat([df_1, df_2], axis=0)

# Columns

df_1 = df.iloc[:, :5]
df_2 = df.iloc[:, -5:]

pd.concat([df_1, df_2], axis=1)

# 9.0 SPLITTING (SEPARATING) COLUMNS AND COMBINING (UNITING) COLUMNS

# Separate

df_2 = df['order_date'].astype('str').str.split("-", expand=True) \
    .set_axis(["year", "month", "day"], axis=1)

df_2

pd.concat([df, df_2], axis=1)

# Combine

df_2

df_2['year'] + "-" + df_2['month'] + "-" + df_2['day']


# 10.0 APPLY
# - Apply functions across rows

sales_cat2_daily_df = df[['category_2', 'order_date', 'total_price']] \
    .set_index('order_date') \
    .groupby('category_2') \
    .resample('D') \
    .sum()

sales_cat2_daily_df

np.mean([1, 2, 3])  # Aggregations

np.sqrt([1, 2, 3])  # Transformation

sales_cat2_daily_df.apply(np.mean)

sales_cat2_daily_df.apply(np.sqrt)

sales_cat2_daily_df.apply(np.mean, result_type="broadcast")
sales_cat2_daily_df.apply(lambda x: np.repeat(np.mean(x), len(x)))

sales_cat2_daily_df \
    .groupby('category_2') \
    .apply(np.mean)

sales_cat2_daily_df \
    .groupby('category_2') \
    .apply(lambda x: np.repeat(np.mean(x), len(x)))

# Grouped Broadcast - Use Transform
sales_cat2_daily_df \
    .groupby('category_2') \
    .transform(np.mean)

sales_cat2_daily_df \
    .groupby('category_2') \
    .transform(np.sqrt)


# 11.0 PIPE
# - Functional programming helper for "data" functions

data = df


def add_column(data, **kwargs):

    data_copy = data.copy()

    # print(kwargs)

    data_copy[list(kwargs.keys())] = pd.DataFrame(kwargs)

    return data_copy


add_column(df, total_price_2=df.total_price * 2)

df \
    .pipe(
        add_column,
        category_2_lower=df['category_2'].str.lower(),
        category_2_upper=df['category_2'].str.upper()
    )
