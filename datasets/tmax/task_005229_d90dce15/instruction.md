You are tasked with debugging a regression in a data processing pipeline. 

A repository located at `/home/user/repo` contains a Bash script `simulate.sh` that reads a base64-encoded configuration file (`config.b64`), decodes it into a JSON object, and performs a series of calculations to reach a convergence value. 

Historically, this script worked perfectly. In the `v1.0` tag, the algorithm successfully converges. However, on the `main` branch (the current `HEAD`), the script fails to converge due to a serialization/encoding bug introduced somewhere in the last 200 commits. The bad commit accidentally corrupted the decoding pipeline while trying to clean up carriage returns from the file.

Your objectives:
1. Perform a bisection on the repository to find the exact commit that introduced the bug. The last known good state is tagged as `v1.0`.
2. Write the full 40-character commit hash of the single bad commit that introduced the regression into `/home/user/bad_commit.txt`.
3. Inspect the bug and the base64 payload. Determine the intended `rate` value that the algorithm is supposed to use for its calculation. Write this exact numeric value to `/home/user/expected_rate.txt`.

Ensure your final answers are saved exactly to the requested file paths.