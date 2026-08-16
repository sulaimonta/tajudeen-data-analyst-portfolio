import pandas as pd

# Load dataset
file_path = "NHS_patient_records.xlsx"
df = pd.read_excel(file_path)

print("\n===== NHS DATA QUALITY: DATE VALIDATION =====")

# Convert dates to datetime
df["Admission_Date"] = pd.to_datetime(
    df["Admission_Date"],
    errors="coerce"
)

df["Discharge_Date"] = pd.to_datetime(
    df["Discharge_Date"],
    errors="coerce"
)

# Find records where discharge is before admission
invalid_dates = df[
    df["Discharge_Date"] < df["Admission_Date"]
]

# Count invalid records
invalid_count = len(invalid_dates)

# Calculate percentage
invalid_percentage = (
    invalid_count / len(df)
) * 100

print(
    "Invalid admission/discharge records:",
    invalid_count
)

print(
    "Invalid date percentage:",
    round(invalid_percentage, 2),
    "%"
)

# Display the problematic records
print("\nInvalid Records:")

print(
    invalid_dates[
        [
            "Patient_ID",
            "Admission_Date",
            "Discharge_Date",
            "Department"
        ]
    ].to_string(index=False)
)