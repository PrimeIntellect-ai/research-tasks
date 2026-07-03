You are a data engineer tasked with fixing and completing an ETL pipeline. 

A startup script has already launched a local data sink service (a Python Flask app) running on `http://127.0.0.1:5000`. This service receives processed JSON records and stores them in a backend SQLite database for analytics.

Currently, there is a buggy Go ETL worker located at `/home/user/etl/main.go`. This worker reads a raw dataset from `/home/user/data/input.csv` and pushes the data to the sink. However, it has severe issues:
1. **Data Loss via Naive Parsing:** The Go script reads the file line-by-line using `bufio.Scanner`. Unfortunately, the CSV `notes` column contains embedded newlines. Because of the naive scanner, these rows are being split incorrectly, corrupted, and silently dropped by the pipeline.
2. **Missing Feature Extraction:** The `contact_info` column contains unstructured text (e.g., "Reach out to john.doe@example.com for info"). You need to use a regular expression to extract the email address into an `email` field, and extract the domain into an `email_domain` field.
3. **Inconsistent Dates:** The `event_date` column contains dates in mixed formats (e.g., `12/31/2022`, `2022-12-31`, `31-12-2022`). They must be normalized to standard ISO 8601 `YYYY-MM-DD`.

Your task:
1. Modify `/home/user/etl/main.go` to properly parse the CSV (handling embedded newlines natively, e.g., using `encoding/csv`).
2. Implement the regex extraction for `email` and `email_domain`. If no email is found, set them to empty strings.
3. Normalize the `event_date` to `YYYY-MM-DD`. If a date is unparseable, leave it as an empty string.
4. Replace all newline (`\n`) and carriage return (`\r`) characters in the `notes` field with a single space to standardize the output.
5. The Go application must send the cleaned data to the sink via a `POST` request to `http://127.0.0.1:5000/ingest` with a JSON payload in this exact format:
   ```json
   {
     "id": "101",
     "notes": "cleaned string with no newlines",
     "email": "john.doe@example.com",
     "email_domain": "example.com",
     "event_date": "2022-12-31"
   }
   ```
6. Compile and run your Go application so that it fully processes `/home/user/data/input.csv` and populates the sink service.

The automated verification will query the sink's internal database to compute the accuracy of your extraction and transformation. You must achieve an accuracy of at least 95%.