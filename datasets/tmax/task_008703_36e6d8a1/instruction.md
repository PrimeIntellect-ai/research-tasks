You have inherited an unfamiliar legacy data processing pipeline located at `/home/user/legacy_project`. The previous developer left abruptly, and the pipeline is currently broken.

You need to perform a comprehensive debugging and recovery operation:

1. **Deleted File Recovery:** 
   The pipeline relies on a configuration file named `calibration_params.txt` which was accidentally deleted from a backup filesystem image. 
   You are provided with an ext4 filesystem image at `/home/user/legacy_project/backup_drive.ext4`. 
   Recover the deleted `calibration_params.txt` from this image. Save the recovered file to `/home/user/legacy_project/recovered_params.txt`.

2. **Intermittent Failure Reproduction & Numerical Instability:**
   There is a compiled binary named `/home/user/legacy_project/metric_evaluator`. The inherited bash script `/home/user/legacy_project/process_sensors.sh` processes sensor readings from `/home/user/legacy_project/sensor_data.csv` by passing them to `metric_evaluator`.
   However, the pipeline intermittently fails with an anomalous output (either a crash, `NaN`, or `Infinity`) due to numerical instability in the binary when processing a specific sensor reading.
   Write a Bash script that isolates the intermittent failure. Identify the exact line number in `sensor_data.csv` that causes the binary to fail or output a non-finite number. 
   Write just the integer line number (1-indexed) to `/home/user/legacy_project/buggy_line_number.txt`.

3. **Binary Inspection / Reverse Engineering:**
   The `metric_evaluator` binary has a hardcoded secret floating-point "safety threshold" that causes this instability when a calculated value approaches it. 
   Inspect the binary to find this hardcoded threshold value. 
   Write the exact threshold value (as it appears in the binary's readable data or decompiled source/strings) to `/home/user/legacy_project/secret_threshold.txt`.

Your final deliverables must be exactly at these paths:
- `/home/user/legacy_project/recovered_params.txt` (the recovered text file)
- `/home/user/legacy_project/buggy_line_number.txt` (single integer)
- `/home/user/legacy_project/secret_threshold.txt` (single floating point number)