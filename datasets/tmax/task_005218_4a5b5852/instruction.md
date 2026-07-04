You are tasked with fixing and optimizing a local data pipeline used for processing sensor logs. The pipeline consists of multiple cooperating components managed by a custom Bash supervisor. 

Currently, the pipeline fails to run correctly and takes too long when it does work. You must fix the synchronization, correct environmental issues, and optimize the processing script to meet strict performance metrics.

**System Overview**
All files are located in `/home/user/app/`.
- `supervisor.sh`: A basic process supervisor that launches the components in the background.
- `sensor.sh`: Simulates a virtual machine generating log files into `/home/user/app/data/`. It takes a moment to initialize.
- `processor.sh`: A Bash script that reads the generated logs, filters them based on the current date, and performs a heavy CPU operation (simulated via `sleep`), outputting results to `/home/user/app/output/`.

**Issues to Fix**
1. **Missing Dependency / Race Condition**: When you run `./supervisor.sh`, `processor.sh` often crashes immediately because `sensor.sh` hasn't created the `ready.flag` in the data directory yet. Implement a robust waiting mechanism or restart policy in `processor.sh` so it waits for `/home/user/app/data/ready.flag` to exist before proceeding.
2. **Timezone Mismatch**: `sensor.sh` generates logs with UTC timestamps. However, `processor.sh` defaults to the system's local timezone (simulated as `America/New_York`), causing it to silently drop valid logs because the date strings don't match. Modify the startup configuration in `supervisor.sh` to ensure `processor.sh` runs with the `UTC` timezone.
3. **Performance Optimization**: `processor.sh` currently loops through the log files sequentially. Each log takes about 0.5 seconds to process, meaning 20 logs take ~10 seconds. Rewrite the processing loop in `/home/user/app/processor.sh` (using pure Bash, `xargs`, or `wait`) to process the files concurrently. 

**Requirements for Success**
- The pipeline must process exactly 20 logs successfully and produce 20 output files in `/home/user/app/output/`.
- Total execution time of `/home/user/app/supervisor.sh` must be **less than 3.5 seconds**. 
- Do not modify `sensor.sh`. 
- Ensure all final outputs are correctly written. Run `./supervisor.sh` to verify your changes. When you are confident, leave the completed pipeline ready for automated testing.