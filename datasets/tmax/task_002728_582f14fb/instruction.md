You are a Machine Learning Engineer preparing tabular data for a training pipeline. You need to build a reproducible data processing script in pure Bash (using standard UNIX utilities like `awk`, `sed`, `bc`). Do not use Python, R, or any other high-level scripting languages.

You are provided with a dataset at `/home/user/raw_data.csv` containing the following columns:
`id,f1,f2,f3,label`

Your task is to create an executable bash script at `/home/user/pipeline.sh` that performs the following steps when run:
1. Calculates the Pearson correlation coefficient ($r$) between the features `f1` and `f2`.
2. Saves this correlation coefficient, rounded to exactly 3 decimal places, to `/home/user/correlation.txt`.
3. Checks if the correlation $r$ is greater than or equal to $0.85$.
4. Generates a new dataset at `/home/user/clean_data.csv` with the following transformations:
   - If $r \ge 0.85$, drop the `f2` column entirely (it is redundant). The header should become `id,f1,f3,label`. If $r < 0.85$, keep all columns.
   - Mean-center the `f1` and `f3` columns (i.e., subtract the mean of the respective column from each value).
   - Format all floating-point values in the output CSV to exactly 3 decimal places (e.g., `0.000`, `-1.500`).
   - The `id` and `label` columns must remain integers and unmodified.

Constraints:
- The script `/home/user/pipeline.sh` must be self-contained and run without arguments.
- Use only Bash and standard POSIX utilities (`awk`, `bc`, `coreutils`, etc.). Do not use `python`, `perl`, `ruby`, etc.
- Make sure to ignore the header row when calculating means and correlations.

Once you have created the script, run it so that `/home/user/correlation.txt` and `/home/user/clean_data.csv` are generated.