You are a data scientist building a lightweight, Bash-based data cleaning pipeline. Sometimes Python is overkill, and you need a fast shell script to sanitize incoming data, validate it, and track the process.

I have a raw dataset located at `/home/user/raw_data.csv`. The file has the following header: `id,age,income,score`.

Write a Bash script at `/home/user/clean_data.sh` that performs the following tasks:
1. **Missing Value Handling**: Remove any rows where the `age` column is completely empty.
2. **Outlier Handling**: Remove any rows where the `income` column is less than 0 or greater than 1,000,000.
3. **Output**: Save the cleaned dataset (including the original header) to `/home/user/cleaned_data.csv`.
4. **Experiment Tracking**: Calculate the number of data rows (excluding the header) in the initial dataset, and the number of data rows in the cleaned dataset. Append a log entry to `/home/user/experiment_log.txt` exactly in this format:
   `[<YYYY-MM-DD HH:MM:SS>] Initial: <N> rows, Cleaned: <M> rows`
   *(where `<N>` is the initial data row count and `<M>` is the cleaned data row count. Ensure the date/time is dynamically generated).*

Your script should be executable and process the file efficiently using standard Unix utilities (like `awk`, `sed`, `grep`, etc.). Run your script once to generate the outputs.