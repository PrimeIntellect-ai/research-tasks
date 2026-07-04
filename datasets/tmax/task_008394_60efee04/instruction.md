You are a Site Reliability Engineer (SRE) investigating an uptime monitoring issue. The system reconstructs transaction timelines across three distributed services (ServiceA, ServiceB, and ServiceC) to track latency and ensure proper event ordering. 

We have an aggregator written in C++ located at `/home/user/aggregator.cpp`. It reads three log files:
- `/home/user/logs/service_a.log`
- `/home/user/logs/service_b.log`
- `/home/user/logs/service_c.log`

Currently, when you compile and run `aggregator.cpp`, it crashes with an assertion failure (`assert(current_time > last_time)`). The assertion acts as an intermediate validation step to ensure strict chronological ordering of events within a transaction timeline.

Your tasks are:
1. Diagnose the root cause of the crash in `/home/user/aggregator.cpp`. Look closely at how timestamps are being tracked and parsed. 
2. Fix the bug in `/home/user/aggregator.cpp` so that no precision loss occurs and the assertion passes.
3. Compile the fixed C++ code (using `g++ -std=c++17 /home/user/aggregator.cpp -o /home/user/aggregator`).
4. Run the compiled executable. It is programmed to automatically output a file to `/home/user/fixed_timeline.csv` once the assertions pass.

The final system state should have the correctly formatted `/home/user/fixed_timeline.csv` file present. Do not change the output file format or the assertion logic itself; only fix the underlying data type issue causing the validation to fail.