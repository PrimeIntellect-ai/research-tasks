You are a data engineer tasked with building an efficient ETL and statistical analysis pipeline in C. You have received a raw TSV log file at `/home/user/raw.tsv`. The file contains server log data with the following tab-separated columns:
`user_id` (string), `item_id` (string), `rating` (integer), `latency_ms` (float)

Your goal is to write a C program that filters this data, calculates a specific statistical metric (hypothesis testing), and a bash script that ensures pipeline reproducibility.

Step 1: Write an ETL and Analysis Program in C
Create a C program at `/home/user/etl.c`. The program should read `/home/user/raw.tsv` line by line and perform the following:
1. **Filtering (ETL):** 
   - Discard any row where `latency_ms` is strictly less than 10.0 or strictly greater than 5000.0.
   - Discard any row where `rating` is not 1, 2, 3, 4, or 5.
   - Write the filtered rows (preserving the exact formatting and tab separation) to a file named `clean.tsv` in the current working directory.

2. **Hypothesis Testing:**
   Using ONLY the filtered data, calculate a two-sample Z-test statistic to compare the mean latency of positive interactions vs negative interactions.
   - **Group 1 (Positive):** Records where `rating >= 4`.
   - **Group 2 (Negative):** Records where `rating < 4`.
   - Formula for Z-statistic: `Z = (mean1 - mean2) / sqrt( (var1 / n1) + (var2 / n2) )`
   - Use the **sample variance** (dividing by n - 1) for `var1` and `var2`.
   - Write the absolute value of the calculated Z-statistic to a file named `z_stat.txt` in the current working directory, formatted to exactly 3 decimal places (e.g., `12.345`).

Step 2: Write a Reproducibility Pipeline
Create a bash script at `/home/user/pipeline.sh` that does the following:
1. Compiles `/home/user/etl.c` using `gcc` into an executable named `run_etl`. Use standard optimization (`-O2`) and link the math library (`-lm`).
2. Runs `./run_etl`, renaming the output `clean.tsv` to `clean_run1.tsv`.
3. Runs `./run_etl` a second time, renaming the output `clean.tsv` to `clean_run2.tsv`.
4. Compares `clean_run1.tsv` and `clean_run2.tsv` using the `md5sum` utility.
5. If the MD5 checksums match exactly, echo `Reproducible` into `/home/user/run_log.txt`. If they do not match, echo `Failed` into `/home/user/run_log.txt`.

Constraints:
- You must write the C code yourself; do not rely on external libraries other than the C Standard Library (`stdio.h`, `stdlib.h`, `string.h`, `math.h`).
- The maximum line length in the TSV is 256 characters. 
- You can assume the data has enough rows in both groups to compute variance (n > 1).