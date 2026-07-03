You are an infrastructure engineer automating the provisioning and monitoring of a cluster of QEMU virtual machines. We recently had an issue where a systemd service responsible for monitoring failed to start because of a missing `After=` dependency on the QEMU provisioning service, causing a massive backlog of unparsed telemetry data. 

To catch up, we need a high-performance log analyzer to process the backlogged QEMU telemetry data.

We have a proprietary, stripped binary located at `/app/qemu_telem_gen`. This binary simulates our QEMU hypervisor's raw telemetry output.
1. First, run this binary and redirect its standard output to create a log file: `/home/user/telemetry.log`. (Note: It generates a large amount of data).
   The output format of the log is exactly: `[TIMESTAMP] VM_ID CPU_USAGE MEM_USAGE`
   Example: `[1690000000] vm-14 45.2 1024.0`

2. Write a highly optimized C++ program located at `/home/user/repo/analyzer.cpp` that calculates the average CPU usage for a specific VM.
   - The program must take exactly two command-line arguments: the path to the log file, and the `VM_ID` (e.g., `vm-42`).
   - It must output *only* the average CPU usage as a floating-point number (e.g., `45.201`) to standard output.
   - The program must be performant. We have an automated metric threshold in place: your C++ program must execute in under 0.15 seconds on the generated log file. Use efficient I/O operations (e.g., `std::ios_base::sync_with_stdio(false);`, memory mapping, or fast string parsing).

3. The directory `/home/user/repo` is a git repository. Once your C++ code is complete, stage and commit `analyzer.cpp` to the repository. The repository has been pre-configured with a strict `pre-commit` hook that will compile your code and run a basic correctness check using a subset of the data. Your commit must succeed.

Complete the task by ensuring your commit is accepted by the pre-commit hook and that your code is highly optimized.