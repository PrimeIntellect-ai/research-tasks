You are a data engineer building an ETL pipeline in C++. We have a legacy vendored library used for CSV parsing, and you need to build a sanitization filter that consumes data, masks PII, removes duplicates (a known issue caused by upstream retry loops), and filters anomalies.

Part 1: Fix the Vendored Package
We have a vendored CSV/string utility library located at `/app/vendored/libcsv_etl`. 
Unfortunately, the previous maintainer left a deliberate perturbation in its `Makefile` that defines a macro causing internal retry loops to yield duplicate lines. 
1. Inspect the `Makefile` and source code of `/app/vendored/libcsv_etl`.
2. Fix the bug in the Makefile so it builds correctly without producing duplicates on retries.
3. Build the library (it generates `libcsv_etl.a` and `csv_etl.h`).

Part 2: Write the Sanitizer
Write a C++ program at `/home/user/sanitizer.cpp` and compile it to `/home/user/sanitizer`.
Link it against the fixed `libcsv_etl.a`.
Your program must read a CSV stream from `stdin` and write the sanitized CSV to `stdout`.

The CSV has the following header:
`timestamp,tx_id,card_number,amount,status`

Your sanitizer must process the stream line-by-line and enforce the following rules:
1. **Constraint Validation**: Reject (drop) the record if `status` is not exactly `SUCCESS` or `PENDING`.
2. **Data Masking**: The `card_number` is a 16-digit string. You must mask the first 12 digits with `*`, leaving only the last 4 digits (e.g., `1234567890123456` becomes `************3456`).
3. **Duplicate Detection**: The upstream source often retries on failure, yielding duplicate `tx_id`s. You must keep track of seen `tx_id`s and drop any record with a `tx_id` you have already processed.
4. **Rolling Statistics / Anomaly Detection**: Maintain a rolling average of the `amount` field for the last 3 *accepted* records (including the current one being evaluated). If the inclusion of the current record's `amount` would cause this rolling average to exceed `5000.0`, drop the record (and do not include its amount in the rolling window history).

Ensure your output CSV includes the header row. Use the included `csv_etl::split(line)` function from the vendored library if helpful.

A verification script will test your compiled `/home/user/sanitizer` against a clean dataset and an evil dataset. Ensure it handles both flawlessly.