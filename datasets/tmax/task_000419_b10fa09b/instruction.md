You have recently inherited an unfamiliar C++ codebase for a simple multi-threaded Key-Value store. The previous developer left abruptly, and the system is currently in a broken state. It occasionally crashes under load, leaving behind a partially corrupted Write-Ahead Log (WAL) file. 

Your objectives are to fix the codebase, recover the data, and ensure the bug is caught.

Here is what you need to do:

1. **Fix the Race Condition**: The source code is located in `/home/user/kv_store/`. When multiple threads write to the store concurrently, the application sometimes crashes with a segmentation fault. Analyze the codebase, identify the concurrency bug (race condition) in `kv_store.cpp`, and fix it. You are allowed to use standard C++ synchronization primitives.

2. **Recover the Database**: There is a corrupted WAL file located at `/home/user/kv_store/data.wal`. The WAL uses a simple custom binary format for each entry:
   - 1 byte: Start magic marker (`0xAA`)
   - 1 byte: Key length (unsigned integer)
   - N bytes: Key string (ASCII)
   - 1 byte: Value length (unsigned integer)
   - M bytes: Value string (ASCII)
   - 1 byte: End magic marker (`0xBB`)
   Because of the crashes, the file might contain partial or corrupted entries at the end or interspersed. You must write a script or program (in C++ or Python) to parse this file, extract all completely valid entries (those starting with `0xAA` and ending with `0xBB` with correct lengths), and output them to `/home/user/recovered_data.txt`. The output format must be exactly one `key=value` pair per line, sorted alphabetically by key.

3. **Regression Test**: Create a minimal reproducible example/regression test to prove the system no longer crashes. Write a bash script at `/home/user/test_race.sh` that compiles the C++ code and runs an executable named `stress_test` (which you should create or compile from the existing files) to demonstrate that concurrent inserts no longer cause a crash. The script should exit with code 0 if successful.

Make sure your fixes are applied directly to the files in `/home/user/kv_store/`.