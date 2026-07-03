You are tasked with debugging a regression in a data processing pipeline located in `/home/user/pipeline_repo`. 

The repository contains ~200 commits. At `v1.0` (the first commit), the pipeline worked perfectly. Currently, at `HEAD`, the pipeline script (`process.sh`) fails.

The pipeline processes a temperature reading from an SQLite database (`sensor.db`) and passes it to a compiled validation binary (`bin/validator`).

However, you are facing multiple issues:
1. **Corrupted Database:** The local `sensor.db` file in the workspace has been corrupted (its header was overwritten). You must recover the temperature integer from it or fix it, and create a working database named `sensor_recovered.db` containing the same `readings` table and `temp` value.
2. **Undocumented Binary:** The `bin/validator` binary has no source code. You will need to reverse-engineer or inspect it to understand the constraints it places on the temperature value it receives.
3. **Regression:** Somewhere in the git history, the temperature conversion formula in `process.sh` was altered, causing the validation to fail.

**Your objectives:**
1. Recover the database into `/home/user/pipeline_repo/sensor_recovered.db` so that `sqlite3 sensor_recovered.db "SELECT temp FROM readings;"` successfully returns the reading.
2. Use `git bisect` (writing an automated bash script to test commits is highly recommended) to find the exact commit hash that introduced the formula bug. The known good tag is `v1.0`.
3. Save the full, 40-character Git SHA of the first bad commit into `/home/user/bad_commit.txt`.
4. Return to the `HEAD` of the `main` branch and fix the formula in `process.sh` so that running `./process.sh sensor_recovered.db` completes successfully with a `0` exit code.

Ensure your fix is applied directly to `/home/user/pipeline_repo/process.sh` in the working directory.