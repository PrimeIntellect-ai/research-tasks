You are a FinOps analyst responsible for optimizing cloud storage costs. We have a simulated shared filesystem where different users store their files. The storage costs vary depending on the file type.

Your task is to create a C++ program and a bash wrapper script to calculate the total storage size and associated cost for each user.

Here are the requirements:
1. The simulated storage directory is located at `/home/user/cloud_storage`. Inside this directory, each subdirectory represents a user (e.g., `/home/user/cloud_storage/alice` means the user is `alice`).
2. Write a C++ program named `/home/user/cost_analyzer.cpp` that recursively traverses the `/home/user/cloud_storage` directory.
3. For each user, calculate the total size of their files (in bytes) and the total cost based on these rules:
   - `.log` files: Cost multiplier is 1 unit per byte.
   - `.db` files: Cost multiplier is 5 units per byte.
   - `.tmp` files: Cost multiplier is 0 units per byte (these are ignored for cost, but count towards total size).
   - Any other file extension (or files without extensions): Cost multiplier is 2 units per byte.
4. Write a bash script named `/home/user/run_analysis.sh` that:
   - Compiles the C++ program into an executable named `/home/user/cost_analyzer`. (Ensure robust error handling; if compilation fails, the script should exit with code 1).
   - Executes the compiled program.
   - The compiled C++ program must generate an output file at `/home/user/cost_report.csv`.
5. The `/home/user/cost_report.csv` must have the following exact format, sorted alphabetically by the username:
   ```csv
   Username,TotalBytes,TotalCost
   <user1>,<bytes1>,<cost1>
   <user2>,<bytes2>,<cost2>
   ```
6. Make sure your C++ code handles standard filesystem operations (you may use `<filesystem>`) and accurately sums up the sizes and costs. The bash script must be executable.

Do not write the final output manually. You must provide the C++ and bash scripts to generate it. Run your bash script to produce the final `cost_report.csv`.