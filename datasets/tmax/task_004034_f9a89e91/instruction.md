You are an application log analyst investigating error patterns across multiple servers. You have an incoming stream of time-series log data in CSV format, but you've noticed that multiline log messages (which contain embedded newlines) are mysteriously disappearing from the pipeline.

Your investigation reveals that the system relies on a local, third-party package called `py_custom_csv` to parse these streams. This package has a bug where it silently drops CSV rows containing embedded newlines.

Your task has two parts:

1. **Fix the vendored package**:
   The source code for `py_custom_csv` is located at `/app/py_custom_csv-0.1/`. Modify the parser implementation (likely in `parser.py`) so that it correctly parses standard CSV data with embedded newlines (RFC 4180 compliant) instead of dropping or corrupting those rows. Make sure the package works correctly.

2. **Implement the log analyzer**:
   Write a Python script at `/home/user/log_analyzer.py` that acts as a stream processor. It must:
   - Read CSV data from standard input (`sys.stdin`) using the fixed `py_custom_csv.parse()` function.
   - Expect rows with exactly three columns: `timestamp`, `server_id`, `message`. Skip any row that does not have exactly three columns.
   - Skip the header row if it exactly matches `timestamp,server_id,message`.
   - For each valid data row, normalize the `message` field:
     - Convert the entire message to lowercase.
     - Replace any sequence of whitespace characters (spaces, tabs, newlines, etc.) with a single space character.
     - Strip any leading or trailing whitespace.
   - Compute the Jaccard similarity between the current normalized message and the *immediately preceding* normalized message for the *same* `server_id`.
     - To compute Jaccard similarity, split the normalized messages into sets of words using space (` `) as the delimiter.
     - Similarity = (size of intersection of word sets) / (size of union of word sets).
     - If both sets are empty, the similarity is `1.0`.
   - Output a JSON Line to standard output (`sys.stdout`) for every valid row processed, in the following exact format:
     `{"timestamp": "<timestamp>", "server_id": "<server_id>", "normalized_message": "<normalized_message>", "similarity": <float_or_null>}`
     - `<float_or_null>` should be the Jaccard similarity rounded to 4 decimal places (e.g., `0.3333`).
     - If there is no previous message for that `server_id`, the similarity value MUST be `null`.

Your script must cleanly process arbitrary length streams from stdin to stdout and must not crash on malformed inputs (just skip invalid rows). 

An automated verification system will feed thousands of randomly generated CSVs (with complex quoting and newlines) into your script and assert that your output is bit-exact equivalent to our reference implementation.