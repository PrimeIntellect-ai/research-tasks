You are a support engineer tasked with collecting diagnostics and determining the root cause of a recent autonomous drone crash. The system relies on a mix of legacy C++ binaries, Python scripts, and bash pipelines. The incident wiped some data, but we have a few artifacts remaining. 

You need to perform the following steps to reconstruct the diagnostic timeline and fix the faulty data parser:

1. **Dashboard Video Analysis**: A screen recording of the ground control station was saved just before the crash at `/app/flight_dashboard.mp4`. We need to know exactly how many times the critical failure indicator flashed. Extract the video frames and count the number of frames where the pixel at coordinates (X=10, Y=10) is pure red (RGB: 255, 0, 0). Write this integer to `/home/user/flash_count.txt`.

2. **Deleted Log Recovery**: The crash corrupted the filesystem, deleting the primary telemetry log. A raw image of the partition is available at `/app/drone_data.img`. Recover the deleted log file named `telemetry_raw.log` and save it to `/home/user/telemetry_raw.log`.

3. **Log Timeline Reconstruction**: The recovered log contains entries from multiple microservices (Nav, Sensor, Comms), but the timestamps are corrupted and out of order. Write a bash script `/home/user/reconstruct.sh` that parses `/home/user/telemetry_raw.log`, sorts the events chronologically using the sequence IDs embedded in the payload, and outputs a clean timeline to `/home/user/timeline.log`.

4. **Parser Repair**: The crash was ultimately caused by a floating-point precision error in the legacy C++ binary used to decode telemetry packets, located at `/app/legacy_decoder`. Decompile or reverse-engineer this binary. You will notice it reads an 8-byte hex string representing a double-precision float, but truncates it to single-precision before performing a calculation, causing drift. 
   
   Write a new, fully functional decoder program (in any language you prefer, but make it executable via a bash wrapper at `/home/user/fixed_decoder`) that reads the same 8-byte hex inputs from `stdin`, processes them *without* the single-precision truncation, and outputs the corrected floating-point values to `stdout`.

Your final output for the decoder must be bit-exact equivalent to our reference implementation. Ensure your wrapper `/home/user/fixed_decoder` is executable.