You are a performance engineer tasked with fixing a critical data pipeline.

Our pipeline processes text records by serializing them and sending them to a high-speed proprietary C++ engine, which is provided as a stripped binary at `/app/record_engine`. 

Recently, we deployed an update to the Python wrapper (`/home/user/wrapper_repo`), but we noticed two major issues:
1. The throughput has dropped precipitously.
2. The pipeline intermittently crashes with a core dump from the engine when processing certain datasets. 

Your objectives are:
1. **Find the Regression:** Use the Git repository in `/home/user/wrapper_repo` to identify the commit that introduced the performance regression and intermittent crashes. 
2. **Troubleshoot the Intermittent Crash:** Analyze the core dumps or failing payloads. The crash happens due to a bug in how the Python wrapper serializes non-ASCII characters before sending them to the engine. Fix the encoding/serialization logic in `driver.py`.
3. **Recover the Performance Secret:** While digging through the Git history, look for a removed configuration, secret environment variable, or fast-path flag that was accidentally deleted or masked. You must restore this fast-path capability.
4. **Optimize:** Fix `driver.py` so it properly handles all text inputs without crashing the binary and runs efficiently.

**Verification Requirements:**
- You must save your finalized, optimized Python script to `/home/user/wrapper_repo/driver_fixed.py`.
- Your script must take a path to a JSON dataset as its first argument and process it using `/app/record_engine`.
- Output: The script must write a file named `/home/user/metrics.log` containing exactly one line with the total execution time in seconds (e.g., `0.85`).
- The automated test will verify that your script successfully processes the test dataset `/app/eval_data.json` without crashing, and that the total execution time is under 1.5 seconds.