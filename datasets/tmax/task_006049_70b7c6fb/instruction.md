You have recently inherited an unfamiliar, legacy data processing system. The previous developer left behind a partially broken ingestion pipeline located in `/home/user/app`.

The system reads a custom Write-Ahead Log (WAL) file called `data.wal`. Unfortunately, the system crashed during the last write cycle, and `data.wal` is now corrupted with partial and malformed writes. 

You need to recover the data, run the legacy transformation step, and compare the result against a known-good checkpoint.

Here is what you know from the previous developer's notes:
1. `data.wal` is a CSV file where each line represents an operation. The fields are: `timestamp,operation,value,checksum`.
2. A valid WAL entry must have exactly 4 fields. Furthermore, as a strict assertion-based validation, the `checksum` (4th field) must exactly equal the mathematical sum of the `timestamp` (1st field) and the `value` (3rd field). Any line failing this assertion is corrupted and must be dropped.
3. The legacy script `/home/user/app/transform.sh` takes a valid CSV file as an argument and computes the final state, writing it to `/home/user/app/current_state.json`.

**Your Task:**
1. Write a Bash script at `/home/user/app/recover.sh` that reads `/home/user/app/data.wal`, filters out all corrupted lines based on the checksum assertion, and writes the valid lines to `/home/user/app/recovered.csv`.
2. Execute `/home/user/app/transform.sh` using your newly created `/home/user/app/recovered.csv` as the input.
3. The transformation will produce `/home/user/app/current_state.json`. Perform a diff analysis to trace the intermediate state drift by running `diff -u /home/user/app/known_good.json /home/user/app/current_state.json > /home/user/app/state.diff`. (It is expected that there will be a diff, as the new operations have advanced the state).

Make sure all files are created exactly at the specified paths.