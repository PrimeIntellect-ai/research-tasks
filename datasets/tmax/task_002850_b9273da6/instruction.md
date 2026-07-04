You are an AI assistant helping a capacity planner set up a mock resource monitoring and health-check pipeline. 

Your task is to implement a simple C++ monitoring daemon, set up its directory structure, and create a shell script pipeline to parse its alerts.

Please perform the following steps:

1. **Directory Structure & Linking**:
   Create the following directories:
   - `/home/user/capacity_planner/src`
   - `/home/user/capacity_planner/bin`
   - `/home/user/capacity_planner/logs`
   - `/home/user/capacity_planner/active`

2. **C++ Monitor Mock**:
   In `/home/user/capacity_planner/src`, write a C++ program named `monitor_mock.cpp`. 
   The program must simply output the following mock CSV data (representing `ServiceName,CPU_Usage_Percent,Memory_Usage_Percent`) to standard output and then exit cleanly:
   ```
   frontend_web,45,60
   backend_api,85,70
   database_main,90,95
   cache_node,10,15
   ml_worker,20,88
   ```
   Compile this C++ program using `g++` and output the binary to `/home/user/capacity_planner/bin/monitor`.

3. **Symlinking**:
   Create a symbolic link at `/home/user/capacity_planner/active/current_monitor` that points to the compiled binary `/home/user/capacity_planner/bin/monitor`.

4. **Health Check Pipeline Script**:
   Create a bash script at `/home/user/capacity_planner/health_check.sh`. 
   The script must:
   - Have executable permissions (`chmod +x`).
   - Execute the symlinked binary: `/home/user/capacity_planner/active/current_monitor`.
   - Use text processing tools (`awk`, `sed`, or `grep`) to filter the output for services where **EITHER** CPU Usage is >= 80 **OR** Memory Usage is >= 80.
   - Extract **only** the ServiceName (the first column) of those violating thresholds.
   - Redirect these extracted service names to `/home/user/capacity_planner/logs/critical_alerts.log`.

5. **Execution**:
   Run the `/home/user/capacity_planner/health_check.sh` script once so the log file is generated.