You are a Data Scientist cleaning a dataset entirely within the command line.

You have two CSV files:
1. `/home/user/data_x.csv` - Contains user IDs and Feature X. Format: `user_id,x_val`
2. `/home/user/data_y.csv` - Contains user IDs and Feature Y. Format: `user_id,y_val`

Your task:
1. Join these two datasets on `user_id`. Note that the datasets are not sorted, and some users only exist in one of the files.
2. Filter the joined dataset to remove any rows where either `x_val` or `y_val` is missing (empty).
3. Compute the Pearson correlation coefficient between Feature X and Feature Y for the remaining joined records.
4. Save the final Pearson correlation coefficient, rounded to 4 decimal places, to `/home/user/correlation.txt`.

Constraints & Guidelines:
- You must accomplish this using Bash shell commands, coreutils, and standard CLI tools. 
- You are allowed to install additional command-line utilities via `sudo apt-get` (e.g., `datamash` is highly recommended for easy statistical operations).
- Do not use Python, R, or Perl to solve this.

Expected Output:
A single file at `/home/user/correlation.txt` containing only the rounded correlation coefficient (e.g., `0.8421`).