You are a Data Scientist tasked with building a reproducible bash-based data cleaning pipeline. You need to process a dataset while ensuring strict environment configuration, output validation, and experiment tracking.

Your objective is to create and run a Bash script at `/home/user/clean_pipeline.sh` that processes `/home/user/raw_data.csv` and outputs to `/home/user/clean_data.csv`.

Here are the requirements for your script:
1. **Numerical Configuration:** To ensure numeric parsing reproducibility across different environments, your script must explicitly set `LC_ALL=C` before processing the data.
2. **Data Cleaning & Validation (Bash/awk/etc.):**
   - The input is a comma-separated values (CSV) file with a header: `id,value,score`.
   - Keep the header in the output.
   - Drop any row where `value` (the 2nd column) is less than 0.
   - Drop any row where `score` (the 3rd column) is exactly `NaN`, `NA`, or empty.
   - Write the cleaned dataset to the output file path provided as an argument.
3. **Experiment Tracking:**
   - After creating the output file, your script must compute the MD5 checksums of the input file and the output file.
   - It must append exactly one line to `/home/user/experiments.log` with the following format:
     `IN:<input_md5> OUT:<output_md5> LINES:<output_line_count>`
     (Note: `<output_line_count>` should be the number of lines in the output file, including the header).
4. **Usage:**
   - Your script must accept exactly two arguments: the input file path and the output file path.
   - Run your script once against the data to generate the final output:
     `bash /home/user/clean_pipeline.sh /home/user/raw_data.csv /home/user/clean_data.csv`

Ensure your script is robust and correctly handles the filtering logic.