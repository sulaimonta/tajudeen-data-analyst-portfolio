import pandas as pd

# Load NHS dataset
file_path = "NHS_patient_records.xlsx"
df = pd.read_excel(file_path)

print("===== DUPLICATE & CONSISTENCY VALIDATION =====")
print(f"Total records: {len(df)}")
print()

# --------------------------------------------------
# 1. Duplicate Patient IDs
# --------------------------------------------------

duplicate_patient_ids = df[df["Patient_ID"].duplicated(keep=False)]

print("===== DUPLICATE PATIENT IDs =====")

if duplicate_patient_ids.empty:
    print("No duplicate Patient IDs found.")
else:
    print(duplicate_patient_ids[
        ["Patient_ID"]
    ].sort_values("Patient_ID").to_string(index=False))

print(f"Duplicate Patient ID records: {len(duplicate_patient_ids)}")
print()


# --------------------------------------------------
# 2. Duplicate NHS Numbers
# --------------------------------------------------

duplicate_nhs = df[
    df["NHS_Number"].notna() &
    df["NHS_Number"].duplicated(keep=False)
]

print("===== DUPLICATE NHS NUMBERS =====")

if duplicate_nhs.empty:
    print("No duplicate NHS Numbers found.")
else:
    print(
        duplicate_nhs[
            ["Patient_ID", "NHS_Number"]
        ].sort_values("NHS_Number").to_string(index=False)
    )

print(f"Duplicate NHS Number records: {len(duplicate_nhs)}")
print()


# --------------------------------------------------
# 3. Duplicate complete records
# --------------------------------------------------

duplicate_rows = df[df.duplicated(keep=False)]

print("===== DUPLICATE COMPLETE RECORDS =====")

if duplicate_rows.empty:
    print("No duplicate complete records found.")
else:
    print(duplicate_rows.to_string(index=False))

print(f"Duplicate complete records: {len(duplicate_rows)}")
print()


# --------------------------------------------------
# 4. Admission and Discharge Date Consistency
# --------------------------------------------------

df["Admission_Date"] = pd.to_datetime(
    df["Admission_Date"],
    errors="coerce"
)

df["Discharge_Date"] = pd.to_datetime(
    df["Discharge_Date"],
    errors="coerce"
)

invalid_dates = df[
    df["Discharge_Date"] < df["Admission_Date"]
]

print("===== DATE CONSISTENCY =====")

print(
    f"Records where Discharge Date is before Admission Date: "
    f"{len(invalid_dates)}"
)

if invalid_dates.empty:
    print("No date consistency issues found.")
else:
    print(
        invalid_dates[
            [
                "Patient_ID",
                "Admission_Date",
                "Discharge_Date",
                "Department"
            ]
        ].head(20).to_string(index=False)
    )

print()


# --------------------------------------------------
# 5. Overall consistency summary
# --------------------------------------------------

print("===== CONSISTENCY SUMMARY =====")

print(f"Duplicate Patient IDs: {df['Patient_ID'].duplicated().sum()}")

print(
    f"Duplicate NHS Numbers: "
    f"{df['NHS_Number'].notna().sum() - df['NHS_Number'].dropna().nunique()}"
)

print(f"Duplicate complete records: {df.duplicated().sum()}")

print(
    f"Invalid admission/discharge dates: "
    f"{len(invalid_dates)}"
)

print()
print("Process completed successfully.")