You are a DevOps engineer tasked with replacing a legacy log-parsing system. You have been asked to write a Python script that exactly replicates the behavior of a legacy compiled oracle (`/app/oracle_parser`) for processing system logs.

However, the environment is currently in a broken state:
1. **Missing Schema**: The required parsing schema file (`/tmp/schema.json`) was accidentally deleted by a careless coworker. Fortunately, a background daemon (`/app/legacy_daemon.py`) is still running and holds an open file descriptor to the deleted schema. You must recover the exact contents of this schema file and save it to `/home/user/schema.json`.
2. **Vendored Package Conflict**: You must use a proprietary log parsing library whose source is located at `/app/log-cruncher-0.5/`. Currently, it cannot be installed because of a severe dependency conflict in its `setup.py`. You need to resolve this conflict and install it locally using `pip install -e /app/log-cruncher-0.5/`.
3. **Library Crash**: The `log-cruncher` library contains a known bug. A previous crash produced a traceback located in `/app/crash_traceback.log`. You must analyze this traceback, identify the faulty line in `/app/log-cruncher-0.5/cruncher/parser.py`, and fix it so it can handle malformed log levels gracefully.
4. **Implementation**: Once the library is fixed and installed, write a script at `/home/user/parse_logs.py`. Your script must take a single command-line argument (a raw log string), utilize the `log-cruncher` library and the recovered `schema.json`, and print the resulting parsed JSON to standard output.

Your implementation must be bit-exact equivalent to the legacy binary. Automated verification will run thousands of randomly generated log strings through both `/app/oracle_parser` and `/home/user/parse_logs.py` to ensure their outputs are identical.

Constraints:
- You do not have root access.
- Do not attempt to decompile the oracle.
- Save your final script exactly at `/home/user/parse_logs.py`.