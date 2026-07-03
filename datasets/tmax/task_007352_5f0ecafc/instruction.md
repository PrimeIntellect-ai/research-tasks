You have just inherited a legacy sensor data processing pipeline written primarily in C, with some Python components. The previous developer left abruptly, and the system is currently failing tests in production. 

The project is located in `/home/user/legacy_project`.

There are three main issues you need to debug and resolve:

1. **Incorrect Calculations (Formula Implementation Correction)**
   The core C program `processor` reads coordinates and calculates the Euclidean distance between successive points. However, the downstream system is reporting completely invalid distance values (often negative or wildly incorrect). Fix the mathematical error in `/home/user/legacy_project/math_utils.c`.

2. **Severe Performance Bottleneck (System Call Tracing)**
   The `processor` is incredibly slow. It processes 100 records in about 5 seconds, which is unacceptable. Use `strace` or similar tools to trace the system calls and identify the bottleneck in `/home/user/legacy_project/processor.c`. You are expected to remove or fix the offending system call(s) causing the extreme latency. 

3. **Log Timeline Reconstruction**
   The system runs three distinct components:
   - A generator script (`gen.log`)
   - The C processor (`proc.log`)
   - An aggregator script (`agg.log`)
   Because they were written at different times, they all use different timestamp formats. Write a script at `/home/user/reconstruct_logs.sh` that reads `/home/user/legacy_project/logs/gen.log`, `/home/user/legacy_project/logs/proc.log`, and `/home/user/legacy_project/logs/agg.log`, normalizes their timestamps to Unix epoch time (in seconds, with decimal milliseconds if applicable), and merges them into a single chronologically sorted log file at `/home/user/timeline.log`. Each line in the merged log should be formatted exactly as: `[<EPOCH_TIME>] <COMPONENT> : <ORIGINAL_MESSAGE_EXCLUDING_TIMESTAMP>` (where COMPONENT is GEN, PROC, or AGG).

4. **Minimal Reproducible Example**
   Create a standalone C file at `/home/user/mre_bottleneck.c` that isolates and minimally reproduces the exact system call performance bottleneck you found in step 2. This file should be independently compilable and demonstrate the flawed logic.

**Verification Requirements:**
- You must successfully compile the fixed processor: `cd /home/user/legacy_project && gcc -o processor processor.c math_utils.c -lm`
- The fixed `processor` must process the provided `test_data.txt` in under 0.1 seconds.
- The `calculate_distance` function must correctly compute Euclidean distance.
- `reconstruct_logs.sh` must successfully generate `/home/user/timeline.log` when executed.