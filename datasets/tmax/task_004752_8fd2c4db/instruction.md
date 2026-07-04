You are a data analyst tasked with processing a batch of international customer feedback files. The files are located in `/home/user/customer_feedback/`. Because these files come from different regional offices, they have different character encodings and contain messy data that violates our data governance policies. 

You need to write a Python script that reads all CSV files in the directory, processes them according to the rules below, and produces two consolidated CSV files: `/home/user/processed_data.csv` (for valid, cleaned records) and `/home/user/rejected_data.csv` (for invalid records).

Here are the requirements for your script:

**1. Character Encoding Handling:**
* The input directory contains CSV files encoded in UTF-8, ISO-8859-1 (Latin-1), and UTF-16.
* Your script must correctly read all of them without crashing or corrupting special characters (e.g., accents like 'é' or 'ö').
* The output files (`processed_data.csv` and `rejected_data.csv`) must be strictly encoded in `utf-8`.

**2. Data Validation (Constraint-based):**
Each file has the following header: `id,name,email,phone,rating,comments`
A row is considered **VALID** only if it meets ALL the following constraints:
* `id`: Must be a non-empty string composed strictly of digits (e.g., "123").
* `email`: Must contain exactly one `@` symbol, and at least one `.` after the `@`.
* `rating`: Must be an integer between 1 and 5 (inclusive).

If a row violates *any* of these constraints, it should be considered **INVALID** and written to `rejected_data.csv` without any masking applied.

**3. Data Masking & Anonymization:**
For all **VALID** rows, you must apply the following masking rules before writing them to `processed_data.csv`:
* `email`: Mask the username portion (everything before the `@`) with `***`. Keep the domain intact. Example: `john.doe@example.com` becomes `***@example.com`.
* `phone`: Mask all characters (including digits, dashes, or spaces) except the last 4 characters with `*`. If the phone string is 4 characters or shorter, do not mask it. If it is empty, leave it empty. Example: `555-123-4567` becomes `********4567`.
* `name`: Leave as is.
* `comments`: Leave as is.

**Output Requirements:**
* Both output files must be comma-separated, include the exact header `id,name,email,phone,rating,comments`, and use standard CSV quoting (where needed).
* Write the valid, masked rows to `/home/user/processed_data.csv`.
* Write the raw, unmasked invalid rows to `/home/user/rejected_data.csv`.
* You may install Python libraries such as `pandas` or `chardet` using `pip` if you wish, but the standard library is also sufficient.