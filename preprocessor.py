import pandas as pd
import numpy as np

# data1 = pd.read_csv("athlete_events.csv")
# data2 = pd.read_csv("noc_regions.csv")

def preprocess(data1, data2):
    # global data1, data2
    data1 = data1[data1['Season']=="Summer"]
    data1 = data1.merge(data2, on="NOC", how="left")
    data1.drop_duplicates(inplace=True)
    medals = pd.get_dummies(data1['Medal'])
    data1 = pd.concat([data1, medals], axis=1)
    return data1
