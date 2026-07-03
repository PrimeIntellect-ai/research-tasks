You are acting as a mobile build engineer maintaining our CI/CD pipelines. We recently migrated our custom pipeline runner to a concurrent architecture, but our recent Android/iOS C++ builds are failing during the CMake linking phase. 

Because the build system runner processes tasks concurrently, the logs are split across multiple worker log files and are completely interleaved in time. 

Your task is to write a Python script at `/home/user/parse_build.py` that processes these unstructured concurrent logs, sorts them, and identifies the exact missing shared library causing the build failure.

Here are the requirements:
1. Read all log files located in `/home/user/build_logs/`. The directory contains several files named `worker_<id>.log`.
2. Each line in these log files follows this format:
   `[YYYY-MM-DDTHH:MM:SS.mmmZ] [Worker-<ID>] <Message>`
3. Your Python script must read all these files and merge them into a single, chronologically sorted log file at `/home/user/merged_build.log`. The output format must be identical to the input format.
4. Scan the merged log to find the CMake linker error. The linker error will look like `ld: library not found for -l<LibraryName>`.
5. Extract the exact missing library name (without the `-l` prefix) and write it to `/home/user/missing_lib.txt`.

Example: If the error is `ld: library not found for -lMobileCoreSync`, you should write `MobileCoreSync` to `/home/user/missing_lib.txt`.

You may use standard shell commands to inspect the files, but the core processing and extraction must be done by your Python script `/home/user/parse_build.py`. When you have written the script, execute it so the output files are generated.