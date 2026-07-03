You are a storage administrator managing disk space on a Linux server. Your task is to create a fast log archiving tool in C++ that filters multi-line log files based on a configuration file, writes the output atomically to prevent data corruption, and outputs statistics.

Write a C++ program at `/home/user/archiver.cpp` and compile it to `/home/user/archiver`.

The program must meet the following requirements:
1. **Configuration File Interpretation:** The program must open and read `/home/user/rules.conf`. This file contains key-value pairs separated by an equals sign (`=`). You must extract the values for `TARGET_LEVEL` and `ARCHIVE_FILE`.
2. **Multi-line Log Parsing:** The program must read log data from `stdin`. 
   - A new log entry always starts with a timestamp enclosed in brackets, followed by a space, the log level, a space, and the message (e.g., `[2023-10-25 14:00:00] CRITICAL Process crashed:`).
   - Any line that does NOT start with `[` is considered a continuation of the previous log entry.
3. **Filtering:** The program must identify all complete log entries (including their continuation lines) where the log level exactly matches the `TARGET_LEVEL` specified in the config file.
4. **Atomic Writes:** The program must write all matching log entries to the `ARCHIVE_FILE` path atomically. To do this safely, you must write the data to a temporary file named `<ARCHIVE_FILE>.tmp` and then rename it to `<ARCHIVE_FILE>` using a system rename call.
5. **Standard Stream Redirection:** The program must output exactly one integer to `stdout` representing the total number of matched log *entries* (not lines).

Once you have written and compiled the program, execute it by piping the provided log file `/home/user/system.log` into it, and redirect the output to `/home/user/count.txt` like this:
`cat /home/user/system.log | /home/user/archiver > /home/user/count.txt`