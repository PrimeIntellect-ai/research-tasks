You are an ETL data engineer debugging a pipeline that produces duplicate records due to retry mechanisms. You have a large input file containing user records that has been corrupted by these retries. 

Your task is to write a C program that streams this file, converts its character encoding, deduplicates adjacent records based on string similarity, and writes the cleaned data to an output file.

Here are the requirements:

1. **Input File**: The input data is located at `/home/user/data/input.csv`. 
   - It is a comma-separated file with three columns: `ID,Name,Role`.
   - The file is encoded in **ISO-8859-1** (Latin-1).
   - The file is large, so your program MUST process it in a streaming fashion (read line by line). Do not load the entire file into memory.

2. **Processing & Encoding**:
   - Convert the data from ISO-8859-1 to **UTF-8** during processing.
   - You may use standard POSIX libraries (like `iconv`) for encoding conversion.

3. **Deduplication Logic**:
   - The retry bug causes near-duplicate records to appear consecutively.
   - For every row, calculate the **Levenshtein distance** of the `Name` field against the `Name` field of the *last kept* (emitted) record.
   - **Crucial**: The Levenshtein distance must be calculated based on **Unicode characters (code points)**, not raw UTF-8 bytes. For example, replacing 'é' with 'e' is a distance of 1.
   - If the Levenshtein distance between the current `Name` and the last kept `Name` is $\le 1$, the current record is considered a duplicate and must be **dropped**.
   - The very first record is always kept.

4. **Output File**:
   - Write the deduplicated records to `/home/user/data/output.csv`.
   - The output must be valid **UTF-8**.
   - Include the exact original formatting (including commas and newlines).

5. **Implementation**:
   - Write your C code in `/home/user/dedup.c`.
   - Compile it to an executable at `/home/user/dedup` (e.g., `gcc -O2 /home/user/dedup.c -o /home/user/dedup`).
   - Run your program to generate `/home/user/data/output.csv`.

Once the `output.csv` file is generated, your task is complete.