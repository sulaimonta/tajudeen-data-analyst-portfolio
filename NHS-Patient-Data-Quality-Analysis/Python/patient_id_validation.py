import pandas as pd
import re

# Load dataset
file_path = "NHS_patient_records.xlsx"
df = pd.read_excel(file_path)

# Convert Patient ID to string
patient_id = df["Patient_ID"].astype("string").str.strip()

# -----------------------------
# PATIENT ID VALIDATION
# -----------------------------

# 1. Missing Patient IDs
missing_ids = patient_id.isna() | (patient_id == "")

# 2. Correct format: P followed by exactly 6 digits
valid_format = patient_id.str.fullmatch(r"P\d{6}", na=False)

# 3. Invalid format
invalid_ids = (~missing_ids) & (~valid_format)

# 4. Duplicate Patient IDs
duplicate_ids = (
    patient_id.notna()
    & patient_id.duplicated(keep=False)
)

# -----------------------------
# SUMMARY
# -----------------------------

total_records = len(df)

print("\n===== PATIENT ID VALIDATION =====")

print(f"Total records: {total_records}")

print(f"Missing Patient IDs: {missing_ids.sum()}")
print(
    f"Missing percentage: "
    f"{missing_ids.mean() * 100:.2f}%"
)

print(f"Invalid Patient ID format: {invalid_ids.sum()}")
print(
    f"Invalid percentage: "
    f"{invalid_ids.mean() * 100:.2f}%"
)

print(f"Duplicate Patient IDs: {duplicate_ids.sum()}")
print(
    f"Duplicate percentage: "
    f"{duplicate_ids.mean() * 100:.2f}%"
)

# -----------------------------
# INVALID PATIENT IDs
# -----------------------------

invalid_records = df.loc[
    invalid_ids,
    ["Patient_ID"]
]

print("\n===== INVALID PATIENT IDs =====")

if len(invalid_records) > 0:
    print(invalid_records.to_string(index=False))
else:
    print("No invalid Patient ID formats found.")

# -----------------------------
# DUPLICATE PATIENT IDs
# -----------------------------

duplicate_records = df.loc[
    duplicate_ids,
    ["Patient_ID"]
]

print("\n===== DUPLICATE PATIENT IDs =====")

if len(duplicate_records) > 0:
    print(duplicate_records.to_string(index=False))
else:
    print("No duplicate Patient IDs found.")

print("\nProcess completed successfully.")