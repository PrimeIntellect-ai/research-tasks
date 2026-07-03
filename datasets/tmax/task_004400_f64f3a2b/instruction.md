You are acting as a support engineer collecting diagnostics and fixing a critical pipeline for our data ingestion system.

We have a vendored package located at `/app/vendored/math-ingest-v1.2.0/` which contains a set of Bash scripts and a pre-compiled Rust binary (`/app/vendored/math-ingest-v1.2.0/bin/checksum_calc`). This binary reads an append-only log file (a simplistic WAL format) and calculates a proprietary mathematical checksum for each record.

Recently, the WAL file at `/home/user/data/ingest.wal` became corrupted due to a disk failure. When the `checksum_calc` binary processes this corrupted file, it intermittently panics (specifically, an `unwrap()` fails on certain malformed mathematical edge cases in the data), crashing the entire diagnostic pipeline. 

Your task is to:
1. Diagnose the exact input that causes the intermittent panic by reproducing the failure against the binary.
2. Recover the uncorrupted records from the WAL file. The format of a valid WAL record is `[TIMESTAMP] (ID) DATA_VALUE`. Corrupted records may have malformed timestamps or non-numeric data values. Extract only the valid records to `/home/user/recovered_records.txt`.
3. Reverse engineer the mathematical checksum logic. Since the binary panics and we cannot recompile it right now (the Makefile is perturbed and the source patch is missing in the vendored directory), you must deduce the mathematical operations it performs on the `DATA_VALUE` of valid inputs.
4. Write a pure Bash script at `/home/user/robust_checksum.sh` that takes a single integer as an argument and outputs the calculated checksum exactly as the Rust binary would (when it doesn't panic). 

Your Bash script will be tested against a hidden, uncorrupted reference implementation using a random-fuzzer. It must be bit-exact equivalent in its standard output.

Requirements for `/home/user/robust_checksum.sh`:
- Must be pure Bash (coreutils are fine, but no external languages).
- Must take exactly one argument (the `DATA_VALUE` integer).
- Must print only the final computed integer to stdout.