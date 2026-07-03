I am a researcher organizing datasets from our custom bio-printer, and I need help extracting specific data from our print logs. The printer outputs standard GCode, but I only care about the extrusion commands that happen within a specific vertical region of interest (a specific Z-height range) defined for each experiment.

I have an experiment directory at `/home/user/dataset/` containing two files:
1. `experiment.conf`: A configuration file specifying the region of interest.
2. `print_run.gcode`: The raw GCode log from the bio-printer.

You need to write a Bash script (using standard Linux tools like `awk`, `sed`, or `grep`) to process this data. 

Here are the specific rules for parsing:
1. **Read the Configuration:** The `experiment.conf` file contains key-value pairs (e.g., `Z_MIN=2.5`). Extract the `Z_MIN` and `Z_MAX` values.
2. **Track Z-Height:** In GCode, the printer's Z-height is stateful. It starts at `0.0`. It changes whenever a command contains a `Z` parameter (e.g., `G0 Z2.0` or `G1 X10 Y10 Z2.5 F300`). The Z-height remains at this value for all subsequent lines until another `Z` parameter is encountered.
3. **Filter Extrusions:** Identify all lines that represent an actual extrusion movement. An extrusion movement is defined as a line starting with `G1` that also contains an `E` parameter (e.g., `G1 X12.5 Y14.0 E0.012`). 
4. **Apply Z-Bounds:** Only keep the extrusion lines where the *currently active Z-height* is strictly greater than or equal to `Z_MIN` and strictly less than or equal to `Z_MAX`.
5. **Handle Comments:** Ignore inline comments. Anything from a semicolon (`;`) to the end of the line should be stripped out before processing the line. Completely blank lines (or lines that become blank after stripping comments) should be ignored.

**Output Requirements:**
1. Save the filtered extrusion lines (with comments stripped and trailing whitespaces removed) to `/home/user/dataset/filtered_extrusion.gcode`.
2. Count the total number of lines written to that file and save this integer to `/home/user/dataset/summary.txt`.

Perform this data extraction now.