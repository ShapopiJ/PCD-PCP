import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go

def get_degree(string):
    deg, minute, sec = string[1:].split("⁰")[0], string[1:].split("⁰")[-1].split("'")[0], string[1:].split("⁰")[-1].split("'")[-1][:-1]
    #print(minute)
    degree = float(deg) + float(minute)/60 + float(sec)/3600
    if string[0] == "S":
        return degree*-1
    return degree

def load_dst(file = "Rainfall_DST_Prod4.csv", set_index=True):
    dst = pd.read_csv(file)
    dst["Date Time"] = pd.to_datetime(dst["Date Time"])
    dst1 = dst.set_index("Date Time")
    if set_index:
        return dst1
    else:
        return dst
    

def get_avg_with_loc(dst):
    """
    Takes a dataset with all our sites and whatever data. Then returns a dataframe with the averages of whatever was in the dataset. This is done percolumn
    """
    locations = pd.read_excel("Final Locality Data.xlsx", usecols=(0,2,3), names=["Place", "Lat", "Long"], skiprows=2)
    locations["Lat"] = locations["Lat"].astype(str)
    locations["Long"] = locations["Long"].astype(str)
    locations["Lat (D)"] = locations["Lat"].apply(get_degree)
    locations["Long (D)"] = locations["Long"].apply(get_degree)
    places = list(dst.columns)
    places_new = [place.split("_")[-1] for place in places]
    dst.columns = places_new
    mean = pd.DataFrame(dst.mean(), columns=['Average'])
    dst2 = pd.merge(mean, locations, left_index=True, right_on="Place", how="inner")
    print(len(mean))
    return dst2

def plot_index(df: pd.DataFrame, date_col: str, precip_col: str, save_file: str=None,
               index_type: str='SPI', bin_width: int=22):

    pos_index = df.loc[df[precip_col] >= 0]
    neg_index = df.loc[df[precip_col] < 0]

    fig, ax = plt.subplots()
    ax.bar(pos_index[date_col], pos_index[precip_col], width=bin_width, align='center', color='b')
    ax.bar(neg_index[date_col], neg_index[precip_col], width=bin_width, align='center', color='r')
    ax.grid(True)
    ax.set_xlabel("Date")
    ax.set_ylabel(index_type)
    #ax.set_xticklabels(ax.get_xticks(), rotation = 45)

    if save_file:
        plt.savefig(save_file, dpi=400)

    return fig

def plot_html(df, col):
    pos_index = df.loc[df[col] >= 0]
    neg_index = df.loc[df[col] < 0]
    fig  = go.Figure()

    fig.add_trace(go.Bar(
        x = pos_index.index,
        y = pos_index[col],
        marker_color = "blue",
        name="unusual wet"
    ))
    fig.add_trace(go.Bar(
        x = neg_index.index,
        y = neg_index[col],
        marker_color = "red",
        name="unusual drought"
    ))
    return fig