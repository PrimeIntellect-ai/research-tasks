You are an archiving administrator for a large 3D printing farm. You need to organize and back up GCode files based on their estimated print times, which are embedded as metadata within the files themselves.

Your task is to write a Rust command-line application in `/home/user/gcode_archiver` that reads a list of active GCode file paths from standard input (stdin). 
For each file path received from stdin, your Rust program must:
1. Open and parse the GCode file to find the estimated print time. In our custom GCode flavor, this is always on a single line starting exactly with `; estimated_time_s: ` followed by an integer representing the time in seconds (e.g., `; estimated_time_s: 4500`).
2. If the GCode file does not contain this line, safely ignore it.
3. If the estimated time is **greater than or equal to 7200 seconds** (2 hours), create a **hard link** to this file inside the directory `/home/user/archive/long_prints/`. The hard link should have the exact same filename as the original file.
4. If the estimated time is **strictly less than 7200 seconds**, create a **symbolic link** (symlink) to this file inside the directory `/home/user/archive/short_prints/`. The symlink must also have the exact same filename as the original file.

To execute the task, write the Rust program, compile it, and run it by piping the configuration file `/home/user/print_farm.conf` into your executable.

Example execution:
`cat /home/user/print_farm.conf | /home/user/gcode_archiver/target/debug/gcode_archiver`

Ensure that the target directories `/home/user/archive/long_prints/` and `/home/user/archive/short_prints/` exist before creating the links (your Rust program or a shell script can create them).