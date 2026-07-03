You are an integration developer tasked with orchestrating an end-to-end API testing pipeline for a microservice architecture. You need to write a Bash script that resolves service dependencies, captures memory profiling metrics for a specific leaky service, and logs the results for verification.

Your task is to create and run a Bash script at `/home/user/orchestrate.sh` that performs the following steps:

1. **Dependency Resolution (Graph Traversal):**
   Read the dependency graph from `/home/user/api_topology.txt`. The file defines which services depend on which, using the format: `ServiceName -> DependencyName`. If a service has no dependencies, it will be written as `ServiceName -> ` (with a trailing space). 
   Your script must calculate a valid topological execution order (start services with no dependencies first, up to the services that depend on everything else).
   Write the exact startup order to `/home/user/startup_order.log`, with one service name per line.

2. **Memory Debugging:**
   One of the services, `AuthService`, is a compiled C binary located at `/home/user/bin/auth_service` and has a suspected memory leak. 
   As part of your orchestration script, execute `/home/user/bin/auth_service` using `valgrind` to profile its memory usage.
   Save the valgrind output by using the `--log-file=/home/user/valgrind_auth.log` flag.
   Make sure you run the binary with `valgrind --leak-check=full`. The binary will exit automatically after completing its mock execution.

3. **Metrics Extraction:**
   After the valgrind run completes, your script must parse `/home/user/valgrind_auth.log` to find the exact number of bytes reported as "definitely lost".
   Extract *only the integer number of bytes* (e.g., if it says `1,024 bytes in 1 blocks`, extract `1024` without commas).
   Write this single integer to `/home/user/leak_report.txt`.

Ensure your script is executable (`chmod +x /home/user/orchestrate.sh`) and run it so the log files are generated.