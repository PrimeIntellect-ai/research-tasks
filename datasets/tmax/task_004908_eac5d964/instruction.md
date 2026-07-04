You are a localization engineer tasked with optimizing your company's translation pipeline. Over the years, multiple JSON localization files have accumulated duplicate source strings under different translation keys. Every duplicated source string costs extra money to translate. 

Your goal is to build a multi-stage deduplication pipeline using bash and a custom C++ hashing utility, and then schedule this pipeline.

Step 1: Write a C++ Deduplication Program
Write a C++ program at `/home/user/src/dedup.cpp`.
The program should read tab-separated values from standard input, where each line has the format: `<Key>\t<SourceString>`.
For each `<SourceString>`, calculate a custom polynomial rolling hash (to avoid collisions and practice algorithmic string hashing). 
The hash function must use:
- Base (p) = 31
- Modulus (m) = 1000000009 (10^9 + 9)
Formula: Hash = (c_0 * p^0 + c_1 * p^1 + ... + c_{n-1} * p^{n-1}) mod m, where c_i is the ASCII value of the i-th character of the string.
If multiple keys have the exact same `<SourceString>` (and thus the same hash), keep ONLY the entry with the lexicographically smallest `<Key>`.
Output the deduplicated results to standard output in the format: `<Hash>\t<Key>\t<SourceString>`, with one entry per line.

Step 2: Orchestrate the Pipeline
Write a bash script at `/home/user/pipeline.sh` that does the following:
1. Compiles `/home/user/src/dedup.cpp` into `/home/user/bin/dedup` (using `g++`, require C++17). Ensure `/home/user/bin` exists.
2. Reads all `.json` files in the directory `/home/user/locales/` (these are simple flat key-value pair JSON files).
3. Uses `jq` to extract all keys and values into a single stream of `<Key>\t<SourceString>` lines.
4. Pipes this stream into the compiled `dedup` C++ program.
5. Sorts the output of the C++ program numerically by the Hash column (the first column).
6. Saves the final sorted output to `/home/user/deduped_report.tsv`.

Step 3: Scheduling
Create a file at `/home/user/cron_schedule.txt` containing exactly one valid crontab line that schedules `/home/user/pipeline.sh` to run every day at exactly 2:00 AM system time. 

Make sure `/home/user/pipeline.sh` is executable. You may install `jq` and `g++` if they are not present.