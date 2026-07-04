As an automation specialist, you are building a text-processing workflow to analyze historical weather logs digitized via OCR. The OCR system sometimes misses hours entirely and often leaves messy punctuation. You need to write a C program that normalizes the text, fills in missing temporal gaps, computes the string distances between consecutive hours, and aggregates the results.

Your task is to write and execute a C program (save your code anywhere, e.g., `/home/user/process_logs.c`, and compile it) that reads a CSV file located at `/home/user/weather_logs.csv`. 

The input CSV has the header `hour,text`. The `hour` column contains integers from `0` to `23` representing the hour of the day. Some hours between 0 and 23 will be missing. 

Your C program must perform the following pipeline:
1. **Resampling and Gap-filling:** Generate a complete sequence of 24 hours (0 through 23). If an hour is missing from the CSV, fill its text by carrying forward the *normalized* text of the most recent available previous hour. (If hour `0` is missing, assume its initial text is an empty string `""`).
2. **Tokenization and Normalization:** For the provided text, normalize it by:
   - Converting all characters to lowercase.
   - Replacing any non-alphanumeric character (anything not `a-z` or `0-9`) with a single space.
   - Collapsing multiple consecutive spaces into a single space.
   - Stripping any leading or trailing spaces.
   *(Note: perform normalization on available logs before carrying them forward to fill gaps).*
3. **Distance Computation:** Compute the standard Levenshtein distance (cost of 1 for insertions, deletions, and substitutions) between the normalized text of hour $H$ and hour $H-1$, for every hour $H$ from 1 to 23.
4. **Aggregation:** Calculate the total number of missing hours filled, the maximum Levenshtein distance between any two consecutive hours (and the hours it occurred between), and the average Levenshtein distance across all 23 consecutive pairs.

The program must output a summary to `/home/user/weather_summary.txt` in exactly the following format:
```
Total Missing Hours Filled: <count>
Max Levenshtein Distance: <max_dist> (between hour <H-1> and hour <H>)
Average Levenshtein Distance: <average_dist>
```
*Notes:*
- `<average_dist>` should be rounded to 2 decimal places (e.g., `3.17`).
- If there is a tie for the maximum distance, use the earliest pair (lowest `<H>`).

Write the C code, compile it, run it against `/home/user/weather_logs.csv`, and generate the `weather_summary.txt` file.