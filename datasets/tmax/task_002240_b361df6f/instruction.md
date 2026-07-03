Wake up, you are on-call and just got a 3am page. Our custom C++ in-memory metric store has crashed, and the service is down. 

When the service restarts, it attempts to read its Write-Ahead Log (WAL) to restore its state, but the recovery process is segfaulting. This issue has been happening intermittently over the past few weeks, but usually, a restart fixes it. This time, it's consistently crashing on the latest WAL file, and we are losing critical production telemetry.

You have been given access to the recovery tool's source code and the corrupted WAL file. 
Directory: `/home/user/db_recovery/`
Files provided:
1. `recover.cpp` - The standalone C++ tool used to parse the WAL and dump the key-value state.
2. `system_state.wal` - The binary Write-Ahead Log file from the crashed production server.
3. `Makefile` - Use `make` to compile the `recover` executable.

Your tasks:
1. Analyze `recover.cpp` and `system_state.wal` to identify why the recovery process is crashing (Hint: Look for encoding, serialization, or memory handling bugs when reading from the binary log).
2. Fix the bug(s) in `recover.cpp`.
3. Recompile the tool and run it against `system_state.wal`.
4. Ensure the tool successfully parses all valid records in the WAL file without crashing.
5. The tool is designed to output recovered metrics to stdout in the format `KEY=VALUE`. Redirect this output to `/home/user/db_recovery/recovered_metrics.txt`.

Verification:
An automated system will check `/home/user/db_recovery/recovered_metrics.txt`. It must contain all the successfully recovered key-value pairs, one per line, exactly as output by the fixed C++ program. Do not modify the output formatting logic in the C++ file, only fix the crash/parsing issue.