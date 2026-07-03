You are a DevOps engineer troubleshooting a custom mathematical aggregation service.

You have been given a compiled Go binary `/home/user/calc_engine` and a Write-Ahead Log (WAL) file `/home/user/tx.wal`. 
The `calc_engine` binary reads the WAL file sequentially, applying floating-point mathematical operations to a running state, and prints the final result.

Currently, the binary is failing to process the logs. You need to debug and fix the pipeline. Here is what you know:
1. The binary silently crashes on startup. You suspect it is missing an environmental configuration file that it expects to read on initialization. You should use system call tracing tools to identify what file it is looking for. The file should contain a single floating-point number representing the initial state (use `100.0` as the initial state).
2. Once the configuration is fixed, the binary will attempt to process `/home/user/tx.wal`. However, the WAL file got corrupted and contains some malformed entries (edge cases like invalid number formats or unknown operations). 
3. The binary is written poorly and panics when it encounters any invalid formatting, causing the whole process to abort.

Your task:
1. Identify and create the missing configuration file so the engine can start. (Set the initial state to `100.0`).
2. Write a minimal reproducible Go script (e.g., `/home/user/recover.go`) to read `/home/user/tx.wal`, identify and filter out the malformed/unparseable lines, and write a cleaned version of the log to `/home/user/recovered.wal`. A valid line consists exactly of an operation (`ADD`, `SUB`, `MUL`, `DIV`) followed by a single space and a valid standard floating-point number.
3. Run the binary against the recovered WAL file: `./calc_engine -file /home/user/recovered.wal`.
4. Save the final numerical output printed by the binary into `/home/user/result.txt`.

Ensure `/home/user/result.txt` contains nothing but the final computed floating-point number.