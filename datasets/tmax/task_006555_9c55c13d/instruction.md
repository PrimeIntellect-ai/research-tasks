You are an on-call engineer who just received a 3 AM page. Our custom in-memory database, MiniKV, has crashed. 

We have a Write-Ahead Log (WAL) located at `/home/user/data/wal.log`. 
The automated C recovery tool at `/home/user/recover.c` is supposed to replay this log, reconstruct the latest database state, and dump it to `/home/user/recovered.txt`. 

However, the recovery tool is currently failing. It crashes with an assertion failure and produces corrupted output when it doesn't crash. 
Looking at the recent commits, two things were introduced:
1. A multi-threaded worker pool to process WAL chunks faster.
2. New log formats that include spaces in the keys and values.

Your task:
1. Diagnose and fix the parsing bug in `/home/user/recover.c` that causes it to fail on keys or values containing spaces.
2. Identify and fix the race condition in the C code that causes the concurrent index updates to step on each other.
3. Compile the fixed program: `gcc -pthread /home/user/recover.c -o /home/user/recover`
4. Run the recovery tool: `/home/user/recover`

The tool must output the final database state to `/home/user/recovered.txt`.
The format of `/home/user/recovered.txt` must be exactly one key-value pair per line, sorted alphabetically by key, like so:
```
key one=value one
key two=value two
```
If a key is updated multiple times in the WAL, the final output must only contain the latest value.

Fix the C code, generate the recovered file, and ensure it is perfectly correct so we can bring the service back online.