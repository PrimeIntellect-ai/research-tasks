You are acting as a backup administrator archiving data. We have a noisy log generator script that outputs continuous logs to standard output. Your task is to write a C program that archives this live data into manageable chunks without losing any lines.

Please complete the following steps:
1. Review the configuration file located at `/home/user/archiver.conf`. It contains a single integer representing the maximum number of lines each archive chunk should contain.
2. Write a C program located at `/home/user/log_archiver.c` that:
   - Reads the integer `N` from `/home/user/archiver.conf`.
   - Reads text line-by-line from `stdin`.
   - Writes the incoming lines to chunk files in the directory `/home/user/archives/`.
   - The chunk files must be named `archive_part_NNN.log` where `NNN` is a 1-indexed, zero-padded 3-digit number (e.g., `archive_part_001.log`, `archive_part_002.log`).
   - Each chunk file should contain exactly `N` lines, except possibly the last one which may contain fewer.
3. Compile your C program into an executable at `/home/user/log_archiver`.
4. We have provided a log generator script at `/home/user/generate_logs.sh`. Execute this script and pipe its standard output directly into your `log_archiver` program.

Ensure the `/home/user/archives/` directory contains exactly the partitioned log files after the run.