import pandas as pd

# Load NHS dataset
file_path = "NHS_patient_records.xlsx"
df = pd.read_excel(file_path)

# Standardise Gender first
df["Gender"] = df["Gender"].replace({
    "M": "Male",
    "F": "Female"
})

# Calculate missing values
missing_count = df.isnull().sum()
missing_percentage = (missing_count / len(df)) * 100

# Create summary table
missing_summary = pd.DataFrame({
    "Column": df.columns,
    "Missing_Values": missing_count.values,
    "Missing_Percentage": missing_percentage.values
})

# Keep columns with missing values
missing_summary = missing_summary[
    missing_summary["Missing_Values"] > 0
]

print("===== MISSING VALUE VALIDATION =====")
print(f"Total records: {len(df)}")
print()

if missing_summary.empty:
    print("No missing values found.")
else:
    print(missing_summary.to_string(index=False))