You are a developer tasked with organizing legacy manufacturing project files for a CNC shop. We recently upgraded our CNC machinery, and the old GCode files need to be audited to ensure they do not exceed the physical limits of the new machine.

Your workflow will involve the following steps:

1. **Extract constraints from audio:**
   The chief machinist recorded an audio memo detailing the strict safety limits of the new machine. The audio file is located at `/app/machine_limits.wav`. 
   You must transcribe or listen to this audio file (you may install tools like `ffmpeg` or use Python libraries/APIs if you prefer) to discover the allowed limits for:
   - Maximum X axis coordinate (X)
   - Maximum Y axis coordinate (Y)
   - Minimum Z axis coordinate (Z) (note: Z goes negative into the material)
   - Maximum Spindle Speed (S)

2. **Create a GCode Validator:**
   Write a Python script at `/home/user/gcode_validator.py`.
   This script must accept exactly one argument (the path to a `.gcode` file).
   It should parse the GCode file line by line and verify that no commands exceed the limits you found in the audio log. 
   - A line might look like `G1 X140.5 Y100.0 Z-5.0` or `M3 S8000`.
   - Ignore comments (anything after a `;` on a line).
   - If the file is perfectly safe (all X, Y, Z, and S values are within the limits), the script must exit with status code `0`.
   - If the file violates ANY of the limits, the script must exit with status code `1`.

3. **Process Legacy Projects:**
   There is a compressed archive of old projects located at `/app/legacy_projects.tar.gz`. 
   Extract this archive. It contains a deeply nested directory structure with various files, including `.gcode` files, ELF binaries (which you can ignore), and text logs.
   Using your `/home/user/gcode_validator.py` script, evaluate every `.gcode` file in the extracted archive.
   Collect all the `.gcode` files that pass validation (exit code 0) and archive them into a single, flat compressed tarball at `/home/user/valid_projects.tar.gz` (do not preserve the old directory structure in the new tarball, just put the valid `.gcode` files at the root of the archive).

Ensure your script is robust against spacing variations in GCode (e.g., `X10` vs `X 10`). You have full permissions in `/home/user`.