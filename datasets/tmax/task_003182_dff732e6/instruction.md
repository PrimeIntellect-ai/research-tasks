You are an AI assistant helping a scientific researcher process and organize a messy dataset with mixed encodings.

The researcher has a directory `/home/user/dataset_raw/` containing a configuration file and several CSV files saved in different character encodings by various instruments.

Your task involves writing a C program to process this data, followed by a bash script to manage backups.

**Step 1: Install Dependencies**
You may install any standard C libraries or tools using `sudo apt-get` (e.g., `libcjson-dev` for JSON parsing, or compiler tools). Note: While the prompt mentions `sudo`, you can use `sudo` for `apt-get` as this environment permits standard package installation. (Assume passwordless sudo for `apt-get`).

**Step 2: C Program for Data Processing**
Write a C program and save it to `/home/user/process_data.c`. The program must do the following:
1. Parse the JSON configuration file located at `/home/user/dataset_raw/config.json`. The JSON is an array of objects, each containing `"filename"` (a string) and `"encoding"` (a string).
2. Iterate through each file specified in the JSON. The files are located in `/home/user/dataset_raw/`.
3. Read each file and use the POSIX `<iconv.h>` library to convert its contents from the specified `"encoding"` into `UTF-8` in memory.
4. Parse the converted CSV data. The CSV has a header row. Find the column named exactly `Measurement`.
5. Sum all the float values in the `Measurement` column for that file.
6. Append the result to `/home/user/dataset_processed/summary.txt` (create the directory and file if they don't exist). The output format for each file must be exactly: `[filename]: [sum]`, with the sum formatted to exactly one decimal place (e.g., `%.1f`). Include a newline character at the end of each line.

Compile your program using `gcc /home/user/process_data.c -o /home/user/process_data -lcjson` (or whichever JSON library you chose to install/use), and run it.

**Step 3: Incremental Backup Script**
Write a bash script at `/home/user/backup.sh`. When executed, this script must:
1. Ensure the directory `/home/user/backup/` exists.
2. Use `tar` to create an incremental backup of the `/home/user/dataset_processed/` directory.
3. The backup archive must be saved in `/home/user/backup/` with the naming format `backup_$(date +%s).tar.gz`.
4. Use a GNU `tar` listed-incremental snapshot file located exactly at `/home/user/backup/snapshot.snar`.
5. Execute the script once to generate the first backup archive and the snapshot file.

Ensure all directories referenced exist or are created by your code. Your final state should have the compiled executable, the `summary.txt` file, the `backup.sh` script, the `snapshot.snar` file, and exactly one `.tar.gz` archive in the backup directory.