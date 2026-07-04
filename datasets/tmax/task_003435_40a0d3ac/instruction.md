You are a data engineer building an ETL pipeline for IoT sensor data. Occasionally, our upstream ingestion service retries and produces duplicate records, or encounters corruption that introduces malicious/invalid records.

Your goal is to build a Go-based ETL pipeline that sanitizes, sorts, deduplicates, gap-fills, and calculates rolling statistics on this data.

There are two main components to this task:

1. **Fix the Vendored Package**:
   We rely on a third-party package for rolling statistics, vendored at `/app/vendored/go-rollstat` (version 1.0.4). However, the package currently fails to compile because its `Makefile` specifies an incorrect build tag. The `Makefile` uses `go build -tags=prod`, but the source code is conditionally compiled with `//go:build production`. Fix this perturbation so the package builds successfully and can be imported.

2. **Implement the ETL Filter and Processor**:
   Write a Go program at `/home/user/etl.go` that takes an input JSONL file and an output JSONL file as command-line arguments:
   `go run /home/user/etl.go <input.jsonl> <output.jsonl>`

   The program must perform the following pipeline operations in order:
   
   a. **Filter (Sanitization)**: Read the input JSONL file. Each line is expected to be a JSON object: `{"ts": <int64>, "val": <float64>, "id": "<string>"}`. 
      You must DROP (ignore) any record that meets ANY of these "evil" criteria:
      - `ts` (timestamp) is less than or equal to 0.
      - `val` is strictly outside the range `[-100.0, 100.0]`.
      - `id` contains any characters other than uppercase letters and digits (e.g., must match `^[A-Z0-9]+$`).
   
   b. **Sort & Deduplicate**: Sort the surviving valid records in ascending order by `ts`. If there are exact duplicate records (same `ts`, `val`, and `id`), keep only the first one. If there are records with the same `ts` but different `val` or `id`, keep the one that appears first in the input file and drop the others.

   c. **Resample & Gap-Fill**: The timestamps are in seconds. Ensure there is a record for every single second between the minimum `ts` and maximum `ts` in the dataset. If a second is missing, create a synthetic record copying the `val` and `id` of the immediately preceding valid record.

   d. **Rolling Statistics**: Using the fixed `go-rollstat` package (which provides a `rollstat.Window` type), calculate a 3-second rolling average of the `val` field for each record (including gap-filled ones). The rolling average for a record at time `T` should be the average of `val` at `T-2`, `T-1`, and `T`. If there are fewer than 3 records available (e.g., at the start of the series), average whatever is available. Add this as a new field `avg` to the output JSON.

   e. **Output**: Write the final processed records to the specified output file in JSONL format, keeping the `ts`, `val`, `id`, and adding the new `avg` field (rounded to 2 decimal places).

We will test your solution against a suite of adversarial datasets. Your program must preserve 100% of clean, valid records, and reject 100% of the evil records, producing the correct contiguous, aggregated output.