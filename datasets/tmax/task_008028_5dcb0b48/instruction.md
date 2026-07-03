You have just inherited an unfamiliar codebase located at `/home/user/project`. Your team relies on this repository to process data files, but the pipeline is currently broken and suffers from multiple issues.

Your goals are to diagnose and fix the build failures, resolve a concurrency bug, and perform some git forensics to recover a lost credential.

Here are your specific objectives:
1. **Fix the Build Script**: The main entry point is `/home/user/project/build.sh`. It is supposed to iterate over all `.txt` files in the `data/` directory and pass them to `processor.py` to be processed in parallel. However, it currently crashes or processes files incorrectly because some filenames contain spaces. Modify `build.sh` so that it correctly passes the filenames to `processor.py` and waits for all background processes to finish.

2. **Fix the Concurrency Bug**: The Python script `processor.py` processes each file and updates a shared JSON file called `summary.json` with the total sum of the numbers found in the processed files. Because `build.sh` launches `processor.py` instances in parallel, there is a race condition where multiple processes read and write `summary.json` simultaneously, leading to data loss and an incorrect final sum. Modify `processor.py` to ensure process-safe read-modify-write operations on `summary.json` (e.g., by using file locking). The final sum in `summary.json` must be perfectly accurate when `./build.sh` completes.

3. **Recover a Lost Secret**: A previous developer accidentally committed a database password into the git repository, which was later removed. You need to search the git history of `/home/user/project` to find this old database password (look for `DB_PASS`). Once you find it, save the exact password string to `/home/user/secret.txt`.

To complete the task:
- Fix `build.sh` and `processor.py`.
- Run `./build.sh` so that it successfully processes all files and generates the correct `summary.json`.
- Extract the deleted secret and save it to `/home/user/secret.txt`.