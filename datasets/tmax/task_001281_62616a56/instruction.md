You are an Operations Engineer triaging a P1 incident in our log ingestion pipeline. A recent deployment caused the ingestion worker to crash, broke parsing for our legacy log formats, and allowed malicious payloads to bypass our security filters. 

Your objectives are divided into three phases:

**Phase 1: Multi-Service Pipeline Restoration**
We have a local log pipeline fixture located in `/app/`. It consists of:
1. A Redis message broker.
2. `api.py`: A FastAPI service on port 8080 that receives HTTP POST requests at `/ingest` and pushes them to Redis.
3. `worker.py`: A background service that pulls logs from Redis, parses them, and writes valid logs to `/app/processed.log`.

Currently, the startup script `/app/start_services.sh` fails to produce a working pipeline. The services are not communicating correctly due to misconfigurations in `/app/config.ini`. 
- Reconfigure the settings so that sending a POST request to `http://localhost:8080/ingest` with `{"log": "test"}` results in the log being processed and written to `/app/processed.log`.

**Phase 2: Git Bisection and Bug Fixing**
The parsing logic used by the worker is maintained in a local Git repository at `/home/user/log_parser_repo`. A recent commit introduced a build failure (syntax/import error) and a regression in handling legacy string-escaped log formats.
- Use `git bisect` to identify the commit that introduced the parsing regression.
- Fix the bug in `/home/user/log_parser_repo/parser.py` so that both modern JSON logs and legacy escaped logs (e.g., `{"msg": "\"legacy format\""}`) are parsed successfully without throwing exceptions.
- Reinstall the fixed package into the system Python environment so the `worker.py` can use it.

**Phase 3: Security Detector Construction**
The pipeline is currently vulnerable to malicious injection attacks disguised as log entries. You must write a standalone Python security detector script at `/home/user/detector.py`.

The security team will test your script against two hidden directories of log files:
- A `clean` corpus of valid edge-case logs (which must be ACCEPTED).
- An `evil` corpus containing malicious payloads like JNDI lookups, SQL injections, and cross-site scripting signatures (which must be REJECTED).

Your script must conform to this exact CLI signature:
`python3 /home/user/detector.py <input_dir> <output.csv>`

For every `.log` file in `<input_dir>`, your script must analyze the file's contents and append a row to `<output.csv>` in the format: `filename,decision` where `decision` is strictly the word `ACCEPT` or `REJECT`.

To pass, your detector must have zero false positives (accept 100% of the clean corpus) and zero false negatives (reject 100% of the evil corpus).