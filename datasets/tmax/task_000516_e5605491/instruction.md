You are tasked with building a configuration drift analysis tool for a fleet of network switches. Over time, switches emit their running configuration as a text stream, which we capture in a log file. However, the logging system is imperfect: some timestamps are dropped, and the configuration formats vary slightly with varying punctuation and casing.

You need to write a Go program at `/home/user/analyze_drift.go` that streams a large log file `/home/user/changes.log` and compares each entry to a baseline configuration in `/home/user/baseline.txt`.

The program must perform the following steps for each line in `/home/user/changes.log`:

1. **Large-File Streaming**: Read `/home/user/changes.log` line-by-line to avoid loading the entire file into memory (assume the file could be arbitrarily large). Each line is formatted as `TIMESTAMP | CONFIG_TEXT`.
2. **Gap-Filling**: The `TIMESTAMP` is in ISO 8601 format (e.g., `2023-10-01T10:00:00Z`). Sometimes the timestamp is literally the string `MISSING`. When you encounter `MISSING`, you must fill the gap by adding exactly 5 minutes (`5m`) to the *timestamp of the immediately preceding line* (whether that preceding timestamp was parsed from the file or was itself gap-filled). The first line in the log is guaranteed to have a valid timestamp.
3. **Tokenization and Normalization**: To compare the configurations, you must normalize both the `baseline.txt` content and the `CONFIG_TEXT` from each log line:
   - Convert the entire text to lowercase.
   - Replace all non-alphanumeric characters (anything that is not `a-z` or `0-9`) with a single space.
   - Split the resulting string by whitespace to get a list of tokens.
   - Deduplicate the tokens to form a mathematical Set of unique tokens. Discard any empty tokens.
4. **Distance and Similarity Computation**: Calculate the Jaccard Similarity between the baseline's token set and the log line's token set. 
   - Jaccard Similarity = (Size of Intersection) / (Size of Union).
   - If both sets are empty, the similarity is `1.0`.

Your program must write its output to a CSV file at `/home/user/drift_report.csv`. 
Each line of the CSV should represent one log entry, formatted exactly as:
`TIMESTAMP,SIMILARITY_SCORE`
Where `TIMESTAMP` is the valid (or filled) ISO 8601 timestamp (e.g., `2023-10-01T10:00:00Z`), and `SIMILARITY_SCORE` is formatted to exactly 4 decimal places (e.g., `0.7500`).

Compile and run your Go program to generate the `/home/user/drift_report.csv` file.