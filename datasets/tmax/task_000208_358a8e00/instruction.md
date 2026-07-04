You are an AI assistant helping a data scientist process a messy dataset of user feedback. The raw data was exported in a custom text format where records often span multiple lines, breaking standard CSV parsers. 

Your task is to write a C program that reads this custom format, extracts the relevant features, computes a rolling statistic, logs errors, and outputs a clean CSV file.

**Input Data**
The raw data is located at: `/home/user/raw_dataset.txt`
The file contains records separated by the exact line: `---RECORD---`

Each record contains key-value pairs separated by a colon and a space (`: `). The keys are `ID` and `Date`. The `Text` key is special: its value starts on the same line, but can span multiple subsequent lines until the next `---RECORD---` marker or the end of the file.

**Processing Requirements**
Write a C program at `/home/user/processor.c`, compile it to `/home/user/processor`, and run it. The program must:

1. **Structured Information Extraction:**
   Parse each record to extract the `ID`, `Date`, and `Text`.
   
2. **Data Cleaning & Transformation:**
   For the `Text` field, replace all embedded newline characters (`\n`) with a single space character (` `). Do not add a space at the very end of the text if the text ended right before the `---RECORD---` line.

3. **Validation & Logging (Pipeline Monitoring):**
   A valid record must contain an `ID`, a `Date`, and a non-empty `Text` field (at least one character).
   If a record is missing any of these, skip it entirely and append the exact line `ERROR: Skipped invalid record.` to `/home/user/pipeline.log`.

4. **Rolling Statistics Computation:**
   For every *valid* record, calculate the length (number of characters) of the cleaned `Text` string. Maintain a running average of this length across all valid records processed so far.

5. **Template-based Text Generation (CSV Output):**
   Output the valid, cleaned records to `/home/user/cleaned.csv`.
   The first line must be the header: `ID,Date,Text,RollingAvgLen`
   For each valid record, append a line with the extracted fields. The `RollingAvgLen` should be printed as a floating-point number formatted to exactly 2 decimal places.

**Example Input Record:**
```
---RECORD---
ID: 101
Date: 2023-10-01
Text: This is a
multi-line
review.
```

**Expected Example CSV Output Row:**
`101,2023-10-01,This is a multi-line review.,28.00`

Ensure your compiled program reads `/home/user/raw_dataset.txt` and generates both `/home/user/cleaned.csv` and `/home/user/pipeline.log`.