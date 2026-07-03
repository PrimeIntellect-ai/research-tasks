I am a researcher organizing my 3D printing experimental datasets. Recently, my data collection system experienced a crash during an aggressive log rotation and compression cycle. This left a messy directory of nested archives in `/home/user/datasets`. Because of the crash, some of these archives are corrupted or incomplete.

I need you to process this directory and calculate the total experimental time. Please do the following:

1. Recursively find and extract all `.zip` and `.tar.gz` archives starting in `/home/user/datasets`. Handle nested archives (archives inside archives) until no more unextracted archives remain.
2. **Crucial:** You must verify the integrity of each archive before attempting to extract it. If an archive is corrupted or fails the integrity check, completely ignore it and do not attempt to extract it.
3. Once all valid archives are fully extracted, recursively search through all the files to find all `.gcode` files.
4. Parse these `.gcode` files to extract the estimated print time. In our GCode files, the time is stored on a line starting exactly with `;TIME:` followed by an integer representing seconds (e.g., `;TIME:4520`). There is exactly one such line per valid `.gcode` file.
5. Sum the time (in seconds) from all the extracted `.gcode` files.
6. Write the final total sum as a single integer to the file `/home/user/total_print_time.txt`.

You may use Bash, Python, or any combination of standard Linux tools to accomplish this. Ensure your solution gracefully skips the corrupted archives without failing.