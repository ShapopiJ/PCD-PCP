# Precipitation Concentration Degree (PCD) & Precipitaiton Concentration Period Calculator

## Overview
_________________

This is a python implementation for the calculation of the PCD and PCP for monthly rainfall data. I did not find anyone who shared an implementation so here you go. It is very basic and needs much work.

I found exactly 3 papers that reference these indicators, however the indicators are quite intuitive and I am surprised they are not used more. They help you find out if and where most rainfall is in an area is concentrated throughout the year. This implementation is based on the paper by [Xuemei Li et al](https://www.researchgate.net/publication/230282840_Spatial_and_temporal_variability_of_precipitation_concentration_index_concentration_degree_and_concentration_period_Xinjiang_China).

## Basic Usage

• Download the pcd_pcp.py file or clone the repo\
• Import modules and load monthly precipitation data
```python
import pandas as pd
from pcd_pcp import precip
monthly = pd.read_csv("file")
```
The function expects the data to be a pandas dataframe that has monthly data.

• Initialize the precip class

```python
data = precip(df = monthly)
```
The above assumes your Date Time column has the name "Date Time". You can change this behaviour by explicitly giving the DateTime column name. Use the `datetime_col` argument when initializing the class.

• Now we calculate the PCP using the `PCP()` function

```python
PCP = data.PCP()
```

• You can calculate the PCD with the `PCD()` function
```python
PCD = data.PCD()
```

At this point you have pandas dataframes that you can do what you want with.

You can cite this project in your work:
```BibTex
@misc {pcp_pcd,
     author = "Jimmy Shapopi",
     title  = "PCP_PCD, an open source Python library providing reference implementations of the precipitation conentration degree and period",
     url    = "https://github.com/ShapopiJ/PCD-PCP",
     month  = "June",
     year   = "2023--"
}
```

To do:

[ ] Better documentation


