You are tasked with analyzing the evolution of server security configurations over time. 

You have been provided a directory of configuration backups located at `/home/user/configs`. These files are backups of `.ini` configuration files collected over several months. The filenames follow the pattern `backup_YYYY-MM-DD.ini`.

Due to a misconfiguration in the backup system, some files were saved in `UTF-8` encoding, while others were saved in `UTF-16` encoding. 

Your objective is to write a Python script to calculate the "configuration drift" between consecutive months based on the keys present in the `[Security]` section of these files.

Perform the following steps:
1. Parse all `.ini` files in `/home/user/configs`, automatically handling the mixed encodings (UTF-8 and UTF-16).
2. Extract the configuration **keys** (ignoring their values) located exclusively under the `[Security]` section of each file. The section ends when a new section starts (e.g., `[AnotherSection]`) or at the end of the file.
3. Group the files into time buckets by month (e.g., `2023-01`, `2023-02`). 
4. For each month, compute the **union** of all `[Security]` keys found across all backups in that specific month.
5. Compute the Jaccard Distance between the set of keys of each month and the set of keys of the **chronologically previous** month. 
   * *Formula*: `Jaccard_Distance = 1.0 - (Size_of_Intersection / Size_of_Union)`
6. Write the results to a CSV file at `/home/user/drift_report.csv` with the exact header `Month,Previous_Month,Distance`.
   * Order the rows chronologically by `Month` (starting from the second month in the dataset, since the first month has no previous month).
   * Format the `Distance` to exactly 3 decimal places (e.g., `0.600`).

Ensure your script runs successfully and creates the final CSV file.