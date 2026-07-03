As a Site Reliability Engineer, you monitor the uptime of our legacy infrastructure. Recently, several QEMU-based VMs have failed to boot properly due to filesystem issues, breaking our CI/CD pipeline. 

A VNC screenshot of the root-cause alert and the new policy has been saved to `/app/vnc_screenshot.png`. 

Your task is to write a Python script at `/home/user/fstab_linter.py` that acts as a CI/CD pre-flight check for `fstab` configuration changes. 

Requirements for `/home/user/fstab_linter.py`:
1. Use a tool like `tesseract` to read the SRE policy from the image `/app/vnc_screenshot.png`.
2. The script must accept exactly one argument: a string representing a single line from an `/etc/fstab` file (e.g., `python3 /home/user/fstab_linter.py "UUID=xxx / ext4 defaults 1 1"`).
3. The script must apply the rule discovered in the screenshot to the fstab line.
4. Parsing rules for the script:
   - Strip leading and trailing whitespace.
   - If the line is empty or starts with `#`, print the stripped line exactly as-is to standard output.
   - Otherwise, split the line by any whitespace into fields.
   - Apply the policy from the image. 
   - Reconstruct the line using exactly **one space** between each field.
   - Print the resulting line to standard output.
   - Do not print anything else.

Make sure your script perfectly conforms to these rules, as it will be rigorously tested against thousands of dynamically generated fstab entries in our verification suite.