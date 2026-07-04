You are a developer debugging a failing build for a C++ simulation engine. 

The repository is located at `/home/user/sim_engine`. The `make test` target is currently failing on the `main` branch due to a recently introduced numerical instability. The known good state was tagged as `v1.0`.

To complicate matters, the test suite requires a configuration file at `/home/user/sim_engine/config.txt` containing a specific calibration coefficient. This file was accidentally deleted from the working directory and is in `.gitignore`. However, the coefficient was recently broadcasted over the local network to our configuration service. A packet capture of this traffic is available at `/home/user/capture.pcap`.

Your tasks are:
1. Analyze `/home/user/capture.pcap` to find the missing calibration coefficient. Look for a cleartext payload containing `COEFF=<value>`.
2. Recreate `/home/user/sim_engine/config.txt` and populate it with exactly that coefficient (just the number).
3. Use `git bisect` (or manual checkout) between `v1.0` (good) and `main` (bad) to identify the exact commit that introduced the numerical instability causing the tests to fail.
4. Identify the C++ source file that was modified in that bad commit to introduce the bug.

Output your final findings to a file named `/home/user/solution.txt` in the following exact format:
```
COEFFICIENT: <the_extracted_number>
BAD_COMMIT: <full_40_character_git_hash>
BUG_FILE: <name_of_the_cpp_file_modified_in_the_bad_commit>
```

Ensure all paths are strictly followed and the solution file is formatted exactly as requested.