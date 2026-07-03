You are a data analyst working with an automated data ingestion system. You need to build a C++ data processing tool and a bash pipeline to normalize messy customer names, match them against a master list using string similarity, and simulate fetching/pushing data from remote directories.

Here is the setup:
- A "remote" input directory exists at `/home/user/remote_in/` containing a file `data.csv` (Format: `ID,RawName`).
- A master list of valid names exists at `/home/user/master_list.txt` (one name per line, already lowercase and normalized).
- A "remote" output directory exists at `/home/user/remote_out/`.

Your tasks:

1. **C++ String Matcher**:
   Write a C++ program in `/home/user/local_process/matcher.cpp` (and compile it to `/home/user/local_process/matcher`) that takes three command-line arguments: `<input_csv>` `<master_list_txt>` `<output_csv>`.
   - The program should read the input CSV and the master list.
   - For each row in the input CSV (skipping the header if present, though assume no header for simplicity—just rows of `ID,Name`), it must normalize the `Name` by:
     a) Removing all leading and trailing whitespace.
     b) Converting all characters to lowercase.
   - It must compute the Levenshtein distance between the normalized name and every name in the master list.
   - It should find the single best match (the one with the lowest Levenshtein distance). If there is a tie, pick the one that appears first in `master_list.txt`.
   - It must write the results to `<output_csv>` in the format: `ID,NormalizedName,BestMatchName,Distance`.

2. **Pipeline Script**:
   Create a bash script at `/home/user/local_process/pipeline.sh` that performs the following steps when executed:
   - Copies `data.csv` from `/home/user/remote_in/` to `/home/user/local_process/`.
   - Executes the compiled `./matcher` program, using the copied local `data.csv` and the `/home/user/master_list.txt`, producing `/home/user/local_process/processed_data.csv`.
   - Copies the `processed_data.csv` to `/home/user/remote_out/processed_data.csv`.

3. **Cron Scheduling**:
   We want this pipeline to run automatically at the top of every hour (e.g., 01:00, 02:00, etc.). Since you cannot edit the live system crontab, write the exact cron expression line that would schedule `/home/user/local_process/pipeline.sh` into a file named `/home/user/crontab_entry.txt`.

Finally, run your `pipeline.sh` script once manually so that `/home/user/remote_out/processed_data.csv` is populated. Ensure the output CSV has exactly the formatting specified (no spaces after commas unless part of the name).