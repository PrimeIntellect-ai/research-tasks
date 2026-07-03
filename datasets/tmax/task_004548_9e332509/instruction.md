You are a machine learning engineer preparing a tabular dataset for a classification model. Your goal is to write a Bash data processing pipeline that performs feature selection (a simple form of dimensionality reduction) by keeping only the features with the highest variance.

You have been provided with a vendored third-party tool called `awk-stat-1.1`, located at `/app/awk-stat-1.1`. This tool calculates the statistical variance of numeric columns in a CSV. 
However, the package is currently broken. Its `Makefile` has a typo and references a missing source file instead of the correct `core.awk` file present in the `src/` directory. 

Your tasks are:
1. **Fix and Build the Package**: Fix the `Makefile` in `/app/awk-stat-1.1` so that it correctly concatenates `src/header.awk` and `src/core.awk` to build `bin/awk-stat`. Run `make` to build it. The resulting executable will take a CSV and output the variance of each numeric column in the format: `ColumnName Variance`.

2. **Write the Pipeline Script**: Create a Bash script at `/home/user/feature_pipeline.sh`. 
   - It must accept exactly one argument: the path to an input CSV file.
   - The input CSV will always have the following columns in order: `ID,Label,F1,F2,F3,F4,F5`. 
   - Your script must use the repaired `/app/awk-stat-1.1/bin/awk-stat` to compute the variance of the feature columns (`F1` to `F5`).
   - Identify the **top 2** features with the highest variance. If there's a tie, fall back to alphabetical order of the feature names (e.g., F2 before F3).
   - Your script should output a transformed CSV to standard output (`stdout`) containing exactly 4 columns: `ID`, `Label`, and the 2 selected feature columns (in their original relative order from the input).
   - The output CSV must include the header row.
   - The output data rows must be sorted numerically by the `ID` column.

Constraints:
- Use only Bash, `awk`, `sort`, `cut`, and standard GNU Coreutils.
- Make sure `/home/user/feature_pipeline.sh` is executable.
- Do not hardcode the column variances; they must be computed dynamically for any provided input CSV.

Ensure your pipeline is robust. An automated tester will fuzz your script with multiple random CSV inputs to verify bit-exact equivalence with a reference implementation.