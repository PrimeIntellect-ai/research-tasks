**Pager Alert - 3:15 AM**
*Severity: SEV-2*
*Component: Sensor Telemetry Pipeline*
*Issue: Pipeline crashed, state corrupted, precision lost.*

You are the on-call engineer. Our background telemetry pipeline processes a Write-Ahead Log (WAL) of sensor readings to maintain an Exponential Moving Average (EMA) of sensor values. 

The pipeline script (`/home/user/telemetry/process_wal.sh`) recently crashed midway through processing `/home/user/telemetry/sensor.wal`. Furthermore, QA reported yesterday that the updated values in `/home/user/telemetry/current_state.csv` were losing precision, resulting in cascading inaccuracies.

Your task is to fix the pipeline, recover the state, and produce the correct final output.

**System Details & Constraints:**
1. **Workspace:** All files are located in `/home/user/telemetry/`.
2. **The Script:** `process_wal.sh` reads `sensor.wal` and applies the formula: `NEW_EMA = (OLD_EMA * 0.9) + (NEW_VALUE * 0.1)`. 
3. **The Bugs:** 
   - **Floating-point precision:** The bash script relies on `bc` but is heavily truncating the values (defaulting to 0 decimal places instead of the required 4). Ensure all EMA calculations retain exactly 4 decimal places of precision (e.g., `12.3456`).
   - **WAL Corruption:** A power blip caused a malformed/corrupted entry in `sensor.wal`. If the script encounters a line where the sensor value is not a valid float (e.g., containing errors or non-numeric characters), the script currently crashes. You must modify the script to **skip** these corrupted log entries safely and continue processing.
4. **State Tracing:** The current `current_state.csv` is in an unknown, partially updated, and precision-truncated state. You must rebuild the state from scratch. An untouched backup of the starting state is available at `/home/user/telemetry/initial_state.csv`.

**Acceptance Criteria:**
1. Fix `process_wal.sh` so it uses `bc` with a scale of 4 for precise floating-point math, and skips corrupted lines gracefully.
2. Re-run your fixed script using `initial_state.csv` as the starting point.
3. Save the final calculated sensor states to `/home/user/telemetry/final_state.csv` in the format `SENSOR_ID,EMA_VALUE` (e.g., `S1,10.1234`).