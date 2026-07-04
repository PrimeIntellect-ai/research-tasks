You are an assistant helping a researcher organize and process vector datasets using Bash. The researcher has a collection of CSV files containing numerical vectors, but some files have schema inconsistencies (e.g., missing values represented as "NA", or incorrect number of columns). 

Your task is to write a Bash script `/home/user/run_experiment.sh` that processes all `.csv` files in the directory `/home/user/datasets/`, enforces a strict data schema, computes a linear algebra metric (dot product), and tracks the results in an experiment log.

Here are the specific requirements for your script:

1. **Schema Enforcement:** 
   For each CSV file, check if it adheres to the following strict schema:
   - Every row must have exactly 2 columns separated by a comma (representing Vector A and Vector B).
   - The values in the columns must either be valid integers (positive or negative) OR exactly the string "NA".
   - If a file violates ANY of these rules (e.g., has 3 columns, contains alphabetic characters other than "NA", contains floats), the file is considered invalid.

2. **Data Imputation & Linear Algebra (Dot Product):**
   - For valid files, you must calculate the dot product of the two columns (i.e., the sum of Column1 * Column2 across all rows).
   - Before calculation, any "NA" values must be imputed as `0`. 
   - Note: The files do not have header rows.

3. **Experiment Tracking:**
   - Your script must evaluate the files and write the results to `/home/user/experiment_log.txt`.
   - Each line in the log must be formatted exactly as: `<filename>:<result>`
   - `<filename>` should be the base name of the file (e.g., `data1.csv`).
   - `<result>` should be the computed dot product integer for valid files, or the string `INVALID_SCHEMA` for invalid files.
   - The final output in `/home/user/experiment_log.txt` must be sorted alphabetically by the filename.

Ensure your script is executable and actually run it to generate `/home/user/experiment_log.txt`. You should exclusively use Bash and standard command-line utilities (like `awk`, `grep`, `sed`, etc.) to accomplish this task.