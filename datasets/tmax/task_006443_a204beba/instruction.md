You are a data analyst setting up an automated, multi-stage data processing pipeline to sanitize and process application log files. You need to write two C++ programs and a Bash orchestration script to process a set of CSV files containing log data.

The system should process CSV files located in `/home/user/input/`. 
Each CSV file has the following columns (no header row):
`ID,Date,Level,Message`

Your task has three components:

1. **Validation Checkpoint (C++)**: 
   Create a C++ program named `/home/user/validator.cpp` (and compile it to `/home/user/validator`). It should take three arguments: `<input_dir> <accepted_dir> <rejected_dir>`.
   For each `.csv` file in the input directory, it must validate every row based on these rules:
   - `ID` must be exactly 5 alphanumeric characters.
   - `Date` must be exactly 10 characters long (format YYYY-MM-DD, e.g., 2023-10-15).
   - `Level` must be exactly one of: `INFO`, `WARN`, `ERROR`.
   If a file has *any* invalid rows, move the file to `<rejected_dir>`. If all rows in a file are valid, move it to `<accepted_dir>`.

2. **Text Transformation (C++)**:
   Create a C++ program named `/home/user/cleaner.cpp` (and compile it to `/home/user/cleaner`). It should take two arguments: `<accepted_dir> <output_file>`.
   It must read all `.csv` files in `<accepted_dir>`. For each row, extract the `ID` and `Message` fields. You must remove all HTML-like tags (anything enclosed in `<` and `>`, including the brackets themselves) from the `Message` field. 
   Write the results to `<output_file>` in the format: `ID,Cleaned_Message`. The output must be sorted alphabetically by `ID`.

3. **Orchestration & Logging (Bash)**:
   Create a bash script at `/home/user/pipeline.sh`. This script must:
   - Create the directories `/home/user/accepted`, `/home/user/rejected`, `/home/user/output`, and `/home/user/logs` if they don't exist.
   - Write a log file to `/home/user/logs/pipeline.log`.
   - Log the message "START: Validation" before running the validator.
   - Run the `validator` program.
   - Log the message "START: Cleaning" before running the cleaner (saving output to `/home/user/output/consolidated.csv`).
   - Run the `cleaner` program.
   - Log the message "END: Pipeline complete".
   *(Ensure the pipeline script is executable).*

Write, compile, and execute the pipeline script. Your final verification will rely on the correct contents of `/home/user/output/consolidated.csv`, the state of the accepted/rejected directories, and the pipeline log.