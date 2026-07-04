You are an AI assistant helping a data researcher clean their datasets and investigate a potential data leak. 

The researcher has two datasets located at:
- `/home/user/train.csv`
- `/home/user/test.csv`

Both files have a header `ID,X,Y`. 
The researcher suspects that due to a faulty data splitting pipeline, some records (identified by the `ID` column) have leaked from the test set into the training set.

Using ONLY standard Bash shell utilities (e.g., `awk`, `join`, `sort`, `comm`, `grep`), perform the following tasks:

1. **Find the Data Leak**: Determine exactly how many unique `ID`s appear in *both* `train.csv` and `test.csv` (ignore the header row).
2. **Clean the Data**: Create a new file `/home/user/train_clean.csv` that contains only the rows from `train.csv` whose `ID`s DO NOT appear in `test.csv`. The output file MUST preserve the original header `ID,X,Y`.
3. **Compute a Mathematical Metric**: To help compute the covariance later, calculate the sum of the product of columns X and Y (i.e., $\sum (X \times Y)$) for all data rows in your new `train_clean.csv`. 

Finally, write your findings to `/home/user/report.txt` in the exact following format:
```
Leaked IDs: <integer_count>
Clean Sum of Products: <float_value_rounded_to_2_decimal_places>
```

Example of `report.txt`:
```
Leaked IDs: 5
Clean Sum of Products: 1245.67
```

Ensure your solution strictly relies on Bash and standard Linux tools (no Python, R, or Perl).