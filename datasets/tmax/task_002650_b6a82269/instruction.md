You are a DevOps engineer investigating an issue with our new C++ log ingestion pipeline. 

We process high-precision server metrics using a vendored copy of the `nlohmann/json` library located at `/app/json`. The ingestion script is located at `/workspace/process_metrics.cpp`, and it processes a log file at `/workspace/logs.json`. 

Currently, the system is completely broken:
1. **Build Failure**: `/workspace/process_metrics.cpp` fails to compile against the vendored `/app/json` headers due to a compilation error inside the JSON library.
2. **Infinite Hang**: If you bypass the build failure, the program hangs indefinitely when parsing `logs.json`. 
3. **Precision Loss**: If you manage to get it to parse, the resulting latency standard deviation printed to `/workspace/output.txt` is wrong. It exhibits severe precision loss, causing our anomaly detection alerts to misfire.

Your task:
1. Diagnose and fix the build failure in the vendored `/app/json` library.
2. Identify and fix the infinite loop/recursion bug within the JSON library's parsing or lexing logic.
3. Identify and fix the precision loss bug in the library so that it correctly handles high-precision floating-point numbers without truncating them prematurely.
4. Compile `/workspace/process_metrics.cpp` using `g++ -std=c++11 -I/app/json/include /workspace/process_metrics.cpp -o /workspace/process_metrics`.
5. Run `/workspace/process_metrics` so that it successfully generates `/workspace/output.txt`.

The automated verifier will check the numerical value printed in `/workspace/output.txt` against the mathematically correct standard deviation of the high-precision logs.