You are an AI assistant helping a technical writer organize documentation and error logs from a recent software testing cycle. 

You have been provided with a zip archive at `/home/user/docs_archive.zip`. Follow these instructions to process the files:

1. **Verify Archive Integrity:** First, test the integrity of `/home/user/docs_archive.zip` using standard command-line zip utilities. Redirect the standard output of this integrity check to `/home/user/integrity.txt`.
2. **Extract Files:** Extract the archive into a new directory called `/home/user/raw_docs/`.
3. **Parse Multi-line Logs (C++):** Inside the extracted files, there is a log file named `system.log`. The file contains multi-line log entries. Each new entry starts with a line formatted exactly as `[YYYY-MM-DD HH:MM:SS] LEVEL`. The message for that log entry spans all subsequent lines until the next entry begins or the file ends.
   Write a C++ program at `/home/user/parse_logs.cpp`, compile it, and run it to parse `system.log`. Your program must:
   - Identify all log entries where the `LEVEL` is `ERROR`.
   - Extract the timestamp (without the brackets) and the complete multi-line message.
   - Convert the multi-line message into a single string by replacing all newline characters within the message with a single space character. Strip any leading or trailing whitespace from the final message string.
   - Output the results to a CSV file at `/home/user/errors.csv` with the header `Timestamp,Message`. Include the extracted errors in chronological order. Enclose the message in double quotes if necessary, but since newlines are replaced by spaces, standard comma-separation is fine (ensure no stray commas in the message break the CSV, or simply enclose every message in double quotes). Let's standardize on enclosing every message in double quotes: `"Timestamp","Message"`.
4. **Package Final Documentation:** Find all Markdown files (`*.md`) inside `/home/user/raw_docs/` (and its subdirectories) and package them along with `/home/user/errors.csv` into a new compressed tarball at `/home/user/final_docs.tar.gz`. When creating the tarball, do not include absolute paths (store them relative to `/home/user/`).

Ensure your C++ program is robust and correctly handles the multi-line parsing logic.