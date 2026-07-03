You are tasked with building a reproducible ETL (Extract, Transform, Load) and numerical validation pipeline for a messy dataset of scientific measurements. 

A raw dataset is located at `/home/user/raw_measurements.csv` with the following columns: `id,value,category`.
The `value` column contains extremely messy data, including unparsable text, NaNs, infinities, and extreme outliers, mixed with high-precision floating-point numbers.

Your goal is to write a reproducible pipeline script at `/home/user/pipeline.sh` that cleans the data, enforces numerical accuracy, and calculates baseline statistics.

The pipeline script must perform the following when executed:
1. Accept two arguments: the input file path, and the output directory path. (e.g., `./pipeline.sh /home/user/raw_measurements.csv /home/user/output/`)
2. Read the input file and filter the rows according to these strict rules:
   - The `value` must be successfully parsed as a standard 64-bit float.
   - Drop any rows where `value` is NaN (Not a Number) or Infinity (positive or negative).
   - Drop any rows where `value` is strictly less than `-100.0` or strictly greater than `100.0`.
3. Save the cleaned dataset to `cleaned_measurements.csv` inside the output directory. It must maintain the `id,value,category` header and original ordering for valid rows.
4. Calculate the statistical **mean** and **population variance** (using N, not N-1) for the `value` column, grouped by `category`.
5. Save these statistics to `stats.json` inside the output directory. The JSON format must be strictly as follows (keys ordered alphabetically by category):
```json
{
  "A": {
    "mean": 1.2345,
    "variance": 0.1234
  },
  "B": {
    "mean": -4.5678,
    "variance": 9.8765
  }
}
```
*Note: Round the mean and variance to exactly 4 decimal places in the JSON output.*

Requirements:
- You may use Python, R, or Bash for the core logic, but the entry point must be an executable bash script at `/home/user/pipeline.sh`.
- You must install any necessary dependencies within your process or script.
- Ensure the output directory is created if it does not exist.
- Run your pipeline once to generate `/home/user/output/cleaned_measurements.csv` and `/home/user/output/stats.json`.