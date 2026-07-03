You are a data analyst setting up an automated pipeline to process text logs. Incoming data is in a CSV file, but it contains mixed character encodings and messy text. You need to write a C++ program to process the data, perform a rolling mathematical aggregation, and set up the scripts to automate this via cron.

Here are the requirements:

1. **Input File**: `/home/user/data/input.csv`. The file has no header and two columns: `timestamp` (format `YYYY-MM-DD HH:MM:SS`) and `message_text`. The text may contain non-ASCII characters.

2. **C++ Processing**:
   Write a C++ program (saved to `/home/user/process.cpp`) that reads `input.csv`.
   For each row:
   a. **Tokenization & Normalization**: Strip out all non-alphanumeric characters (keep only A-Z, a-z, and 0-9) and spaces. Convert all letters to lowercase. Treat spaces as token delimiters. Any non-ASCII bytes should be completely removed/ignored.
   b. **Line Statistic ($L_i$)**: Calculate the average length of the tokens in the message. If the line has no valid tokens, $L_i = 0$.
   c. **Rolling Aggregation ($R_i$)**: Calculate a windowed rolling average of the line statistics $L_i$ over a window size of 3 (the current line and up to 2 previous lines). 
      - For row 1: $R_1 = L_1$
      - For row 2: $R_2 = (L_1 + L_2) / 2$
      - For row $i \ge 3$: $R_i = (L_{i-2} + L_{i-1} + L_i) / 3$

3. **Output Format**:
   The C++ program must output a CSV file to `/home/user/output.csv` with exactly two columns (no header): `timestamp` and `rolling_avg`. The `rolling_avg` must be formatted to exactly 2 decimal places (e.g., `3.50`).

4. **Pipeline Execution**:
   - Write a shell script `/home/user/run_pipeline.sh` that compiles `process.cpp` (using `g++`) and then runs the compiled executable. Make sure it has execute permissions.
   - You must manually run `./run_pipeline.sh` to produce `/home/user/output.csv` for verification.
   - Write a cron expression to `/home/user/cron.txt` that schedules `/home/user/run_pipeline.sh` to run exactly every 15 minutes. The file should contain only the single crontab line.