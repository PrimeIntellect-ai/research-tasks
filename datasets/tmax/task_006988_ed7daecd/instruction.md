You are a developer tasked with debugging a failing build step in a continuous integration system.

The build script `/home/user/build_tool.py` parses a dependency manifest file located at `/home/user/system_manifest.conf` to generate a compiled build list. However, the script is currently crashing. 

Your investigation indicates there are two main issues:
1. An off-by-one boundary condition in the main parsing loop that causes an out-of-bounds error.
2. The script assumes all lines in the manifest are perfectly formatted. It lacks corrupted input handling. Recently, some malformed entries (lines that do not have exactly 3 comma-separated fields) were introduced into the manifest, causing the script to crash.

Your task:
1. Fix the boundary condition in `/home/user/build_tool.py`.
2. Add logic to intermediate state processing to gracefully recover from corrupted input: if a line does not contain exactly three comma-separated fields, the script must **skip the line entirely** and continue parsing the rest of the file.
3. Run the repaired script with the following command to produce the final output:
   `python3 /home/user/build_tool.py --manifest /home/user/system_manifest.conf --output /home/user/build_output.txt`

If you are successful, the script will complete without errors and `/home/user/build_output.txt` will be created containing the properly formatted list of valid packages.