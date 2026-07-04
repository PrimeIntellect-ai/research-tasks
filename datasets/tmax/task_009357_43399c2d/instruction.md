You are a data engineer building an ETL pipeline to unify and analyze alert streams from two legacy monitoring systems. One system exports data as JSON, and the other as CSV. 

Your task is to write and execute a Go program that processes these files, cleans the text data, imputes missing values using string similarity, detects anomalous alert surges, and outputs the results.

Here are the requirements:

1. **Input Data**:
   - `/home/user/data/system_a.json`: A JSON array of objects. Keys: `timestamp` (ISO8601), `msg` (string), `severity` (string).
   - `/home/user/data/system_b.csv`: A CSV file with a header row. Columns: `timestamp`, `message`, `severity`. Some rows have an empty `severity` column.

2. **Text Normalization**:
   - For all alerts (both systems), normalize the message text:
     - Convert to lowercase.
     - Replace all non-alphanumeric characters with spaces.
     - Collapse multiple consecutive spaces into a single space.
     - Trim leading and trailing spaces.

3. **Imputation via Similarity**:
   - For any CSV record with a missing severity, you must impute it by finding the most similar normalized message from the JSON dataset.
   - Use the **Jaccard Similarity** over the set of words in the normalized messages. (Jaccard = size of intersection / size of union).
   - Assign the `severity` of the JSON record that yields the highest Jaccard similarity. If there is a tie, pick the severity of the matching JSON record that occurs earliest in the JSON file. If a CSV message shares no words with any JSON message, assign the severity `"UNKNOWN"`.

4. **Anomaly Detection**:
   - Group the unified dataset (JSON + CSV) by their normalized messages.
   - For each distinct normalized message, sort its occurrences by timestamp.
   - An anomaly is defined as **4 or more** occurrences of the *exact same* normalized message occurring within a **10-minute (600 seconds) inclusive window**. (i.e., the time difference between the 1st and 4th occurrence in any contiguous sequence of 4 is <= 10 minutes).

5. **Output**:
   - Ensure the `/home/user/output/` directory exists.
   - **Unified Data**: Write all records (both JSON and CSV) to `/home/user/output/unified.jsonl` as JSON Lines (one JSON object per line). Each object must have keys: `timestamp` (string, preserved as-is), `normalized_msg` (string), and `severity` (string, the original or imputed one). The lines must be sorted chronologically by timestamp (earliest first). If timestamps match exactly, order JSON records before CSV records.
   - **Anomalies Report**: Write `/home/user/output/anomalies.txt`. List the normalized messages that met the anomaly criteria, one per line, sorted alphabetically. If none, leave the file empty.

You can write your Go code anywhere in `/home/user/` (e.g., `/home/user/etl/main.go`) and run it to produce the outputs. Standard library only is preferred, but you may install external Go modules if absolutely necessary.