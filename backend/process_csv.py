import os
import pandas as pd
from datetime import datetime
from app import app, db
from models import GradeDistribution  # Ensure this model exists
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def process_csv_files():
    directory = "/Users/shauryaiyer/Documents/GitHub/CourseAnalyzer/Grade_Distributions"
    
    # List to hold DataFrames
    dfs = []
    
    # Iterate over CSV files in the directory
    for file in os.listdir(directory):
        if file.endswith(".csv"):
            file_name = os.path.splitext(file)[0]  # Remove .csv extension
            try:
                term, year = file_name.split()
            except ValueError:
                print(f"Filename '{file}' does not match the 'Term Year.csv' format. Skipping.")
                continue
            
            file_path = os.path.join(directory, file)
            try:
                df = pd.read_csv(file_path)
            except Exception as e:
                print(f"Error reading '{file}': {e}")
                continue
            
            # Add Term and Year columns
            df['Term'] = term
            df['Year'] = year
            
            # Optional: Rename columns to match database schema if necessary
            df.rename(columns={
                "CRS SUBJ CD": "course_subject",
                "CRS NBR": "course_number",
                "Primary Instructor": "instructor",
                "A": "grade_a",
                "B": "grade_b",
                "C": "grade_c",
                "D": "grade_d",
                "F": "grade_f"
            }, inplace=True)
            
            # Select relevant columns
            df = df[['Term', 'Year', 'course_subject', 'course_number', 'instructor', 'grade_a', 'grade_b', 'grade_c', 'grade_d', 'grade_f']]
            
            dfs.append(df)
            print(f"Processed '{file}' successfully.")
    
    if not dfs:
        print("No CSV files were processed.")
        return
    
    # Concatenate all DataFrames
    all_data = pd.concat(dfs, ignore_index=True)
    
    # Insert data into the database
    with app.app_context():
        for index, row in all_data.iterrows():
            grade_entry = GradeDistribution(
                term=row['Term'],
                year=row['Year'],
                course_subject=row['course_subject'],
                course_number=row['course_number'],
                instructor=row['instructor'],
                grade_a=row['grade_a'],
                grade_b=row['grade_b'],
                grade_c=row['grade_c'],
                grade_d=row['grade_d'],
                grade_f=row['grade_f']
            )
            db.session.add(grade_entry)
            if index % 1000 == 0 and index > 0:
                try:
                    db.session.commit()
                    print(f"Committed {index} records.")
                except Exception as e:
                    print(f"Error committing records at index {index}: {e}")
                    db.session.rollback()
        
        # Commit any remaining records
        try:
            db.session.commit()
            print("All records have been committed successfully.")
        except Exception as e:
            print(f"Error committing records: {e}")
            db.session.rollback()

if __name__ == "__main__":
    process_csv_files()
