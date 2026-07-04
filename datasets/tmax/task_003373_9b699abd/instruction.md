You are tasked with helping a researcher organize and process experimental datasets using only Bash and standard command-line tools (like `awk`, `sed`, `grep`, `sort`, `bc`, etc.). Python, R, and other high-level scripting languages are strictly forbidden. 

The researcher has a set of raw data files in `/home/user/raw_data/`. These files are pipe-separated (`|`) and have the following intended schema:
`ExperimentID | Date | Category | Value`

However, the data is messy:
1. **Dates** are in mixed formats: some are `YYYY-MM-DD`, others are `MM/DD/YYYY`.
2. **Values** in some files use commas as decimal separators (e.g., `12,34`) instead of dots (`12.34`).
3. **Invalid rows**: Some rows have missing columns, empty fields, or `Value`s that are completely non-numeric (e.g., "N/A" or "error").

**Your objectives:**

1. **Dependency Setup**:
   The researcher wants to use `datamash` for aggregation, but it's not installed, and you do not have root access. 
   Download the statically linked GNU `datamash` binary (version 1.8) for x86_64 Linux from:
   `https://ftp.gnu.org/gnu/datamash/datamash-1.8.tar.gz`
   Extract it, and place the `datamash` executable (found inside the compiled/bin folders of the archive, or you may need to build it from source without root by using `./configure --prefix=/home/user/local && make && make install`) into `/home/user/local/bin/`. (Actually, the tar.gz is the source code. You must compile it from source and install it to `/home/user/local`).

2. **Data Schema Enforcement & Normalization**:
   Write a bash script at `/home/user/process_data.sh`. This script should read all `.txt` files in `/home/user/raw_data/`, and output a cleaned, tab-separated values (TSV) file at `/home/user/cleaned_data.tsv`.
   - Convert all pipe (`|`) delimiters to tabs (`\t`).
   - Standardize all dates to `YYYY-MM-DD`. (Assume any `MM/DD/YYYY` format has exactly a 4 digit year and 2 digit month/day, or single digit padded to 2. e.g. `12/31/2022` -> `2022-12-31`).
   - Replace commas with dots in the `Value` column.
   - Discard any row that does not have exactly 4 columns.
   - Discard any row where the `Value` column (after comma replacement) is not a valid positive or negative float/integer.
   - Discard any row where any field is empty.

3. **Aggregation**:
   Extend your script `/home/user/process_data.sh` to use the locally installed `datamash` (ensure `/home/user/local/bin` is in the PATH during script execution).
   - Group the cleaned data by `Category`.
   - Calculate the **sum** and the **mean** of the `Value` column for each category.
   - Sort the output alphabetically by `Category`.
   - Save the final aggregated output as a comma-separated values (CSV) file at `/home/user/results/summary.csv` with the header: `Category,Total,Average`. Round the numbers to 2 decimal places if necessary (datamash default for rounding or format using awk).

Run your script to produce the final `summary.csv`.