You are a data engineer tasked with setting up a real-time ETL ingestion server. We process incoming application logs, clean them, and deduplicate highly similar entries before storing them.

We use a custom, in-house HTTP serving framework called `text-pipeline-server`. The source code for this framework is vendored on your machine at `/app/text-pipeline-server-1.0`.

Here is your multi-stage task:

**Stage 1: Fix and Install the Framework**
The vendored package at `/app/text-pipeline-server-1.0` has a known bug. In the file `text_pipeline/parser.py`, there is a regular expression meant to validate incoming `X-Batch-ID` headers (which should look like `batch-12345-prod`). The current regex is flawed and causes the server to reject all valid requests with a 400 Bad Request error.
1. Inspect `/app/text-pipeline-server-1.0/text_pipeline/parser.py`.
2. Fix the regex pattern so it correctly matches the format `batch-<digits>-<word>`.
3. Install the package locally in editable mode (e.g., using `pip install -e`).

**Stage 2: Implement the ETL Logic**
Create a Python script at `/home/user/etl.py` containing a function:
`def process_logs(raw_text: str) -> list[dict]:`

The function must perform the following:
1. **Extraction:** Split the `raw_text` into lines. Use a regex to parse each line which follows the format: `[YYYY-MM-DDTHH:MM:SS] [LEVEL] Message payload`. Ignore any lines that do not match this format exactly.
2. **Cleaning & Normalization:** For the extracted message payload, convert it to lowercase and remove all punctuation (keep only alphanumeric characters and spaces). 
3. **Similarity & Deduplication:** Compare the cleaned payloads of all parsed logs. Calculate the Jaccard similarity (based on space-separated words). If two logs have a Jaccard similarity $\ge 0.75$, they are considered duplicates. Deduplicate the logs such that for any group of duplicates, ONLY the log with the chronologically earliest timestamp is kept.
4. **Return Format:** Return a list of dictionaries, sorted chronologically, in the format: `{"timestamp": "...", "level": "...", "cleaned_message": "..."}`.

**Stage 3: Start the Server**
Use the CLI tool provided by the framework to start the service. You must run:
`text-pipeline-server --host 127.0.0.1 --port 8080 --handler /home/user/etl.py:process_logs`

Leave the server running in the background or terminal multiplexer. An automated testing suite will send HTTP POST requests to `http://127.0.0.1:8080/ingest` with raw text payloads and an `X-Batch-ID` header to verify your ETL pipeline's correctness.