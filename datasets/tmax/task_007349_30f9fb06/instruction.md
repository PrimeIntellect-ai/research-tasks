You are helping a researcher organize and analyze a large tabular dataset. 

The researcher has written a Bash script that uses `awk` to compute the Pearson correlation coefficient between two numeric feature columns in a CSV file. However, the script is currently producing incorrect results because the dataset contains missing values (represented as `NA` or empty strings). The current `awk` script silently coerces these non-numeric/missing values into `0` during aggregation, skewing the mathematical sums and the final correlation result.

Your task:
1. Fix the script located at `/home/user/calc_corr.sh`. 
2. Modify it so that it strictly ignores any row where *either* the second or third column contains missing, empty, or non-numeric values (like `NA`). Only rows with valid numbers in both columns should be included in the sums and the sample size `N`.
3. Run your fixed script on `/home/user/dataset.csv` using the command `./calc_corr.sh /home/user/dataset.csv`.
4. Save the exact numerical output of the script to `/home/user/correlation_result.txt`.

Ensure your updated `calc_corr.sh` calculates the standard Pearson correlation coefficient correctly based strictly on the valid pairwise data. Note that the first row is a header and should be ignored.