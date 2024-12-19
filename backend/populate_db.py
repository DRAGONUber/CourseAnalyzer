import os
import pandas as pd
from app import app, db
from models import GradeDistribution
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def populate_db():
    with app.app_context():
        # Path to your CSV directory
        directory = "../Grade_Distributions"

        # Verify if the directory exists
        if not os.path.exists(directory):
            print(f"Directory {directory} does not exist.")
            exit(1)

        # Initialize a counter for total entries
        total_entries = 0

        # Loop through each CSV file in the directory
        for file in os.listdir(directory):
            if file.endswith(".csv"):
                filepath = os.path.join(directory, file)
                print(f"Processing file: {filepath}")
                try:
                    data = pd.read_csv(filepath)
                    print(f"Read {len(data)} rows from {file}")
                except Exception as e:
                    print(f"Error reading {file}: {e}")
                    continue

                # Iterate over the rows in the DataFrame
                for index, row in data.iterrows():
                    # Print progress every 1000 rows to reduce console spam
                    if index % 1000 == 0:
                        print(f"Processing row {index} in {file}")

                    try:
                        # Map CSV columns to model fields
                        grade_entry = GradeDistribution(
                            term=row.get("SCHED TYPE DESC"),  # Assuming 'SCHED TYPE DESC' represents the term
                            year=row.get("SESS CD"),           # Assuming 'SESS CD' represents the year/session
                            course_subject=row.get("CRS SUBJ CD"),
                            course_number=row.get("CRS NBR"),
                            instructor=row.get("Primary Instructor"),
                            grade_a=row.get("A"),
                            grade_b=row.get("B"),
                            grade_c=row.get("C"),
                            grade_d=row.get("D"),
                            grade_f=row.get("F"),
                        )
                        db.session.add(grade_entry)
                        total_entries += 1
                    except Exception as e:
                        print(f"Error processing row {index} in {file}: {e}")
                        continue

        # Commit all changes to the database
        print(f"Committing {total_entries} entries to the database...")
        try:
            db.session.commit()
            print("Database populated successfully!")
        except Exception as e:
            print(f"Error during commit: {e}")
            db.session.rollback()

if __name__ == "__main__":
    populate_db()
