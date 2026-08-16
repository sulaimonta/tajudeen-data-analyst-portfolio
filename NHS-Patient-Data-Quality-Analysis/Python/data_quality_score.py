import pandas as pd

# ==========================================================
# LOAD DATA
# ==========================================================

file_path = "NHS_patient_records.xlsx"
df = pd.read_excel(file_path)

total_records = len(df)

# ==========================================================
# STANDARDISE GENDER
# ==========================================================

df["Gender"] = df["Gender"].replace({
    "M": "Male",
    "F": "Female"
})

# ==========================================================
# 1. COMPLETENESS SCORE
# ==========================================================

total_missing = df.isna().sum().sum()
total_cells = df.shape[0] * df.shape[1]

completeness_score = (
    1 - (total_missing / total_cells)
) * 100

# ==========================================================
# 2. VALIDITY SCORE
# ==========================================================

# Date validity
df["Admission_Date"] = pd.to_datetime(
    df["Admission_Date"],
    errors="coerce"
)

df["Discharge_Date"] = pd.to_datetime(
    df["Discharge_Date"],
    errors="coerce"
)

invalid_dates = (
    df["Discharge_Date"] < df["Admission_Date"]
).sum()

date_validity = (
    1 - invalid_dates / total_records
) * 100


# NHS Number format validity
def valid_nhs_number(value):
    if pd.isna(value):
        return True

    value = str(value).replace(".0", "")

    return value.isdigit() and len(value) == 10


invalid_nhs = (
    ~df["NHS_Number"].apply(valid_nhs_number)
).sum()

nhs_validity = (
    1 - invalid_nhs / total_records
) * 100


# Patient ID validity
def valid_patient_id(value):
    if pd.isna(value):
        return False

    value = str(value)

    return (
        len(value) == 7
        and value.startswith("P")
        and value[1:].isdigit()
    )


invalid_patient_ids = (
    ~df["Patient_ID"].apply(valid_patient_id)
).sum()

patient_id_validity = (
    1 - invalid_patient_ids / total_records
) * 100


# Gender validity
valid_genders = ["Male", "Female"]

invalid_gender = (
    df["Gender"].notna()
    & ~df["Gender"].isin(valid_genders)
).sum()

gender_validity = (
    1 - invalid_gender / total_records
) * 100


# Department validity
valid_departments = [
    "A&E",
    "Cardiology",
    "Orthopaedics",
    "Outpatients",
    "Radiology",
    "Surgery"
]

invalid_department = (
    ~df["Department"].isin(valid_departments)
).sum()

department_validity = (
    1 - invalid_department / total_records
) * 100


# Appointment Status validity
valid_statuses = [
    "Completed",
    "Cancelled",
    "Missed"
]

invalid_status = (
    ~df["Appointment_Status"].isin(valid_statuses)
).sum()

status_validity = (
    1 - invalid_status / total_records
) * 100


# Overall validity score
validity_score = (
    date_validity
    + nhs_validity
    + patient_id_validity
    + gender_validity
    + department_validity
    + status_validity
) / 6

# ==========================================================
# 3. UNIQUENESS SCORE
# ==========================================================

duplicate_patient_ids = df["Patient_ID"].duplicated().sum()

duplicate_nhs_numbers = (
    df["NHS_Number"].notna()
    & df["NHS_Number"].duplicated()
).sum()

duplicate_complete_records = df.duplicated().sum()

total_duplicate_issues = (
    duplicate_patient_ids
    + duplicate_nhs_numbers
    + duplicate_complete_records
)

uniqueness_score = (
    1 - total_duplicate_issues / total_records
) * 100

# ==========================================================
# 4. CONSISTENCY SCORE
# ==========================================================

consistency_issues = invalid_dates

consistency_score = (
    1 - consistency_issues / total_records
) * 100

# ==========================================================
# 5. OVERALL DATA QUALITY SCORE
# ==========================================================

overall_score = (
    completeness_score * 0.25
    + validity_score * 0.25
    + uniqueness_score * 0.25
    + consistency_score * 0.25
)

# ==========================================================
# DISPLAY RESULTS
# ==========================================================

print("=" * 55)
print("        NHS DATA QUALITY SCORE")
print("=" * 55)

print(f"Total records: {total_records}")
print()

print("===== DATA QUALITY DIMENSIONS =====")

print(f"Completeness Score: {completeness_score:.2f}%")
print(f"Validity Score:     {validity_score:.2f}%")
print(f"Uniqueness Score:   {uniqueness_score:.2f}%")
print(f"Consistency Score:  {consistency_score:.2f}%")

print()

print("===== OVERALL DATA QUALITY SCORE =====")

print(f"Overall Score: {overall_score:.2f}%")

print()

print("===== VALIDITY DETAILS =====")

print(f"Date Validity:          {date_validity:.2f}%")
print(f"NHS Number Validity:    {nhs_validity:.2f}%")
print(f"Patient ID Validity:    {patient_id_validity:.2f}%")
print(f"Gender Validity:        {gender_validity:.2f}%")
print(f"Department Validity:    {department_validity:.2f}%")
print(f"Appointment Status:     {status_validity:.2f}%")

print()

print("===== DATA QUALITY ISSUES =====")

print(f"Missing cells: {total_missing}")
print(f"Invalid date relationships: {invalid_dates}")
print(f"Duplicate Patient IDs: {duplicate_patient_ids}")
print(f"Duplicate NHS Number occurrences: {duplicate_nhs_numbers}")
print(f"Duplicate complete records: {duplicate_complete_records}")

print()

print("Process completed successfully.")