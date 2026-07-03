You are an AI assistant helping a data scientist clean and process a clinical trial dataset. The pipeline involves data masking, validation, wide-to-long reshaping, and database bulk importing, orchestrated via a Makefile. 

We have a raw dataset located at `/home/user/workspace/clinical_data.csv`.
It contains the following columns (wide format):
`ID,FullName,Email,M1_BP,M2_BP,M3_BP`

Your task is to build an automated pipeline using C, Makefile, and SQLite3 to process this data. 

Here are the specific requirements:

1. **C Program (`/home/user/workspace/cleaner.c`)**:
   Write a C program that takes two arguments: input CSV path and output CSV path (e.g., `./cleaner input.csv output.csv`).
   The program must:
   - Read the input CSV.
   - **Anonymize PII**: 
     - Replace `FullName` with Initials (e.g., "Alice Smith" becomes "AS", "Bob Jones" becomes "BJ"). Assume names are at most two words separated by a space.
     - Replace `Email` strictly with the literal string `[REDACTED]`.
   - **Reshape (Wide to Long)**: Convert the three blood pressure columns (`M1_BP`, `M2_BP`, `M3_BP`) into two columns: `Month` (integer 1, 2, or 3) and `BP`. 
   - **Validation Checkpoint**: Only output rows where the `BP` value is greater than 0. If a specific month's BP is missing, 0, or negative, drop that month's record for that patient (do not output a row for it).
   - The output CSV must have the header: `ID,Initials,Email,Month,BP`.

2. **Database Schema (`/home/user/workspace/schema.sql`)**:
   Write a SQL script to create a SQLite table named `bp_log` with the following schema:
   `ID INTEGER, Initials TEXT, Email TEXT, Month INTEGER, BP INTEGER`

3. **Orchestration (`/home/user/workspace/Makefile`)**:
   Create a Makefile to define the DAG orchestration with the following targets:
   - `build`: Compiles `cleaner.c` into an executable named `cleaner` using `gcc`.
   - `process`: Depends on `build`. Runs `./cleaner /home/user/workspace/clinical_data.csv /home/user/workspace/clean_data.csv`.
   - `db_setup`: Applies `schema.sql` to a new SQLite database at `/home/user/workspace/patients.db`.
   - `load`: Depends on `process` and `db_setup`. Bulk imports `/home/user/workspace/clean_data.csv` into the `bp_log` table in `/home/user/workspace/patients.db`. Use the SQLite `.import` command with CSV mode, skipping the header.
   - `all`: The default target. Depends on `load`.

Ensure that you install any necessary system packages (like `sqlite3`, `build-essential`) before executing the Makefile. Run `make all` to execute the full pipeline. Do not leave the final database file empty.