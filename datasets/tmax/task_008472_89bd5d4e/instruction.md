You are tasked with building a C++ data processing tool to recover a configuration deployment plan from a noisy ETL log. 

An ETL job responsible for tracking system configuration changes crashed and retried multiple times, resulting in a log file containing duplicate records. Furthermore, services have inter-dependencies, and we need to reconstruct the final configuration state and output a deployment plan in the correct order.

The log file is located at `/home/user/data/config_events.log`. 

Each line in the log follows this exact format:
`[YYYY-MM-DD HH:MM:SS] SERVICE=<service_name> DEPENDS_ON=<comma_separated_services> CONFIG=<key>:<value>`
*(Note: If a service has no dependencies, DEPENDS_ON will be empty, e.g., `DEPENDS_ON= `)*

Your objective is to write a C++17 program (`/home/user/config_manager.cpp`) that does the following:
1. **Parallel Regex Parsing:** Reads the log file. You must use C++ `std::regex` to parse the lines and utilize multi-threading (e.g., `std::thread`, `std::async`, or OpenMP) to parse the file in parallel.
2. **Deduplication & State Merging:** 
   - Discard exact duplicate lines.
   - If multiple lines update the same `CONFIG` key for the same `SERVICE`, the one with the chronologically latest timestamp wins.
   - A service's final dependencies are the union of all its valid `DEPENDS_ON` declarations in the log.
3. **DAG Orchestration:** Construct a Directed Acyclic Graph (DAG) of the service dependencies. `DEPENDS_ON=DB` means the service depends on `DB`, so `DB` must be deployed *before* the service.
4. **Output:** Perform a topological sort on the DAG. Write the final deployment plan to `/home/user/deployment_plan.txt`.

**Output Format:**
For each service in the topologically sorted order, write exactly one line to `/home/user/deployment_plan.txt` in this format:
`SERVICE:<service_name> CONFIG:<key1>=<val1>,<key2>=<val2>`
- If there are multiple configuration keys for a service, sort the `key=value` pairs alphabetically by the key.
- If multiple valid topological sorts are possible, break ties by sorting the service names alphabetically.

Compile your code using `g++ -O3 -std=c++17 -pthread /home/user/config_manager.cpp -o /home/user/config_manager`.
Run your tool to generate `/home/user/deployment_plan.txt`.