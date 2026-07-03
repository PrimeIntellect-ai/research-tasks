You are a data engineer tasked with cleaning up time-series datasets. Recently, an upstream ETL job has been malfunctioning, producing duplicate records on retry, missing samples (gaps), and failing to properly normalize output values.

We have a proprietary, stripped binary located at `/app/etl_oracle` which correctly validates these datasets. It takes a single file path as an argument and exits with `0` if the dataset is "clean", and `1` if the dataset is "corrupted" (e.g., contains duplicates, gaps, or unnormalized values). 

Because we are migrating our pipeline to a different architecture, we can no longer use this closed-source binary. Your task is to reverse-engineer its validation logic (treating it as a black-box oracle or using binary analysis tools) and reimplement it in C.

Write your C program at `/home/user/filter_etl.c` and compile it to `/home/user/filter_etl`.

Requirements:
1. Your compiled binary `/home/user/filter_etl` must take exactly one argument: the path to a CSV dataset.
2. The CSV files contain two columns without a header: `timestamp_ms` (a long integer) and `value` (a float). Example: `1600000050,0.45`
3. Your program must exit with code `0` if the file perfectly adheres to the cleaning rules (matching the oracle's definition of a "clean" dataset).
4. Your program must exit with a non-zero code (e.g., `1`) if the file violates any of the rules (matching the oracle's definition of an "evil" dataset).
5. The dataset validation rules involve standard time-series checks: monotonic ordering, strict gap enforcement (resampling interval), and value normalization bounds. Use the `/app/etl_oracle` on sample files you generate to deduce the exact constants and constraints.

Your final deliverable is the compiled executable at `/home/user/filter_etl`.