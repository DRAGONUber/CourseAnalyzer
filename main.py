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

# Search by Professor
def search_by_professor(professor):
    all_df[['Last Name', 'First Name']] = all_df['Primary Instructor'].str.split(',', expand=True)
    all_df['Last Name'] = all_df['Last Name'].str.strip()
    all_df['First Name'] = all_df['First Name'].str.strip()
    professor_df = all_df[
        all_df['Last Name'].str.contains(professor, case=False, na=False) |
        all_df['First Name'].str.contains(professor, case=False, na=False)
    ]

    return professor_df

def search_by_course(course, num):
    course_df = all_df[(all_df['CRS SUBJ CD'] == course) & (all_df['CRS NBR'] == num)]

    return course_df


















