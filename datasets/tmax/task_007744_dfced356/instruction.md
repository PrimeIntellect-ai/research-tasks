You are a performance engineer tasked with debugging and profiling a multi-stage data processing pipeline. The pipeline currently fails to build, crashes on specific edge-case data due to floating-point precision loss, and has asynchronous logs that make it hard to track failures.

Your workspace is located at `/home/user/pipeline/`.

The pipeline consists of:
1. A Cython-based aggregator in `fast_agg.pyx` and `setup.py`.
2. A Python processing script `processor.py`.
3. A set of simulated service logs in `/home/user/pipeline/logs/`.

Your objectives:

**Phase 1: Build Failure Diagnosis**
The Cython aggregator is failing to compile. The build script `setup.py` is missing a critical configuration to locate C-headers for a required numerical library. 
Diagnose and fix `setup.py`, then build the extension in-place by running:
`python3 setup.py build_ext --inplace`

**Phase 2: Log Timeline Reconstruction**
The pipeline uses three services (`generator`, `processor`, `aggregator`), which write logs to `/home/user/pipeline/logs/` using completely different timestamp formats:
- `generator.log` uses ISO 8601 (`YYYY-MM-DDTHH:MM:SSZ`).
- `processor.log` uses Unix epoch timestamps.
- `aggregator.log` uses `YYYY/MM/DD HH:MM:SS`.

The aggregator crashed, but the log only says "CRITICAL: ZeroDivisionError in fast_agg". You need to reconstruct the chronological timeline of all three logs to find out which `sensor_id` was being processed exactly when the crash occurred. 
Identify the faulty sensor ID and write *only* the exact sensor ID string (e.g., `SEN-1234`) to `/home/user/pipeline/faulty_sensor.txt`.

**Phase 3: Floating-Point Precision Repair**
The root cause of the crash is in `processor.py`. The script calculates the variance of sensor readings using the naive single-pass formula (`E[X^2] - E[X]^2`). Because the sensor values are very large base numbers with tiny micro-fluctuations, catastrophic cancellation (floating-point precision loss) occurs. This results in a calculated variance of exactly `0.0` or a negative number, causing a downstream divide-by-zero error in the aggregator.

Modify `processor.py` to fix the precision loss. You may use a stable two-pass variance algorithm, Welford's method, or standard library functions that handle precision correctly. Do not change the input/output signatures of the functions.

**Phase 4: Run the Pipeline**
Once the build is fixed and the precision issue is resolved, run the pipeline wrapper:
`python3 run_pipeline.py`

This will read the raw data, process it, aggregate it using your compiled Cython module, and output the final results to `/home/user/pipeline/output/final_metrics.json`.

**Verification Requirements:**
1. `/home/user/pipeline/setup.py` must be fixed and the `.so` file built successfully.
2. `/home/user/pipeline/faulty_sensor.txt` must contain the correct sensor ID responsible for the crash.
3. `/home/user/pipeline/output/final_metrics.json` must be successfully generated without any exceptions.