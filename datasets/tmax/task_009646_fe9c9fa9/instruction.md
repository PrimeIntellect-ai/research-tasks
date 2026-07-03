You are a developer troubleshooting a failing data processing pipeline. 

The repository is located at `/home/user/data_pipeline`. When you run `./build.sh` on the `main` branch, it fails. 

Your task is to:
1. Identify and fix an environment misconfiguration that is preventing `./build.sh` from even running its core logic. The script expects an environment variable pointing to the data file located at `/home/user/data.bin`. You must export this variable in your shell so the script can execute.
2. Once the script can execute, you will notice the build is still failing on the `main` branch. Use Git bisection to find the exact commit that introduced the regression. The last known good release is tagged as `v1.0`.
3. Analyze the bad commit and the binary data file (`/home/user/data.bin`) using standard bash utilities to understand why the build is failing. The bad commit introduced a faulty security check that rejects a specific IP address found in the data file.
4. Output your findings into two files:
   - Write the full, full-length Git commit hash of the first bad commit to `/home/user/bad_commit_hash.txt`.
   - Write the exact IPv4 address that is causing the build to fail to `/home/user/rejected_ip.txt`.

Ensure your final answers do not contain any extra text, spaces, or newlines, just the requested values. You may use any standard shell tools (e.g., `git`, `strings`, `grep`, `cat`) to complete this task.