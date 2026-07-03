I'm building a data processing pipeline for audio features, but I'm worried about data leakage between my train and test sets during feature scaling.

First, I have an audio recording at `/app/recording.wav`. It contains a short sequence of spoken numbers. Please transcribe the numbers as digits separated by spaces (e.g., "4 8 15") and save this exactly to `/home/user/transcription.txt`. You can use `whisper` or any other tool you install locally.

Second, I need you to write a Bash script `/home/user/normalize.sh` that performs min-max scaling on tabular data, strictly avoiding train-test leakage. 

The script must:
1. Accept an integer `N` as its first argument (the number of training rows).
2. Read a CSV from standard input. The CSV will always have a header row, followed by an arbitrary number of data rows containing numerical values (integers or floats).
3. Compute the `min` and `max` for *each column* using **only** the first `N` data rows (the training set). 
4. Apply min-max scaling to **all** data rows (both train and test) using the training set's `min` and `max`. The formula is `(value - min) / (max - min)`. If a column's `max` equals its `min` in the training set, the scaled value for that column should be `0.00` for all rows.
5. Print the header row, followed by the scaled data rows. All scaled values must be formatted to exactly two decimal places (e.g., `0.50`). The output must be valid CSV.

Example of expected behavior:
```bash
cat data.csv
a,b
1,10
3,20
5,30
2,40

# N=2 means training set is the first 2 rows:
# Col a: min=1, max=3
# Col b: min=10, max=20
$ ./normalize.sh 2 < data.csv
a,b
0.00,0.00
1.00,1.00
2.00,2.00
0.50,3.00
```

Make sure your script correctly handles edge cases, negative numbers, and is efficient.