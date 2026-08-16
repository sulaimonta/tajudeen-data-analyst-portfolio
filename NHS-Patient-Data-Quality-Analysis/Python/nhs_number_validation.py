import pandas as pd

# Load dataset
file_path = "NHS_patient_records.xlsx"
df = pd.read_excel(file_path)

# Convert NHS Number to string while preserving missing values
nhs_number = (
    df["NHS_Number"]
    .apply(lambda x: str(int(x)) if pd.notna(x) else pd.NA)
    .astype("string")
    .str.strip()
)

# -----------------------------
# NHS NUMBER VALIDATION
# -----------------------------

# 1. Missing NHS Numbers
missing_nhs = nhs_number.isna() | (nhs_number == "")

# 2. Check numeric format
numeric_nhs = nhs_number.str.fullmatch(r"\d{10}", na=False)

# 3. Invalid NHS Numbers
invalid_nhs = (~missing_nhs) & (~numeric_nhs)

# 4. Duplicate NHS Numbers
duplicate_nhs = (
    nhs_number.notna()
    & nhs_number.duplicated(keep=False)
)

# -----------------------------
# SUMMARY
# -----------------------------

total_records = len(df)

print("\n===== NHS NUMBER VALIDATION =====")

print(f"Total records: {total_records}")

print(f"Missing NHS Numbers: {missing_nhs.sum()}")
print(
    f"Missing percentage: "
    f"{missing_nhs.mean() * 100:.2f}%"
)

print(f"Invalid NHS Number format: {invalid_nhs.sum()}")
print(
    f"Invalid percentage: "
    f"{invalid_nhs.mean() * 100:.2f}%"
)

print(f"Duplicate NHS Number records: {duplicate_nhs.sum()}")
print(
    f"Duplicate percentage: "
    f"{duplicate_nhs.mean() * 100:.2f}%"
)

# -----------------------------
# SHOW INVALID RECORDS
# -----------------------------

invalid_records = df.loc[
    invalid_nhs,
    ["Patient_ID", "NHS_Number"]
]

print("\n===== INVALID NHS NUMBERS =====")

if len(invalid_records) > 0:
    print(invalid_records.to_string(index=False))
else:
    print("No invalid NHS Number formats found.")

# -----------------------------
# SHOW DUPLICATES
# -----------------------------

duplicate_records = df.loc[
    duplicate_nhs,
    ["Patient_ID", "NHS_Number"]
]

print("\n===== DUPLICATE NHS NUMBERS =====")

if len(duplicate_records) > 0:
    print(duplicate_records.to_string(index=False))
else:
    print("No duplicate NHS Numbers found.")