You are helping to configure a change-tracking pipeline for our 3D printer fleet. Our configuration manager tracks GCode profiles, but users often submit messy or unsafe GCode. We need to enforce standardization.

Your task is to write a Python script at `/home/user/process_gcode.py` that normalizes GCode according to a specific set of rules. 

We have received a rule specification as an image, located at `/app/processing_rules.png`. You will need to extract the rules from this image (e.g., using `tesseract`) to understand exactly how the GCode must be formatted and constrained.

Requirements for your script:
1. It must read raw GCode from `stdin` and print the processed GCode to `stdout`.
2. It must correctly parse the domain-specific GCode format to apply the capping and formatting rules extracted from the image.
3. It should be efficient enough to handle large macro files.
4. Ensure your script is executable (`chmod +x /home/user/process_gcode.py`) and includes the appropriate python shebang.

Do not write any hardcoded file paths in your script; it must rely entirely on standard I/O streams. The automated verification will test your script against thousands of generated test cases to ensure it behaves exactly as the rules dictate.