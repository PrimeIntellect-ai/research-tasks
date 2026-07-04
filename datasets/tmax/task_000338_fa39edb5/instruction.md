We are migrating an old CI/CD build infrastructure where services frequently fail to reach each other due to a legacy Docker Compose network misconfiguration. In our current setup, build jobs are isolated using a proprietary, undocumented binary that generates network routing rules and disk quota allocations.

The binary is located at `/app/legacy_net_quota.bin`. It takes a single command-line argument representing a CI/CD job definition string and prints the necessary network and storage configuration to standard output. Since the tool is unmaintained and we have lost the source code, we cannot adjust it to fix the network misconfigurations. 

Your task is to:
1. Reverse-engineer the behavior of the black-box binary `/app/legacy_net_quota.bin`. You can execute it with different inputs to observe its output, or use tools to inspect it.
2. Write a Python script at `/home/user/quota_router.py` that behaves **exactly** like the binary. Your script must accept a single command-line argument (the job definition string) and print the exact same output as the binary for any given input, including error handling.
3. To prepare for the new configuration rollout, create a simple shell script at `/home/user/setup_workers.sh` that, when executed, creates a mock CI/CD pipeline directory structure. It should create directories `/home/user/cicd/worker_1` through `/home/user/cicd/worker_5`.

Your Python script will be rigorously tested against the original binary with hundreds of random inputs to ensure bit-exact equivalence. Do not add any extra print statements or debugging output in your final Python script.