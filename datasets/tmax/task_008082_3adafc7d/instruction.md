You are acting as a data scientist cleaning up a dataset from an unreliable ETL pipeline. The pipeline retried a few times, resulting in duplicate records, and occasionally failed to run for several hours, resulting in missing data.

You have been provided with:
1. `/home/user/data/raw_measurements.csv` - The raw data file containing `timestamp` and `value` columns.
2. `/home/user/template.md` - A Markdown template for your final report.

Your tasks are to write and execute a Python script that does the following:
1. **Deduplicate**: The raw data contains multiple entries for the same timestamp due to ETL retries. For any duplicate `timestamp`, keep only the row with the maximum `value`.
2. **Bucket and Aggregate**: Resample the deduplicated data into 1-hour intervals (e.g., `2023-10-01T00:00:00Z` to `2023-10-01T00:59:59Z` is bucketed to `2023-10-01T00:00:00Z`). The value for the hour bucket should be the arithmetic mean of all deduplicated values falling within that hour.
3. **Impute**: The ETL pipeline occasionally missed hours entirely. Impute these missing 1-hour buckets using linear interpolation.
4. **Export Cleaned Data**: Save the resulting cleaned and interpolated time series to `/home/user/data/cleaned_measurements.csv`. The output must have the columns `timestamp` (in ISO8601 format with 'Z' timezone, e.g., `2023-10-01T00:00:00Z`) and `value` (rounded to 1 decimal place).
5. **Generate Report**: Read `/home/user/template.md` and replace the placeholders `{orig_rows}`, `{clean_rows}`, `{max_val}`, and `{min_val}` with the actual statistics from your processing. Save the generated report to `/home/user/report.md`. Note: `{max_val}` and `{min_val}` should be based on the final `value`s in the cleaned dataset, rounded to 1 decimal place.

The format of the cleaned CSV should be strictly:
```csv
timestamp,value
2023-10-01T00:00:00Z,11.0
...
```

The template file `/home/user/template.md` contains:
```markdown
# ETL Pipeline Cleanup Report

- Original Rows Processed: {orig_rows}
- Cleaned Hourly Buckets: {clean_rows}
- Peak Average Value: {max_val}
- Lowest Average Value: {min_val}
```