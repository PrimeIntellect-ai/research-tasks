You are tasked with helping a backup administrator safely archive rapidly rotating log files. 

We have a proprietary logging binary located at `/app/log_writer`. This stripped binary rapidly writes structured JSON log entries to `/home/user/logs/active.log`. Every few milliseconds, the binary rotates the log by moving `active.log` to `rotated.log` (overwriting the old rotated log) and creates a new `active.log`. To prevent data corruption, `/app/log_writer` acquires an exclusive `flock` on the file before writing or rotating.

The JSON logs look like this:
`{"seq": 1024, "data": "480065006c006c006f00"}`

The `data` field contains a hex-encoded string representing UTF-16LE characters. 

Your objective is to write a C++ program, `archiver.cpp`, that:
1. Runs concurrently with the `log_writer`.
2. Safely reads the log entries from `/home/user/logs/active.log` and `/home/user/logs/rotated.log` without missing records due to the rapid rotation race condition. You MUST use file locking (`flock` with `LOCK_SH`) to synchronize access with the writer.
3. Parses the JSON data.
4. Converts the hex-encoded UTF-16LE `data` string into standard UTF-8 text.
5. Appends the parsed and converted records to a CSV file at `/home/user/archive.csv` in the format: `seq,utf8_text`.

Requirements:
- Compile your program to `/home/user/archiver` (use `g++ -O3 -std=c++17`).
- Create a bash script `/home/user/run_test.sh` that:
  - Clears the `/home/user/logs` directory.
  - Starts `/app/log_writer /home/user/logs` in the background.
  - Starts your `/home/user/archiver /home/user/logs /home/user/archive.csv` in the background.
  - Waits for `/app/log_writer` to finish (it automatically exits after 5 seconds).
  - Kills the archiver cleanly.

We will run your `run_test.sh` script and verify the integrity of `/home/user/archive.csv`. Because of the aggressive rotation, missing a few records is possible, but your solution must capture at least 95% of the generated logs.