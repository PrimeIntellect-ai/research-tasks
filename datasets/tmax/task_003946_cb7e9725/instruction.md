You are an engineer investigating a persistent memory leak and intermittent crashes in our long-running telemetry aggregation service. The service parses incoming JSON-formatted system metrics, performs statistical anomaly detection, and outputs a compacted binary summary. 

We have a vendored third-party JSON library at `/app/cJSON-1.7.15` and our main service code at `/app/telemetry_processor.c`. Recently, our telemetry volume increased, and we've noticed the service leaking memory specifically when processing batches of statistically anomalous inputs containing specific keys under heavy concurrent load.

Your task is to:
1. Diagnose and fix the memory leak and race condition. The issue involves a conflict between our concurrent parsing logic in `telemetry_processor.c` and a perturbation in the vendored `cJSON` library where error paths for deeply nested anomalous items fail to release allocations.
2. Resolve a dependency conflict in the provided `Makefile` which currently dynamically links against an older, system-wide version of the library instead of the vendored source. 
3. After fixing the source and Makefile, compile your fixed executable to `/home/user/fixed_processor`. 

To ensure your logic remains functionally correct after the fix, your compiled executable must be perfectly bit-for-bit equivalent in its standard output to our internal reference binary (`/app/bin/oracle_processor`) when fed identical input files via standard input. 

Both the oracle and your processor accept input from stdin and output the packed binary summary to stdout. Ensure your final binary is compiled with no memory leaks (we will verify using Valgrind/ASAN) and handles anomalous payloads correctly.