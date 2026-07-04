You are an AI assistant helping a climate researcher organize and extract anomalous readings from a messy, nested dataset archive. 

The researcher has uploaded a raw archive located at `/home/user/data_dump.tar.gz`. Due to how different field teams submit their data, this archive contains other compressed archives (zips, tarballs) nested inside it, which in turn contain sensor data in various formats: CSV, JSON, and XML.

Your task is to:
1. Extract `/home/user/data_dump.tar.gz` and all of its nested archives (which may include `.zip` and `.tar.bz2` files) into a working directory.
2. Find all data files within the extracted contents. 
3. Write a Python script (e.g., `process_anomalies.py`) that parses these structured formats to identify "anomalous" sensor readings where the `value` is strictly greater than `85.0`.
4. The data formats you will encounter are:
   - **CSV**: Contains columns `id`, `timestamp`, `value`.
   - **JSON**: An array of objects, e.g., `[{"id": "S3", "value": 91.2}, ...]`.
   - **XML**: A root `<readings>` element containing multiple `<reading>` elements. Each `<reading>` has an `<id>` and a `<value>` child element.
5. Aggregate all the anomalous readings (id and value) and write them to a new CSV file at `/home/user/anomalies_summary.csv`. The output CSV must have a header `id,value` and the rows must be sorted alphabetically by the `id` column.
6. Finally, compress `/home/user/anomalies_summary.csv` using gzip to create `/home/user/anomalies_archive.csv.gz`.

Requirements:
- Only include readings where `value > 85.0`.
- The final gzip archive must be strictly named `/home/user/anomalies_archive.csv.gz`.
- Use Python for the parsing logic, but you may use Bash tools (`find`, `xargs`, standard stream redirection) to pass the files to your script or orchestrate the process.