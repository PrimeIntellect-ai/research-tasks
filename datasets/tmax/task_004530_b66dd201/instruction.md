You are a data engineer tasked with building a text processing ETL pipeline for customer support tickets. 

You have been provided with a raw, unstructured text file located at `/home/user/raw_tickets.txt`. This file contains support tickets separated by `===`.

Your goal is to build a multi-stage pipeline using Bash and Python (standard library only, no external packages like `pandas` or `scikit-learn` allowed) that extracts, deduplicates, groups, and logs the processing of these tickets.

Here are the requirements:

1. **Extraction**: Write a Python script to parse `/home/user/raw_tickets.txt`. Each ticket block contains a Ticket ID, an Email, and an Issue Description. Extract these into structured records.
2. **Hash-based Deduplication**: Some tickets were submitted multiple times by the system. Use SHA-256 hashing on the extracted "Issue Description" string (stripped of leading/trailing whitespace, converted to lowercase) to identify exact duplicates. Keep only the first occurrence (based on the order in the file) and discard subsequent exact duplicates.
3. **Similarity-based Grouping**: For the remaining unique tickets, compute the text similarity of the "Issue Description" using Python's built-in `difflib.SequenceMatcher`. Group tickets together if the `ratio()` of their issue descriptions is `>= 0.85`. A group should be represented by a list of Ticket IDs. If a ticket does not match any other, it is in a group by itself.
4. **Output**: Write the final grouped tickets to `/home/user/grouped_tickets.json`. The format should be a JSON array of arrays, where each inner array contains the Ticket IDs (as strings) of a similar group. Sort each inner array alphabetically, and sort the outer array by the first Ticket ID in each inner array.
5. **Logging**: The pipeline must log its execution to `/home/user/pipeline.log`. The log must contain exactly these lines:
   - `TOTAL_RAW: <number>`
   - `TOTAL_UNIQUE_AFTER_HASH: <number>`
   - `TOTAL_GROUPS: <number>`
6. **Orchestration**: Create a bash script at `/home/user/run_pipeline.sh` that, when executed, runs your Python script(s) and produces the required outputs.

You must build the scripts and then execute `/home/user/run_pipeline.sh` so that the final files are generated.

Example raw ticket block:
```
Ticket: TKT-001
Contact: user@example.com
Description: I cannot reset my password. The link gives a 404 error.
===
```