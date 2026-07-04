You are assisting a researcher who is organizing a large dataset of 3D printing GCode files. The researcher receives a continuous stream of `.gcode` files in an incoming directory and needs to automatically extract metadata, generate a manifest, and archive them.

Your task is to build a background file processing pipeline:

1. Create two directories: `/home/user/incoming_gcode` and `/home/user/archived_gcode`.
2. Write a Python script `/home/user/process_gcode.py` that watches the `/home/user/incoming_gcode` directory for new files. You may use the `watchdog` library or simple polling (e.g., checking every 0.5 seconds).
3. When a new `.gcode` file appears, your script must:
   - Calculate its SHA256 checksum.
   - Parse the file to extract the filament usage. Specifically, find the line that starts exactly with `; filament used [mm] = ` and extract the numeric value as a float.
   - Append a JSON object to `/home/user/gcode_manifest.jsonl` (one valid JSON object per line) containing exactly these keys:
     - `"filename"`: The basename of the file (e.g., `"print1.gcode"`).
     - `"sha256"`: The hex digest of the SHA256 checksum.
     - `"filament_mm"`: The extracted filament usage as a float.
   - Move the processed file to `/home/user/archived_gcode/`.
4. Your script must output logging information to standard output/error.
5. A simulation script is provided at `/home/user/simulate_incoming.py`. It will automatically drop several test `.gcode` files into the incoming directory over a few seconds.

To complete the task:
- Install any necessary dependencies.
- Start your `process_gcode.py` script in the background, redirecting both standard output and standard error to `/home/user/processing.log`.
- Run `/home/user/simulate_incoming.py` and wait for it to complete.
- Ensure your background script has processed all files.
- Terminate your background script cleanly (or kill it).
- Verify that `/home/user/gcode_manifest.jsonl` and `/home/user/archived_gcode/` contain the expected results.