You are a data scientist cleaning up server metrics. You have been given a dataset in `/app/data/metrics.csv` that contains daily metric readings for three servers (ServerA, ServerB, ServerC) in a wide format (columns: `date, ServerA, ServerB, ServerC`). 

Unfortunately, the data export pipeline had a bug, and some values are wrapped in quotes and contain embedded newlines, which breaks standard line-by-line processing. 

Additionally, your team lead gave you a screenshot `/app/rules.png` containing the anomaly detection threshold rule that must be applied to the cleaned data.

Your task is to write a data processing pipeline (primarily using Bash and standard UNIX utilities, though Python is allowed if necessary) that does the following:
1. Extracts the anomaly threshold rule from the image `/app/rules.png` (Tesseract OCR is available).
2. Cleans the `metrics.csv` file, properly handling or removing the embedded newlines so that each date corresponds to exactly one row.
3. Reshapes the cleaned data from wide format to long format with columns `date, server_name, value`.
4. Detects anomalies where the `value` exceeds the threshold extracted from the image.
5. Saves the final detected anomalies in a CSV file at `/home/user/anomalies.csv` with the exact header `date,server_name,value`.

Ensure your output is complete and perfectly formatted. Your result will be evaluated based on the F1 score of the detected anomalies compared to a hidden ground truth. You need an F1 score of at least 0.95 to pass.