You are a localization engineer tasked with cleaning up a messy, newly ingested translation file from an external vendor. The file is located at `/home/user/raw_locales.txt`.

The raw file contains key-value pairs separated by a colon (`:`). However, the formatting is inconsistent, contains invalid keys, and has duplicate entries. 

You need to write a C program to perform data validation and normalization, and then use it within a shell pipeline to deduplicate and sort the final output.

Step 1: Write a C program at `/home/user/loc_cleaner.c` that does the following:
- Reads text from standard input (stdin) line by line.
- Splits each line into a key and a value using the *first* colon (`:`) as the delimiter. (Note: The value itself may contain colons).
- Trims all leading and trailing spaces and tabs (` ` and `\t`) from both the key and the value. Newline characters should also be stripped.
- Validates the trimmed key. A valid key must contain **only** uppercase letters (`A-Z`) and underscores (`_`), and must be at least 1 character long.
- If a line does not contain a colon, or if the key is invalid, discard the line silently.
- For valid lines, print to standard output (stdout) in the exact format: `KEY=VALUE`.

Step 2: Compile your program to `/home/user/loc_cleaner`.

Step 3: Construct and execute a shell pipeline that:
- Feeds `/home/user/raw_locales.txt` into your `/home/user/loc_cleaner` program.
- Deduplicates the keys. If a key appears multiple times in the valid output, you must retain **only the last** occurrence from the original file sequence.
- Sorts the final deduplicated entries alphabetically by key.
- Writes the final output to `/home/user/clean_locales.ini`.

Constraints:
- Do not use temporary files for the intermediate steps of the pipeline (between the C program and the final output).
- The value might be empty after trimming, which is valid and should be output as `KEY=`.