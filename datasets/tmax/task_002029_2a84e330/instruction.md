You are an on-call engineer responding to a 3 AM page. Our legacy event normalization service has crashed. We are migrating this service to Python, but the migration is incomplete. 

The original service is compiled into a stripped binary located at `/app/time_oracle`. This binary implements our proprietary "time-shift" logic for normalizing timestamps. 

Before the crash, the system was processing events from a local SQLite database at `/home/user/data/events.db`. The main database file is corrupted, but there is a WAL (`events.db-wal`) file that contains uncommitted transactions.

Your tasks:
1. **Dependency Resolution**: The python environment setup is failing. Fix the dependency conflicts in `/home/user/requirements.txt` and install the requirements in a virtual environment at `/home/user/venv`.
2. **Database Recovery**: Recover the corrupted SQLite database `/home/user/data/events.db`. Extract all the recovered event rows (id, timestamp, event_name) into a CSV file at `/home/user/recovered_events.csv`.
3. **Algorithm Reverse-Engineering**: The stripped binary `/app/time_oracle` takes a single argument: an integer UNIX epoch timestamp. It outputs a formatted date string using a proprietary timezone calculation. You must reverse engineer its behavior (treat it as a black box and observe its outputs) and implement the EXACT same logic in Python.
4. **Implementation**: Write your solution in `/home/user/processor.py`. This script must accept a single argument (the UNIX timestamp as a string), process it using your reverse-engineered logic, and print the exact same output string to stdout as the oracle binary. Do not print anything else.

The automated system will verify your `/home/user/processor.py` by fuzzing it against `/app/time_oracle` with thousands of random timestamps to ensure bit-exact equivalence.