You are a data scientist cleaning a legacy IoT temperature dataset. 

You have been given a raw, messy dataset at `/home/user/raw_sensor.txt`. 
The file has the following issues:
1. **Character Encoding:** The file is encoded in UTF-16LE.
2. **Duplicates:** There are exact duplicate lines caused by a faulty logging system.
3. **Missing Days:** The data spans from `2023-10-01` to `2023-10-07`, but some days have no readings.
4. **Multiple Readings:** Some days have multiple readings that need to be aggregated.

Your task is to process this file entirely using standard Linux command-line tools (Bash, awk, iconv, sort, etc.) and generate a cleaned, gap-filled time series dataset at `/home/user/cleaned_timeseries.csv`.

Here are the exact requirements for the pipeline:
1. Decode the file to standard UTF-8.
2. Remove exact duplicate lines (lines where both date and temperature are identical).
3. Compute the **daily average temperature**. If a day has multiple unique readings, average them.
4. **Gap-fill** missing days between `2023-10-01` and `2023-10-07` inclusive. Use **forward-filling**: if a day is missing, it should take the average temperature of the most recent available previous day.
5. Format the output as a CSV file with the exact header `Date,Avg_Temp`.
6. Format the `Avg_Temp` column to exactly one decimal place (e.g., `21.0`, `23.5`).

The input format of the text file (once decoded) is pipe-separated: `YYYY-MM-DD|temperature` (e.g., `2023-10-01|22.5`).

Create the final cleaned CSV at `/home/user/cleaned_timeseries.csv`.