import pandas as pd
import numpy as np
df = pd.read_excel("/content/student data.xlsx")  # Fixed file path
#print(df.to_string(index=False))
pass_mark = int(input("enter the pass marks for each subject: "))
min_attendence = float(input("enter the minimum attendence percent: "))
is_pass = (
    (df['s1'] >= pass_mark) &
    (df['s2'] >= pass_mark) &
    (df['s3'] >= pass_mark) &
    (df['s4'] >= pass_mark) &
    (df['s5'] >= pass_mark) &
    (df['s6'] >= pass_mark) &
    (df['attendence'] >= min_attendence)
)
# calculating average marks of students
df['Average Marks'] = df[['s1', 's2', 's3', 's4', 's5', 's6']].mean(axis=1)
# Define Grading System Conditions
grade_conditions = [
    (df['Average Marks'] >= 90),
    (df['Average Marks'] >= 80) & (df['Average Marks'] < 90),
    (df['Average Marks'] >= 70) & (df['Average Marks'] < 80),
    (df['Average Marks'] >= 60) & (df['Average Marks'] < 70),
    (df['Average Marks'] < 60)
]
# Define Grade Labels
grade_labels = ['A', 'B', 'C', 'D', 'E']
# Assign Grades dynamically
df['Grade'] = np.select(grade_conditions, grade_labels, default='fail')
# Use np.where to assign 'pass' if True, and 'fail' if False for each row
df['Result'] = np.where(is_pass, 'pass', 'fail')
# Safely set Grade to 'fail' where is_pass is False
df['Grade'] = np.where(~is_pass, 'fail', df['Grade'])
# Print the results with the student names
#print(df[['name', 'Result']].to_string(index=False))
#print complete dataframe
print(df.to_string(index=False))
# --- NEW: Generate Student Descriptions ---
print("\n" + "="*50)
print("STUDENT PERFORMANCE DESCRIPTIONS")
print("="*50)

for index, row in df.iterrows():
    name = row['name']
    avg_marks = round(row['Average Marks'], 2)
    attendance = row['attendence']
    result = row['Result']
    grade = row['Grade']
    
    # Identify failed components
    failed_subjects = []
    for sub in ['s1', 's2', 's3', 's4', 's5', 's6']:
      if row[sub] < pass_mark:
            failed_subjects.append(sub.upper())
            
    low_attendance = attendance < min_attendence

    # Construct the description string
    if result == 'pass':
        description = f"{name} passed with an average score of {avg_marks}% and earned a Grade '{grade}'. Attendance was satisfactory at {attendance}%."
    else:
        reasons = []
        if failed_subjects:
            reasons.append(f"failing in {', '.join(failed_subjects)}")
        if low_attendance:
            reasons.append(f"shortage of attendance ({attendance}% out of minimum {min_attendence}%)")
        
        description = f"{name} failed due to { ' and '.join(reasons) }. The student's overall average marks were {avg_marks}%."

    print(f"- {description}")
    print()
    #top student
    top_student_idx = df['Average Marks'].idxmax()
    top_student_name = df.loc[top_student_idx, 'name']
    top_student_avg = round(df.loc[top_student_idx, 'Average Marks'], 2)
print(f"TOP PERFORMING STUDENT: {top_student_name} with an Average of {top_student_avg}%")
