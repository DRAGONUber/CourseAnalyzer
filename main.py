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




# def test_search_by_professor():
#     print("Testing search_by_professor function...")

#     # Test case: Search for "Kobotis"
#     professor_name = "Kobotis"
#     print(f"Searching for professor: {professor_name}")

#     # Call the function
#     try:
#         results = search_by_professor(professor_name)
#         if results.empty:
#             print(f"No grade data found for professor {professor_name}.")
#         else:
#             print("\nGrade Distribution Data:")
#             print(results)

#         # Fix: Ensure the `school` object is used here
#         school_name = "University of Illinois Chicago"
#         school = ratemyprofessor.get_school_by_name(school_name)
#         if not school:
#             print("School not found in RMP.")
#             return

#         # Use the school object, not the school name string
#         rmp_professor = ratemyprofessor.get_professor_by_school_and_name(school, professor_name)
#         if rmp_professor:
#             print("\nRate My Professor Data:")
#             print(f"Name: {rmp_professor.name}")
#             print(f"Rating: {rmp_professor.rating}")
#             print(f"Difficulty: {rmp_professor.difficulty}")
#             print(f"Would Take Again: {rmp_professor.would_take_again}")
#             print(f"Number of Ratings: {rmp_professor.num_ratings}")
#         else:
#             print(f"No RMP data found for professor {professor_name}.")
#     except Exception as e:
#         print(f"An error occurred during the test: {e}")

# # Run the test
# test_search_by_professor()




def search_by_course(course, num):
    course_df = all_df[(all_df['CRS SUBJ CD'] == course) & (all_df['CRS NBR'] == num)]

    return course_df


def main():
    print('UIC Course Analyzer')
    print('1 - Search by Professor')
    print('2 - Search by Course')
    print('0 - quit')

    


if __name__ == '__main__':
    





















    # professor_name = 'Kobotus'
    # school_name = "University of Illinois Chicago"
    # school = ratemyprofessor.get_school_by_name(school_name)
    # if not school:
    #     print("School not found in RMP.")
        

    # # Use the school object, not the school name string
    # rmp_professor = ratemyprofessor.get_professor_by_school_and_name(school, professor_name)
    # if rmp_professor:
    #     print("\nRate My Professor Data:")
    #     print(f"Name: {rmp_professor.name}")
    #     print(f"Rating: {rmp_professor.rating}/5")
    #     print(f"Difficulty: {rmp_professor.difficulty}/5")
    #     print(f"Would Take Again: {rmp_professor.would_take_again:.2f}%")
    #     print(f"Number of Ratings: {rmp_professor.num_ratings}")
    # else:
    #     print(f"No RMP data found for professor {professor_name}.")





















