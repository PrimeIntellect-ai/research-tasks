You are an infrastructure engineer working on a configuration manager that tracks system state changes. The system exports delta logs in a strict, pseudo-JSON text format, but the exporter has a bug: it sometimes encodes string values using Unicode escape sequences (e.g., `\u0061` instead of `a`). 

Your task is to write a C program that parses these logs, calculates summary statistics, and generates a clean CSV file for bulk database importing.

**Input Data:**
A file exists at `/home/user/changes.txt`. Each line in the file is strictly formatted as:
`{"cfg_id": <INTEGER>, "delta": <FLOAT>, "status": "<STRING>"}`
*   `<INTEGER>` is an ID between 1 and 100.
*   `<FLOAT>` is a decimal number representing the configuration change delta.
*   `<STRING>` is a status indicator. It will evaluate to either `active` or `inactive`, but characters may be obfuscated as `\uXXXX` (e.g., `\u0061\u0063\u0074\u0069\u0076\u0065` represents `active`). 

**Requirements:**
1.  **C Implementation:** Write a C program at `/home/user/parser.c` and compile it to `/home/user/parser`. You must use C to process the file and perform the calculations.
2.  **Decoding:** The C program must correctly interpret `\uXXXX` hex sequences in the status string into standard ASCII characters to determine the true status.
3.  **Aggregation:** For each unique `cfg_id`, calculate the arithmetic mean (average) of the `delta` values.
4.  **Quality Gate:** *Only* include records where the decoded status is exactly `active`. Completely ignore records with an `inactive` status.
5.  **Export Format:** Generate a CSV file at `/home/user/db_import.csv` containing the aggregated results.
    *   The first line must be the header: `cfg_id,avg_delta`
    *   Following lines must contain the ID and the average delta formatted to exactly two decimal places (e.g., `3.50`).
    *   Only output rows for `cfg_id`s that have at least one `active` record.
    *   The rows must be sorted by `cfg_id` in ascending order.

Run your compiled C program to produce the `/home/user/db_import.csv` file. Ensure the file is completely accurate so the automated bulk import tests pass.