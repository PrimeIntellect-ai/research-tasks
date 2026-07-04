You are a log analyst investigating regional error patterns. Our server logs from different regions have been aggregated into a poorly formatted wide CSV file, and you need to process it to extract a representative sample of normalized access records.

The raw data is located at `/home/user/raw_logs.csv`. 
This file has the following columns: `region`, `ip_address`, `2023-10-01`, `2023-10-02`, `2023-10-03`.
The date columns contain pipe-separated (`|`) raw HTTP request strings. 

Write a Python script at `/home/user/process_logs.py` that does the following:

1. **Wide-to-Long Reshaping:** Read the CSV. Reshape it so that the date columns become a single column named `date`, and the values become a column named `raw_requests`. Filter out any rows where `raw_requests` is empty or NaN.
2. **Explode:** Since `raw_requests` can contain multiple pipe-separated requests, split these strings by the pipe `|` character and explode them so each individual request has its own row. Name this column `raw_request`.
3. **Character Decoding & Normalization:** Some of the request strings contain URL-encoded characters (e.g., `%20` for space, `%C3%A9` for é). URL-decode the `raw_request` strings.
4. **Tokenization:** Parse the decoded `raw_request` string (format: `"<METHOD> <ENDPOINT> <PROTOCOL>" <STATUS_CODE>`). Extract three new columns: `method` (e.g., GET), `endpoint`, and `status_code` (as an integer). 
5. **Endpoint Normalization:** Lowercase the extracted `endpoint` and remove any query parameters (everything including and after the `?` character). For example, `/Api/Users?id=123` becomes `/api/users`.
6. **Data Cleaning:** Drop the `raw_requests` and `raw_request` columns. You should be left with: `region`, `ip_address`, `date`, `method`, `endpoint`, and `status_code`.
7. **Stratified Sampling:** We need a representative sample. Sort the entire DataFrame by `date`, `ip_address`, `method`, and `endpoint` (all in ascending order) to ensure deterministic ordering. Then, group the data by `region` and `status_code`. Using pandas, take a random sample of exactly 2 rows per group. Use `random_state=42` in your sampling function. If a group has fewer than 2 rows, include all rows for that group.
8. **Output:** Save the final sampled DataFrame to `/home/user/sampled_logs.json` in JSON `records` orientation (a list of dictionaries).

Run your script to produce the output file.