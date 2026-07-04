You are an automation specialist tasked with creating a C-based data processing workflow to handle multi-language telemetry logs from global edge servers. 

We have a raw log file located at `/home/user/raw_logs.txt`. The logs contain timestamps, region codes, and multi-language UTF-8 status messages that embed a CPU metric.

The input data is already chronologically sorted. Each line in the file follows this exact format:
`YYYY-MM-DD HH:MM:SS | REGION | [UTF-8 Message] CPU:[XX]%`

Example lines:
`2023-10-01 14:02:15 | JP | サーバーのステータスは正常です CPU:45%`
`2023-10-01 14:08:30 | US | System operating normally CPU:52%`
`2023-10-01 14:15:00 | JP | 警告: 高負荷 CPU:89%`
`2023-10-01 14:16:10 | ES | Operación exitosa CPU:30%`

Your task is to write a C program named `/home/user/process_logs.c` that compiles to `/home/user/process_logs`. The program must read `/home/user/raw_logs.txt` and perform the following operations:
1. **Timestamp Parsing & Alignment**: Parse the timestamp (assumed UTC) and convert it to a Unix epoch integer.
2. **Structured Extraction**: Extract the integer CPU percentage from the end of the UTF-8 message.
3. **Stratified Sampling**: We only want the *first* recorded log entry per `REGION` for every 10-minute window. A 10-minute window starts at the top of the hour (e.g., 14:00:00 to 14:09:59 is one window, 14:10:00 to 14:19:59 is the next).
4. **Output**: Write the sampled data to a CSV file at `/home/user/sampled_metrics.csv`.

The output CSV must have the following exact header and format:
`WindowEpoch,Region,CPU_Percent`
`1696168800,JP,45`
`1696168800,US,52`

Requirements:
- Write the C code and compile it using `gcc`.
- Run the compiled executable to produce the output file.
- The C program must handle standard C libraries and properly process the UTF-8 text (you can treat it as a byte stream to scan for `CPU:`).
- You may use standard POSIX functions like `strptime` and `mktime` for time parsing.

Create the C program, compile it, and generate the final `sampled_metrics.csv`.