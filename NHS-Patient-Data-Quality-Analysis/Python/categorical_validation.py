import pandas as pd

# Load dataset
file_path = "NHS_patient_records.xlsx"
df = pd.read_excel(file_path)

print("\n===== CATEGORICAL DATA VALIDATION =====")

# Columns to check
categorical_columns = [
    "Gender",
    "Department",
    "Appointment_Status"
]

# Expected values
expected_values = {
    "Gender": [
        "Male",
        "Female",
        "Other",
        "Unknown"
    ],

    "Department": [
        "A&E",
        "Cardiology",
        "Outpatients",
        "Orthopaedics",
        "Radiology",
        "Surgery"
    ],

    "Appointment_Status": [
        "Completed",
        "Cancelled",
        "Missed"
    ]
}

# Check each categorical column
for column in categorical_columns:

    print(f"\n===== {column.upper()} =====")

    # Show all values and their counts
    print("\nValue counts:")
    print(df[column].value_counts(dropna=False))

    # Identify unexpected values
    unexpected = df[
        ~df[column].isin(expected_values[column])
        & df[column].notna()
    ]

    print("\nUnexpected values:")

    if len(unexpected) > 0:
        print(
            unexpected[column]
            .value_counts()
            .to_string()
        )
    else:
        print("No unexpected values found.")

    # Missing values
    missing = df[column].isna().sum()

    print(f"\nMissing values: {missing}")

print("\nProcess completed successfully.")
# Standardise Gender values
df["Gender"] = df["Gender"].replace({
    "M": "Male",
    "F": "Female"
})
print("\n===== CLEANED GENDER =====")
print(df["Gender"].value_counts(dropna=False))