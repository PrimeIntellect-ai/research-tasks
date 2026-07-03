You are acting as a system configuration manager. We receive raw, messy configuration backups from various servers that need to be cleaned and tracked.

Raw configuration files are located in `/home/user/raw_configs/`.

Your task is to implement a cleaner tool in C++ and set up an automated processing pipeline.

Step 1: Write a C++ program at `/home/user/cleaner.cpp`.
The program should read from standard input line-by-line and write to standard output. It must perform the following operations on each line:
1. Use Regular Expressions (e.g., `std::regex`) to remove any comments. A comment starts with the `#` character and continues to the end of the line.
2. Trim all leading and trailing whitespace from the line.
3. Ignore (do not output) any lines that become completely empty after the above steps.
4. Deduplicate the lines: only output the *first* occurrence of any normalized line. If a line has been seen before in the same file, skip it.

Compile your program using:
`g++ -std=c++17 /home/user/cleaner.cpp -o /home/user/cleaner`

Step 2: Write a bash script at `/home/user/process.sh`.
This script should:
1. Ensure the directory `/home/user/clean_configs/` exists.
2. Iterate over every file in `/home/user/raw_configs/`.
3. Pass the contents of each file through your compiled `/home/user/cleaner` executable.
4. Save the output into `/home/user/clean_configs/` using the exact same base filename.
Make sure the script has executable permissions. Run it once to process the existing files.

Step 3: Schedule the pipeline.
Create a file named `/home/user/cron.txt` containing exactly one crontab line that schedules `/home/user/process.sh` to run every 15 minutes (i.e., at minutes 0, 15, 30, and 45 of every hour). Do not actually install the crontab; just create the file.