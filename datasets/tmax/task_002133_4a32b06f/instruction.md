I am trying to fix a failing build in our analytics pipeline located at `/home/user/metrics_build`. We recently migrated some code and removed hardcoded secrets, but the CI pipeline is now broken due to two issues. I need you to debug and fix both.

**Issue 1: Missing API Secret**
Our build script requires an API token that used to be hardcoded in `publish.sh` but was removed in a recent commit. We haven't set up the new secret manager yet.
Please dive into the Git history of the `/home/user/metrics_build` repository, find the removed API token (it starts with `SEC-`), and write *just the token value* into `/home/user/recovered_token.txt`.

**Issue 2: Statistical Anomaly & Floating-Point Precision**
The script `/home/user/metrics_build/compute_mean.sh` calculates the statistical mean of the `value` column (the second column) in `measurements.csv` using `awk`. However, the downstream query validator rejects the result. 
I suspect `awk` is truncating or rounding the floating-point result to its default precision. You need to modify `/home/user/metrics_build/compute_mean.sh` so that it outputs the exact floating-point mean with exactly **9 decimal places** (e.g., `0.123456789`).

**Verification**
Once you have:
1. Created `/home/user/recovered_token.txt` with the correct token
2. Fixed `/home/user/metrics_build/compute_mean.sh`

Run the test suite by executing `bash /home/user/metrics_build/test_build.sh`.
If successful, the script will generate `/home/user/build_success.log`. 

Please leave the system in a state where `/home/user/build_success.log` is generated and contains the string `BUILD OK`.