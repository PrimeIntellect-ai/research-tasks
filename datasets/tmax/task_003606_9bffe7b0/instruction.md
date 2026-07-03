You have just inherited a legacy bash-based data processing pipeline located in `/home/user/sensor_pipeline`. The previous developer left abruptly, and the pipeline is currently broken. Your manager has asked you to perform a forensic debugging session to fix the system.

The pipeline processes floating-point sensor readings from multiple files. You run it using `./run_pipeline.sh`, but it suffers from several issues:
1. **Intermittent failures & Race Conditions**: The `run_pipeline.sh` script spawns multiple background jobs (`process_chunk.sh`) that write to a shared output file concurrently, causing garbled data and missing lines.
2. **Precision Loss & Convergence Failure**: The final script `calculate_convergence.sh` reads the aggregated data and applies an iterative smoothing algorithm using `bc`. However, due to improper precision settings (scale), the loop loses precision and fails to converge to a stable value, ultimately returning an error.

Your tasks:
1. Diagnose and fix the race condition in `/home/user/sensor_pipeline/run_pipeline.sh` (or `process_chunk.sh`) so that all data chunks are safely and completely aggregated into `/home/user/sensor_pipeline/out/aggregated.dat` without missing or interleaved lines.
2. Debug and fix `/home/user/sensor_pipeline/calculate_convergence.sh` to prevent precision loss. You must modify the `bc` commands to use a `scale` of at least 6 so the algorithm correctly converges.
3. Once the pipeline runs reliably and successfully converges, write the final, correctly converged numerical value to `/home/user/convergence_result.txt`.

Constraints:
- You must use bash/standard Linux utilities. 
- Do not change the core mathematical formula in `calculate_convergence.sh`, only fix the precision/scale and race conditions.