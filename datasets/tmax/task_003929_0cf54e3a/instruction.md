You are an operations engineer triaging an incident with our new sensor data pipeline. We are migrating from a proprietary legacy tool to an in-house C++ implementation.

You have been provided with the proprietary legacy binary at `/app/legacy_oracle`. This binary takes a list of floating-point numbers from standard input and prints the transformed data to standard output. 
However, `/app/legacy_oracle` requires a license key to run, provided via the `ORACLE_KEY` environment variable. The key is embedded inside the stripped binary and is a 16-character string starting with `KEY_`. You will need to extract it to use the oracle.

Our new in-house C++ implementation is located in the Git repository at `/home/user/sensor_pipeline`. Currently, the integration pipeline is failing due to two major regressions:
1. **Infinite Loop / Hang**: The program hangs indefinitely on certain inputs (such as the provided `/home/user/sample_input.txt`). You must debug and fix the loop termination or recursion logic in the C++ code.
2. **Precision Loss**: Even when the hang is bypassed, the new code produces outputs that slightly diverge from the legacy oracle. You should use `git bisect` (or analyze the diffs) to identify the commit that introduced this precision loss, and patch the current code to restore high-precision arithmetic.

Your tasks:
1. Extract the `ORACLE_KEY` from `/app/legacy_oracle` and set it in your environment.
2. Fix the infinite loop bug in `/home/user/sensor_pipeline`.
3. Fix the precision loss bug in `/home/user/sensor_pipeline`.
4. Build the final fixed executable and place it EXACTLY at `/home/user/sensor_pipeline/pipeline_fixed`.

Your program `/home/user/sensor_pipeline/pipeline_fixed` must read space-separated numbers from standard input and print the processed numbers to standard output, matching the behavior of `/app/legacy_oracle`.

The automated verifier will generate a hidden dataset of 1000 sensor readings, pass them to both your compiled `/home/user/sensor_pipeline/pipeline_fixed` and `/app/legacy_oracle`, and compute the Mean Squared Error (MSE) between the outputs. To succeed, your implementation must achieve an MSE of less than 1e-8.