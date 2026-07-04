You are an automation specialist tasked with fixing a fragile ETL workflow. The existing pipeline occasionally retries failed batches, causing duplicate records to be ingested. Additionally, the downstream systems are failing due to sudden data spikes (changepoints/anomalies) that are not being filtered out.

You need to write a standalone Python script, `/home/user/etl_cleaner.py`, that processes raw data dumps and cleans them before loading. 

We have provided a screenshot of the legacy system's configuration diagram at `/app/pipeline_specs.png`. You must extract the operational parameters from this image (using OCR tools like `tesseract` which is preinstalled). The image contains three critical pieces of information:
1. The unique key used for deduplicating records.
2. The sort field used to order records before anomaly detection.
3. The `MAX_STEP_DELTA` value used to detect anomalous changepoints.

Your script must adhere to the following strict specifications:
1. **Invocation**: The script must be executable and accept a single positional argument: the path to an input JSONL (JSON Lines) file. Example: `python3 /home/user/etl_cleaner.py input.jsonl`.
2. **Input Format**: Each line is a JSON object. You may assume they contain at least the deduplication key, the sort field (an integer), and a `value` field (a float).
3. **Deduplication**: Read all records. If multiple records share the same deduplication key, keep ONLY the record that appears *last* in the input file (simulating the latest retry payload overriding previous ones). 
4. **Sorting**: After deduplication, sort the remaining records in ascending order based on the sort field specified in the image.
5. **Changepoint/Anomaly Filtering**: Iterate through the sorted records. Keep the first record unconditionally. For every subsequent record, calculate the absolute difference in `value` between the *current* record and the *last accepted* record. If this difference is strictly greater than the `MAX_STEP_DELTA` extracted from the image, it is considered an anomaly and must be discarded. (Note: compare against the *last accepted* record, not the previous unaccepted record).
6. **Output**: Print the final cleaned list of JSON objects to standard output (stdout), one valid JSON object per line. Do not print any other debugging information or logs to stdout.

You must handle parallel processing efficiently if the files get large, but the final output order must strictly match the sorting criteria. Ensure your Python script is robust. An automated testing suite will fuzz your script with thousands of random JSONL files to ensure it produces bit-exact equivalent output to our reference implementation.