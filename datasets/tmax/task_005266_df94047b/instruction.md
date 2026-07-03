You have recently inherited a data processing pipeline from a departed developer. The system relies on a Python script located at `/home/user/process.py` to read and parse a binary sensor log `/home/user/sensor_data.bin`, and output the results to `/home/user/output.txt`. 

However, the script is currently producing incorrect and incomplete results:
1. **Floating-Point Errors:** The extracted coordinates (Latitude and Longitude) appear completely mangled and inaccurate. The binary file encodes each record as 24 bytes in little-endian format: a 4-byte magic number (`0xDEADBEEF`), a 4-byte unsigned integer timestamp, and two 8-byte IEEE 754 double-precision floats (Latitude, then Longitude). The script seems to be unpacking these incorrectly.
2. **Missing Data / Race Conditions:** The script uses multiprocessing to speed up processing, but the output file is often missing records or contains interleaved/garbled lines. There are exactly 10 valid records in the binary file, but the output file usually ends up with fewer, or broken text.
3. **Corrupted Input:** Some records in the binary file are corrupted (their magic number is not `0xDEADBEEF`). The script already has a check to skip them, but make sure your fixes don't break this logic.

Your task:
Fix `/home/user/process.py` so that it correctly extracts the double-precision floating-point values and safely writes all valid records to `/home/user/output.txt` without any race conditions or dropped lines. 

The final `/home/user/output.txt` must contain exactly the formatted strings for the valid records, one per line. The formatting should remain `Timestamp: {ts}, Lat: {lat:.4f}, Lon: {lon:.4f}`. Since multiprocessing order is non-deterministic, you must ensure your fixed script sorts the final output lines by the Timestamp in ascending order before writing them, or write them in order if collected in the main process.

Run your fixed script to generate the correct `/home/user/output.txt`.