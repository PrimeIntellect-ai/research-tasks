You are an AI assistant helping a materials science researcher organize and correct a massive dataset of 3D printing logs and toolpath files. 

The dataset is located in `/home/user/dataset/`. You will need to write a Python script to navigate the directories, parse specific log formats, and perform large-scale text editing on domain-specific files (GCode).

Here is the situation:
During a recent batch of experiments, a systematic sensor failure occurred. The researcher has a large multi-line event log file at `/home/user/dataset/machine_events.log`. Each event in the log spans multiple lines and is enclosed by `[EVENT START]` and `[EVENT END]`.

Your task is to:
1. Parse `/home/user/dataset/machine_events.log` to identify all prints that failed. A print is considered failed if its multi-line event block contains `Level: ERROR` and `Module: Extruder`. You need to extract the `PrintID` from these specific event blocks.
2. For each failed print, locate its corresponding GCode file in `/home/user/dataset/gcode/` (the file will be named `<PrintID>.gcode`).
3. Apply a systematic correction to the GCode files of the failed prints. The researcher determined that while Tool 0 (`T0`) was active during these specific failed prints, the Z-axis was offset by -0.5mm. You must correct this by adding `0.5` to the Z-axis value of any `G1` (linear move) command, but **only** while Tool 0 is the active tool.
   - GCode files are processed line-by-line from top to bottom.
   - The active tool is set by a line containing exactly `T0` or `T1`. Assume `T0` is the active tool at the very beginning of the file unless specified otherwise.
   - If a line starts with `G1` and contains a `Z` parameter (e.g., `G1 X10 Y20 Z1.2`), and the active tool is `T0`, you must parse the Z value, add 0.5 to it, and replace it in the string (e.g., `G1 X10 Y20 Z1.7`). Keep the formatting to 1 decimal place.
   - Do not modify `G1` lines if `T1` is the active tool. Do not modify lines that do not start with `G1` or do not contain a `Z` parameter.
4. Save the corrected GCode files to a new directory: `/home/user/dataset/corrected/`. The filenames should remain exactly the same (e.g., `P005.gcode`).
5. Generate a report file at `/home/user/report.txt`. Each line of the report should correspond to a corrected print, in alphabetical order of the PrintID, formatted exactly as: `PrintID: <number_of_Z_values_modified>`.

Ensure your script handles file I/O properly and has the correct permissions. You are expected to write and execute a Python script to achieve this end-to-end workflow.