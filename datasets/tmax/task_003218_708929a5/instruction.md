You are a support engineer tasked with collecting diagnostic logs from a failing distributed system. You have been provided with a diagnostic extraction script at `/home/user/log_collector.py` and a dataset of raw logs at `/app/raw_logs.txt`.

The script relies on a highly optimized JSON parser, `ujson`, which has been vendored at `/app/vendored/ujson-5.7.0` because the production environment is fully air-gapped. 

Currently, you face two issues:
1. The vendored `ujson` package fails to build and install from source. You must diagnose the build failure, patch the C/C++ or Python source of the vendored package, and successfully install it (`pip install -e .` inside the vendored directory).
2. Once installed, `log_collector.py` runs, but it suffers from a race condition. It uses Python's `multiprocessing` to parse logs and writes out to `/home/user/diagnostics.jsonl`. Because multiple worker processes write to the same file concurrently without synchronization, the output is frequently corrupted (interleaved text) and log lines are dropped.

Your tasks:
1. Fix the build failure in `/app/vendored/ujson-5.7.0` and install it.
2. Fix the concurrency bug in `/home/user/log_collector.py` so that no logs are corrupted or dropped. You may modify the script to use proper locking, or refactor it to aggregate results in the main process before writing.
3. Run the script to process all logs in `/app/raw_logs.txt`.

The final output must be exactly at `/home/user/diagnostics.jsonl`. An automated test will evaluate the number of uncorrupted, perfectly valid JSON lines in this file. You must maximize the number of successfully recovered logs.