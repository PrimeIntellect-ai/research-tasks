You are a data engineer tasked with building an ETL pipeline that processes user records. The data is large, so you need to process it in parallel using a combination of a bash orchestration script and a custom C program for the fast data transformations.

The raw data is located at `/home/user/input.csv` and has the following columns:
`id,name,email,ssn,country`

Your objective is to write a C program and a Bash script that processes this file according to the following pipeline requirements:

**1. Transform & Sample (C Program: `/home/user/transform.c`)**
Write a C program that reads a CSV without a header from `stdin` and writes the transformed CSV to `stdout`.
For each row, it must:
- **Sample:** Drop the row entirely if the `id` is an even number. Only output rows with odd `id`s.
- **Normalize:** Convert the `email` field entirely to lowercase.
- **Mask:** Mask the `ssn` field by replacing the first three digits and the two digits after the first hyphen with 'X'. (e.g., `123-45-6789` becomes `XXX-XX-6789`).
You can assume standard valid formatting for the input rows (no commas inside fields) and a maximum line length of 1024 bytes. Compile this program to `/home/user/transform`.

**2. Pipeline Orchestration & Deduplication (Bash Script: `/home/user/pipeline.sh`)**
Write a bash script that performs the following steps:
- Extracts the header from `/home/user/input.csv` and writes it to a new file `/home/user/output.csv`.
- Splits the remaining data (excluding the header) into multiple chunks.
- Processes these chunks **in parallel** by piping each chunk through your compiled `./transform` C program.
- Merges the transformed results.
- **Deduplicates** the merged results based on the `email` column. If multiple rows have the same email address, keep only the row with the lowest `id`.
- Sorts the final deduplicated data numerically by `id` in ascending order.
- Appends the sorted, deduplicated records to `/home/user/output.csv`.

Once you have written both the C program and the bash script, run `/home/user/pipeline.sh` so that `/home/user/output.csv` is fully generated.

Ensure your script is executable and paths are absolute or correctly relative to `/home/user`. Do not use external C libraries outside of the standard POSIX C library.