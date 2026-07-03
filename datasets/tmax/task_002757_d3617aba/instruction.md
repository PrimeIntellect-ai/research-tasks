You are a database administrator dealing with a corrupted graph database export. An index corruption caused the system to output "stale" and phantom edges alongside valid data. 

Your task requires you to clean the data, write a robust filter in C, and run analytical queries on the cleaned dataset.

**Step 1: Identify the Corruption Signature**
There is an image file at `/app/corruption_rule.png`. It is a screenshot of a DBA's notes that contains the exact mathematical condition identifying the "stale" edges. You must extract this rule (you can use `tesseract`). 

**Step 2: Build the Data Sanitizer (C Language)**
Write a C program at `/home/user/filter_edges.c` and compile it to `/home/user/filter_edges`. 
The program must take a single command-line argument (the path to a CSV file) and output ONLY the valid rows to `stdout`.
The CSV format is: `source_id,target_id,weight,timestamp` (all integers, with a header row).
Your program MUST preserve the header row. It must evaluate each subsequent row and drop any row that matches the corruption signature found in the image.

*Note: Your compiled `/home/user/filter_edges` binary will be tested against a strict verification corpus.*
- Clean corpus: Contains only valid edges. Your program must preserve these exactly.
- Evil corpus: Contains ONLY corrupted/stale edges. Your program must reject all of these (outputting only the header).

**Step 3: Clean the Main Graph and Analyze**
1. Apply your `/home/user/filter_edges` program to the main raw export located at `/app/raw_graph.csv` and save the output to `/home/user/cleaned_graph.csv`.
2. Write an SQLite script at `/home/user/analyze.sql` that does the following:
   - Creates a table `edges (source_id INT, target_id INT, weight INT, timestamp INT)`.
   - Imports `/home/user/cleaned_graph.csv` into this table.
   - Uses a SQL Window Function to rank the targets for each `source_id` ordered by `weight` DESCENDING. (If weights are equal, order by `target_id` ASCENDING).
   - Projects a final result with columns: `source_id, target_id, weight, rank`.
   - Filters the results to only include rows where `rank <= 3` (the top 3 heaviest edges per source).
   - Sorts the final result globally by `source_id` ASC, `rank` ASC.
   - Applies pagination to retrieve exactly 15 rows starting from row 10 (i.e., OFFSET 10 LIMIT 15).
3. Execute this SQL script against a new database `/home/user/graph.db` and output the results (with headers) to `/home/user/final_report.csv`.

Ensure your C code is efficient and cleanly handles standard file I/O.