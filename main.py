import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import os


directory = "/Users/shauryaiyer/Documents/GitHub/CourseAnalyzer/Grade_Distributions"

dfs = []


for file in os.listdir(directory):
    if file.endswith(".csv"):
        file_name = os.path.splitext(file)[0]
        term, year = file_name.split()
        df = pd.read_csv(os.path.join(directory, file))
        df['Term'] = term
        df['Year'] = year
        dfs.append(df)

all_df = pd.concat(dfs, ignore_index=True)

print(all_df.columns)





