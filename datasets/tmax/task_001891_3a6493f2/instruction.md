You have just inherited an unfamiliar codebase responsible for performing mathematical transformations on transaction values. The system uses a C program (`process_math.c`) to read transaction entries from a Write-Ahead Log (WAL) and compute a scaled result based on a dynamic coefficient. 

Recently, the system suffered an intermittent failure and crashed, leaving behind a raw memory dump and a partially corrupted WAL file.

Your objective is to recover the system state, fix the intermittent bug, and process the remaining valid data.

Here is what you have in `/home/user/`:
1. `/home/user/process_math.c`: The source code for the calculation engine. It takes the secret coefficient as a command-line argument and reads WAL entries from `stdin`. It appears to crash intermittently on specific transaction values.
2. `/home/user/memdump.dat`: A raw memory dump captured during the crash. The secret coefficient used during the last run is still present in this dump in the format `SECRET_COEFF=<number>`.
3. `/home/user/data.wal`: The Write-Ahead Log containing the transactions. Due to the crash, some lines have been corrupted with non-ASCII binary garbage. Valid lines follow the exact format: `TX:<id> VAL:<number>`.

Perform the following steps:
1. **Memory Dump Analysis:** Extract the numerical value of `SECRET_COEFF` from `/home/user/memdump.dat`.
2. **Database Recovery:** Parse `/home/user/data.wal` to extract only the perfectly valid, uncorrupted transaction lines. Filter out any lines containing non-ASCII characters or garbage. Save these valid lines to `/home/user/clean.wal`.
3. **Intermittent Bug Fix:** Inspect `/home/user/process_math.c`. There is a bug that causes a segmentation fault on certain mathematical conditions. Fix the bug so that the program safely processes all valid numbers. Compile your fixed version into an executable named `/home/user/process_math`.
4. **Final Processing:** Run your compiled `./process_math` using the extracted `SECRET_COEFF` as the first argument, feeding it `/home/user/clean.wal` via standard input. Redirect the standard output to `/home/user/recovered_results.txt`.

The automated test will verify the contents of `/home/user/recovered_results.txt`. It must contain the final computed results for all valid transactions in the exact output format produced by the C program.