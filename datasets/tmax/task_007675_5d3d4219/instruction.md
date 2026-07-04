You are a data scientist tasked with cleaning a large dataset using only standard Linux command-line tools. An automated pipeline has been downloading sensor data, but there is a known issue where data-type coercion silently corrupts high-precision identifiers when processed incorrectly.

Your objective is to write a Bash script at `/home/user/clean.sh` that processes a dataset (`/home/user/raw_data.csv`). You must strictly use Bash and standard CLI tools (like `awk`, `sed`, `grep`, `bc`, `zstd`, `tar`, etc.). Do NOT use Python, R, Perl, or Ruby.

The script must perform the following operations:

1. **Storage Management:** Before processing, compress `/home/user/raw_data.csv` into a Zstandard-compressed tarball located at `/home/user/archive/backup.tar.zst`. You will need to create the `archive` directory.
2. **Dimensionality Reduction (Feature Selection):** Read the CSV and dynamically identify and drop any column where *every* data row (excluding the header) contains the value `NaN`. 
3. **Imputation:** For the remaining columns, replace any instance of `NaN` with `0.0`.
4. **Numerical Accuracy Verification:** The first column is `ID`, which contains 19-digit integers. Standard processing tools often silently coerce these into double-precision floats, losing precision. Calculate the exact, precision-lossless sum of all the `ID` values (excluding the header). Write this exact sum to `/home/user/id_sum.txt`.
5. **Output:** Save the final cleaned, dimension-reduced CSV (with `NaN`s imputed) to `/home/user/cleaned_data.csv`. Keep the header intact.

Make sure your script is executable (`chmod +x /home/user/clean.sh`) and run it so the expected output files are generated.

**Constraints:**
- The input CSV is comma-separated.
- The `id_sum.txt` must contain only the exact integer sum and a newline.
- Do not hardcode the column indices to drop; your script must deduce which columns are entirely `NaN` by inspecting the data.