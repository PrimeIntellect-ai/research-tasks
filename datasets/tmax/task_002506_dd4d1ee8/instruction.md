You are an automation specialist managing a legacy data pipeline. The upstream ETL process frequently fails and retries, dumping raw, duplicated binary records into the stream. Additionally, the sensors generating this data sometimes experience extreme drift (anomalies), which needs to be caught.

Your task is to write a Go program that reads a binary data stream from standard input (`STDIN`), processes the records to filter out duplicates, decodes the text properly, checks for changepoint anomalies, and prints the cleaned stream to standard output (`STDOUT`). 

However, the specific configuration parameters for this legacy pipeline (the character encoding, the fixed record size, and the anomaly threshold) have been lost from the source code and are only available in a scanned printout located at `/app/data_spec.png`. 

**Step 1: Extract Configuration**
Use OCR (e.g., `tesseract`, which is pre-installed) to read the text inside `/app/data_spec.png`. It will contain three key-value pairs defining:
1. `CHARSET`: The character encoding of the input stream.
2. `RECORD_SIZE`: The exact size of each record in bytes.
3. `THRESHOLD`: The maximum allowed absolute difference between consecutive valid values.

**Step 2: Implement the Processor in Go**
Create a Go program at `/home/user/processor.go` and compile it to `/home/user/processor`. The program must do the following:
1. Read the binary stream from `STDIN`.
2. Chunk the stream into records of exactly `RECORD_SIZE` bytes. If the stream ends with an incomplete record, ignore the incomplete trailing bytes.
3. For each record:
   a. Decode the entire record from the specified `CHARSET` to UTF-8.
   b. Extract the `ID`: The first 8 characters of the decoded string.
   c. Extract the `Value`: Characters at index 8 through 15 (inclusive) of the decoded string. Parse this as a base-10 integer (ignore leading/trailing spaces).
   d. **Deduplication:** If the `ID` has already been successfully processed (seen before in the stream), drop this record completely (it's an ETL retry).
   e. **Anomaly Detection:** Compare the current `Value` with the *previously processed valid* `Value`. If the absolute difference is strictly greater than `THRESHOLD`, print `ANOMALY DETECTED AT ID:<ID>` to `STDOUT` and immediately exit the program with status code 0. (The first valid record never triggers an anomaly).
4. For every valid, non-duplicate record that does *not* trigger an anomaly, print it to `STDOUT` in the following exact format: `[<ID>] -> <Value>` followed by a newline.

Your compiled binary must be executable at `/home/user/processor`. The automated verifier will pipe thousands of fuzzed byte streams into your binary and compare its standard output bit-for-bit against a reference oracle.