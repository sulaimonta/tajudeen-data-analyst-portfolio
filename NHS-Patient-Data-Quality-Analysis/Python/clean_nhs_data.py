import pandas as pd

# ==========================================================
# 1. LOAD ORIGINAL DATA
# ==========================================================

file_path = "NHS_patient_records.xlsx"
df = pd.read_excel(file_path)

print(f"Original records: {len(df)}")

# ==========================================================
# 2. STANDARDISE GENDER
# ==========================================================

df["Gender"] = df["Gender"].replace({
    "M": "Male",
    "F": "Female"
})

# ==========================================================
# 3. CONVERT DATE COLUMNS
# ==========================================================

df["Admission_Date"] = pd.to_datetime(
    df["Admission_Date"],
    errors="coerce"
)

df["Discharge_Date"] = pd.to_datetime(
    df["Discharge_Date"],
    errors="coerce"
)

# ==========================================================
# 4. CREATE DATE QUALITY FLAG
# ==========================================================

df["Date_Quality_Flag"] = "Valid"

df.loc[
    df["Discharge_Date"] < df["Admission_Date"],
    "Date_Quality_Flag"
] = "Invalid"

# ==========================================================
# 5. NHS NUMBER QUALITY FLAG
# ==========================================================

df["NHS_Number_Missing"] = df["NHS_Number"].isna()

df["NHS_Number_Duplicate"] = (
    df["NHS_Number"].notna()
    & df["NHS_Number"].duplicated(keep=False)
)

# ==========================================================
# 6. MISSING DATA FLAGS
# ==========================================================

df["Gender_Missing"] = df["Gender"].isna()

df["Postcode_Missing"] = df["Postcode"].isna()

df["GP_Practice_Missing"] = df["GP_Practice"].isna()

df["Diagnosis_Code_Missing"] = df["Diagnosis_Code"].isna()

# ==========================================================
# 7. OVERALL DATA QUALITY FLAG
# ==========================================================

df["Data_Quality_Status"] = "Good"

quality_problem = (
    (df["Date_Quality_Flag"] == "Invalid")
    | df["NHS_Number_Missing"]
    | df["NHS_Number_Duplicate"]
    | df["Gender_Missing"]
    | df["Postcode_Missing"]
    | df["GP_Practice_Missing"]
    | df["Diagnosis_Code_Missing"]
)

df.loc[quality_problem, "Data_Quality_Status"] = "Review"

# ==========================================================
# 8. SAVE CLEANED DATA
# ==========================================================

output_file = "NHS_patient_records_cleaned.csv"

df.to_csv(
    output_file,
    index=False
)

# ==========================================================
# 9. SUMMARY
# ==========================================================

print()
print("===== CLEANING SUMMARY =====")

print(f"Total records: {len(df)}")

print(
    f"Invalid date records: "
    f"{(df['Date_Quality_Flag'] == 'Invalid').sum()}"
)

print(
    f"Missing NHS Numbers: "
    f"{df['NHS_Number_Missing'].sum()}"
)

print(
    f"Duplicate NHS Number records: "
    f"{df['NHS_Number_Duplicate'].sum()}"
)

print(
    f"Missing Gender: "
    f"{df['Gender_Missing'].sum()}"
)

print(
    f"Missing Postcode: "
    f"{df['Postcode_Missing'].sum()}"
)

print(
    f"Missing GP Practice: "
    f"{df['GP_Practice_Missing'].sum()}"
)

print(
    f"Missing Diagnosis Code: "
    f"{df['Diagnosis_Code_Missing'].sum()}"
)

print(
    f"Records requiring review: "
    f"{(df['Data_Quality_Status'] == 'Review').sum()}"
)

print()
print(f"Cleaned file saved to: {output_file}")
print()
print("Process completed successfully.")