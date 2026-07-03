You are a performance engineer tasked with deploying and profiling a multi-service scientific computing pipeline that performs distributed matrix decompositions.

The system consists of three services located in `/app/`:
1. **Simulation Daemon** (`/app/sim/sim.c`): A C-based scientific engine that performs LU and QR decompositions. It must be compiled from source.
2. **Telemetry Logger** (`/app/logger/logger.py`): A Python service that aggregates trace events.
3. **API Gateway** (`/app/gateway/gateway.sh`): A simple Bash-based router.

### Part 1: Service Configuration & Composition
You must compile and start the pipeline.
1. Compile `/app/sim/sim.c` into an executable at `/app/sim/sim_daemon`. You will need to link the LAPACK and BLAS libraries (already installed on the system).
2. Start the services so they form an end-to-end pipeline:
   - The Telemetry Logger must listen on port `9002`.
   - The Simulation Daemon must listen on port `9001` and be configured to send traces to the logger at `127.0.0.1:9002` (via the `TELEMETRY_URL` environment variable).
   - The API Gateway must listen on port `9000` and route requests to `127.0.0.1:9001` (via the `BACKEND_URL` environment variable).

### Part 2: Trace Analysis Algorithm (Bash/Awk)
The telemetry logger writes traces representing the execution graph of the matrix decomposition tasks. 
You must write a strict Bash script at `/home/user/trace_analyzer.sh` that takes a trace file as its first and only argument and outputs performance metrics.

The input trace file contains space-separated lines:
`[Source_Node_ID] [Destination_Node_ID] [Latency_in_ms]`
(The graph is guaranteed to be a Directed Acyclic Graph).

Your script must compute and print exactly two lines to standard output:
**Line 1: Critical Path**
Find the path through the DAG with the maximum total latency. Output the nodes in order, separated by `->`, followed by the total latency.
*Format:* `Path: A->B->C, Total: 150` (If multiple paths have the exact same maximum latency, break ties by selecting the one that comes first lexicographically by full path string).

**Line 2: Density Estimation (5-Bin Histogram)**
Calculate a simple 5-bin histogram of all individual edge latencies to estimate the distribution. 
- Find the global minimum (`MIN`) and maximum (`MAX`) latency.
- Calculate the bin width: `W = (MAX - MIN) / 5`.
- The 5 bins are `[MIN, MIN+W)`, `[MIN+W, MIN+2W)`, `[MIN+2W, MIN+3W)`, `[MIN+3W, MIN+4W)`, and `[MIN+4W, MAX]`. (Note the last bin is inclusive of MAX).
- Output the counts for each bin.
*Format:* `Density: B1:4, B2:1, B3:0, B4:2, B5:7`

A compiled oracle binary exists at `/app/oracle_analyzer`. Your script must be bit-exact equivalent in output to this oracle for any valid trace file.

Ensure `/home/user/trace_analyzer.sh` is executable. You may use any standard Linux text processing tools (awk, sed, grep, bc).