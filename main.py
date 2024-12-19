import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import os
import ratemyprofessor

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

def search_by_course_and_professor(course, num, professor):
    course_df = all_df[(all_df['CRS SUBJ CD'] == course) & (all_df['CRS NBR'] == num) & (search_by_professor(professor))]

    return course_df


def main():
    print('UIC Course Analyzer')
    print('1 - Search by Professor')
    print('2 - Search by Course')
    print('0 - quit')
    num = int(input('Enter Number: '))

    if num == 1:
        professor_name = input('Enter Professor: ')
        school_name = "University of Illinois Chicago"
        school = ratemyprofessor.get_school_by_name(school_name)
        if not school:
            print("School not found in RMP.")
        rmp_professor = ratemyprofessor.get_professor_by_school_and_name(school, professor_name)
        if rmp_professor:
            print("\nRate My Professor Data:")
            print(f"Name: {rmp_professor.name}")
            print(f"Rating: {rmp_professor.rating}/5")
            print(f"Difficulty: {rmp_professor.difficulty}/5")
            print(f"Would Take Again: {rmp_professor.would_take_again:.2f}%")
            print(f"Number of Ratings: {rmp_professor.num_ratings}")
        else:
            print(f"No RMP data found for professor {professor_name}.")
        
        df = search_by_professor(professor_name)
        unique_courses = df[['CRS SUBJ CD', 'CRS NBR']].drop_duplicates()
        print(f"A list of {professor_name} courses:")
        for lab, row in unique_courses.iterrows():
            print(f"{row['CRS SUBJ CD']} {row['CRS NBR']}")
    if num == 2:
        course = input('Enter department: ')
        course_num = int(input('Enter course number: '))
        df = search_by_course_and_professor(course, course_num)









    


if __name__ == '__main__':
    main()
