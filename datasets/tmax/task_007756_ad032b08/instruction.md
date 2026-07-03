You are a storage administrator managing disk space on a heavily constrained server. An industrial machine controller has dumped a large backup of its operational logs, which were split into a multi-part archive due to upload restrictions. The server's current disk space is too low to fully extract the raw log files to disk.

The archive parts are located at:
`/home/user/archive/data.tar.gz.parta`
`/home/user/archive/data.tar.gz.partb`
`/home/user/archive/data.tar.gz.partc`

When merged and decompressed, this tarball contains a single large file named `machine.gcode`. 

Your task is to:
1. Write a Python script `/home/user/parse_gcode.py` that reads GCode data from standard input.
2. The script must parse the incoming GCode to find all lines that define a Z-axis movement (lines starting exactly with `G1 Z` followed by a numeric value, e.g., `G1 Z0.200 F7800` or `G1 Z1.4`).
3. Extract only the numeric Z value (e.g., `0.200`, `1.4`).
4. Output the strictly unique Z values, sorted numerically in ascending order, one per line.
5. Use a shell pipeline to merge the archive parts, extract the contents to standard output (bypassing the filesystem), and pipe the decompressed stream into your Python script.
6. Redirect the final output of your Python script to `/home/user/z_layers.txt`.

Example of a valid GCode line to match:
`G1 Z1.250 F300` -> extracted value: `1.250` (or `1.25`)

Do not extract the `.gcode` file to disk. The final `/home/user/z_layers.txt` file must contain only the sorted, unique floating-point Z values, formatted to 3 decimal places (e.g., `0.200`), one per line.