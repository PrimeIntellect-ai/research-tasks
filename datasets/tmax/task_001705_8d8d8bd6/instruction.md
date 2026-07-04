You are a log analyst for a legacy system. The system dumps raw event logs in a custom binary format. You need to write a C program to parse, clean, normalize, and resample these logs, extracting specific features. Finally, you must set up an automated pipeline script and a cron schedule for this job.

**Step 1: Write the Log Processor in C**
Create a C program at `/home/user/process_logs.c` that reads a binary file `/home/user/logs.bin` and outputs a CSV file to `/home/user/output.csv`.

**Binary File Format (`logs.bin`):**
The file consists of sequentially packed records (no padding). Every record has:
1. `timestamp`: 8 bytes, unsigned 64-bit integer, little-endian. (Unix epoch seconds)
2. `encoding`: 1 byte, unsigned 8-bit integer. `0` means UTF-8, `1` means UTF-16LE.
3. `msg_len`: 2 bytes, unsigned 16-bit integer, little-endian. The length of the `message` payload in bytes.
4. `message`: `msg_len` bytes. If `encoding` is `1` (UTF-16LE), you must convert it to a standard ASCII/UTF-8 string. You can safely assume that any UTF-16LE string in this file only contains characters in the standard ASCII range (so every second byte is `0x00` and can simply be dropped for basic conversion).

**Processing Rules:**
1. **Deduplication:** As you iterate through the records sequentially, drop any record whose decoded message string is identical to the *most recently accepted* record's decoded message.
2. **Feature Extraction:** For each accepted record, extract the `Event_Type`, which is defined as the first word of the message (all characters up to the first space character `' '`). If there is no space, the entire message is the `Event_Type`.
3. **Resampling & Gap Filling:** We need the output to have exactly one record per 60-second interval. 
   - Start your 60-second buckets precisely at the timestamp of the *very first record* in the file (`T_start`).
   - The buckets are intervals: `[T_start, T_start+60)`, `[T_start+60, T_start+120)`, etc.
   - Continue generating buckets until you process the bucket that contains the *last* record in the file.
   - If a bucket contains one or more accepted records, output ONLY the *first* accepted record that falls into this bucket.
   - If a bucket contains NO accepted records, output a gap-fill record where the timestamp is the start of that bucket, the `Event_Type` is `GAP`, and the message is `MISSING`.

**Output Format (`/home/user/output.csv`):**
The output must be a standard CSV file with the following header:
`Timestamp,Event_Type,Message`
Followed by the resampled rows. For standard rows, the `Timestamp` should be the start of the 60-second bucket, NOT the original timestamp of the record.

**Step 2: Automation Setup**
1. Write a shell script `/home/user/run_pipeline.sh` that compiles `/home/user/process_logs.c` (using `gcc`) and executes the resulting binary.
2. Create a file `/home/user/crontab.txt` containing exactly one cron expression line that schedules `/home/user/run_pipeline.sh` to run every 5 minutes. Use standard cron syntax.

Execute your pipeline script once to generate the `output.csv`.