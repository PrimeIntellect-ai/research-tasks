I've inherited a messy project and need your help getting it back on track. We have a custom vendored data processing library located at `/app/vendor/quant-db-1.2.0/`. It's a Python package that wraps a C extension for fast numerical processing and logging. However, it's currently broken due to an environment misconfiguration in its build system (the `setup.py` has a broken include path and missing compiler flag). 

Once you fix the build configuration and install the package locally, you'll discover that the library has a floating-point precision bug in its core aggregation logic (`aggregator.c`), which causes accumulated sums of small floats to drift drastically. You need to debug and fix this C code so that precision is maintained (e.g., using Kahan summation or double precision where appropriate).

Next, we had a crash, and our system's Write-Ahead Log (WAL) at `/app/data/transaction.wal` was corrupted. The WAL contains a series of binary records. Using the now-fixed `quant-db` library, you must write a script to recover the valid entries from this corrupted WAL file and dump them into `/app/data/recovered_records.json`.

Finally, we are receiving incoming telemetry payloads. Some of these payloads are maliciously crafted to exploit a vulnerability in an older version of our system, while others are legitimate. I have provided a corpus of known malicious payloads in `/app/corpus/evil/` and legitimate payloads in `/app/corpus/clean/`. 
You need to write a Python script at `/home/user/sanitizer.py` that takes a directory path as a command-line argument, reads all `.dat` files within it, and outputs `REJECT` or `ACCEPT` for each file on standard output (format: `<filename>: ACCEPT/REJECT`). Your script must correctly classify 100% of the files in both corpora based on the structural anomalies present in the evil corpus.

To summarize, your tasks are:
1. Fix the environment/build configuration of `/app/vendor/quant-db-1.2.0/` and install it.
2. Fix the floating-point precision bug in the C extension.
3. Recover the database records from `/app/data/transaction.wal` into `/app/data/recovered_records.json`.
4. Create the filter script at `/home/user/sanitizer.py` to classify payloads.