You are tasked with building the data processing pipeline for a configuration manager. The system tracks file size changes across servers and generates a stream of JSON logs. Your goal is to write a C program that calculates a rolling Z-score (standardization) of these configuration sizes to detect anomalies, and set up a pipeline to process them.

**Step 1: Fix the JSON Library**
We have vendored the `cJSON` library source code in `/app/cJSON-1.7.15`.
However, the `Makefile` is broken. An intern accidentally removed the `-fPIC` flag from the compiler options, causing the shared library build (`make cJSON.so`) to fail with relocation errors.
1. Fix the `Makefile` in `/app/cJSON-1.7.15` so that `libcjson.so` builds successfully.
2. Run `make` to build the shared library.

**Step 2: C Implementation**
Write a C program at `/home/user/config_tracker.c` that parses a JSON Lines file.
Compile it to `/home/user/config_tracker`, linking against the fixed `libcjson.so` in `/app/cJSON-1.7.15`.
The program must:
1. Accept two arguments: `<input_jsonl> <output_csv>`.
2. Read the input line by line. Each line is a JSON object: `{"timestamp": 1690000000, "file": "/etc/nginx/nginx.conf", "size": 4096}`.
3. Maintain a **single global rolling window** of the last `10` configuration `size` values seen. If fewer than 10 values have been processed, use all values seen so far.
4. For each incoming log, after adding its size to the window:
   - Calculate the moving average ($\mu$) of the current window.
   - Calculate the population standard deviation ($\sigma$) of the current window (divide by $N$, not $N-1$).
   - Calculate the normalized Z-score of the *current* size: $Z = \frac{size - \mu}{\sigma}$. If $\sigma = 0$, then $Z = 0.0$.
5. Write the result to the output CSV in the format: `timestamp,z_score` (with `z_score` formatted to 6 decimal places, e.g., `1690000000,1.200000`).
   - The CSV should have a header: `timestamp,z_score`.

**Step 3: Pipeline & Cron Management**
1. Write a bash script at `/home/user/process_logs.sh` that executes `/home/user/config_tracker /home/user/config_logs.jsonl /home/user/anomalies.csv`. Ensure the script is executable and sets `LD_LIBRARY_PATH` correctly so the C program can find `libcjson.so`.
2. Install a crontab for the `user` account that runs `/home/user/process_logs.sh` every 5 minutes (e.g., `*/5 * * * *`).

We have provided a sample input file at `/home/user/config_logs.jsonl` for you to test your implementation. Note that for final verification, your program will be evaluated on a much larger, hidden dataset.