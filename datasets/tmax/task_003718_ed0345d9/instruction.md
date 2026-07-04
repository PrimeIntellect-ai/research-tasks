You are a data scientist tasked with cleaning a dataset and computing some basic statistical metrics using standard Unix shell tools.

You have a dataset located at `/home/user/dataset.csv` with the following columns: `transaction_id,cohort,amount`.
Some of the data is dirty: `amount` might be empty, contain non-numeric characters, or be negative.

Your objective is to write a Bash script at `/home/user/analyze.sh` that does the following:
1. Cleans the data by keeping only the rows where `amount` is a valid positive number (greater than 0, can have decimal places) and `cohort` is either `Control` or `Treatment`. (Assume a header row is present and should be ignored or skipped in calculations).
2. Computes the mean `amount` for the `Control` cohort.
3. Computes the mean `amount` for the `Treatment` cohort.
4. Computes the absolute difference between the two means.
5. Prints the results exactly in the following format (rounded to exactly 2 decimal places):

```
Control Mean: <value>
Treatment Mean: <value>
Absolute Difference: <value>
```

Requirements:
- The script must be written in Bash and use standard command-line tools (e.g., `awk`, `sed`, `grep`, `bc`). You cannot use Python, R, or Perl.
- The script must take the input CSV file path as its first argument (e.g., `./analyze.sh /home/user/dataset.csv`).
- Make sure the script is executable.
- Output the result to standard output when run.

Save the output of your script run on `/home/user/dataset.csv` to `/home/user/results.txt`.