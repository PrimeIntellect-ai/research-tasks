I am organizing my web security project files and trying to run our end-to-end test suite. This suite validates our request rate-limiting logic, checksum verifications, and dependency graph traversals.

We use `bats-core` (Bash Automated Testing System) to orchestrate these tests. I have placed the source code for `bats-core` version 1.8.2 in `/app/bats-core-1.8.2`. 

To speed up my workflow, I need to run these tests in parallel. However, when I try to run the tests using the `--jobs` flag (for example, `/app/bats-core-1.8.2/bin/bats --jobs 8 /home/user/web-sec-tests`), the test suite stubbornly runs sequentially and takes a very long time to complete. I suspect a team member accidentally introduced a bug or hardcoded a debug value in the vendored `bats-core` source code that breaks the parallel execution flag.

Your task:
1. Locate and fix the bug in the vendored `/app/bats-core-1.8.2` source code that is forcing sequential execution and ignoring the `--jobs` parameter.
2. Create a bash script at `/home/user/run_tests.sh` that executes the test suite located at `/home/user/web-sec-tests` using the fixed `bats` executable, specifying 8 parallel jobs.
3. Make sure `/home/user/run_tests.sh` is executable.

The automated verification system will run your `/home/user/run_tests.sh` script and measure its execution time. To pass, the tests must run successfully and complete significantly faster than the sequential baseline.