You are an on-call engineer and have just been paged at 3:00 AM. The primary data processing service has gone down, and the system is in a degraded state. 

Here is the situation:
1. **Corrupted WAL**: The Write-Ahead Log (WAL) located at `/home/user/wal.log` experienced a partial write during a power fluctuation, resulting in corrupted entries. 
   The log format is strictly: `SEQ|ACTION|KEY|VALUE|CHECKSUM`
   - `SEQ`: A monotonically increasing integer sequence number.
   - `ACTION`: A string (e.g., `SET` or `DEL`).
   - `KEY`: The data key (string).
   - `VALUE`: The data value (string).
   - `CHECKSUM`: The exact byte count of `KEY` concatenated with `VALUE`. For example, if KEY is "abc" and VALUE is "defg", the CHECKSUM must be 7.
   
   **Your task**: Write a Bash script at `/home/user/recover.sh` that reads `/home/user/wal.log` and writes all perfectly valid lines (correct format, correct checksum) to `/home/user/wal_recovered.log`. Discard any corrupted lines.

2. **Off-by-one Error**: The processor script `/home/user/apply_wal.sh` takes a target sequence number as its first argument and applies transactions from `wal_recovered.log` up to that `SEQ`. However, there is a known off-by-one boundary bug where it fails to apply the transaction that exactly matches the target `SEQ` (it processes strictly less than).
   
   **Your task**: Fix the boundary condition bug in `/home/user/apply_wal.sh` in place so that it processes transactions inclusive of the target `SEQ`.

3. **Poison Pill Transaction**: Even after fixing the WAL and the processor, running `/home/user/apply_wal.sh 99999` against the recovered WAL still crashes with a non-zero exit code due to a specific "poison pill" transaction that causes internal state corruption.
   
   **Your task**: Use a bisection or delta-debugging approach to identify the exact `SEQ` number of the single transaction that causes the script to crash. Write ONLY this integer `SEQ` to `/home/user/poison_seq.txt`.

Ensure all requested output files (`/home/user/wal_recovered.log`, `/home/user/poison_seq.txt`) are created with the correct information, and that `/home/user/apply_wal.sh` has been modified to fix the boundary bug.