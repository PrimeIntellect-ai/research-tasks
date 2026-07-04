You are a security researcher analyzing a suspicious compiled binary located at `/home/user/suspicious`. 

From static analysis, we know it reads mathematical coordinates from `/home/user/input.txt`. We have a helper Bash script `/home/user/generate.sh` that attempts to generate a test `input.txt` file, but the binary currently rejects its output with a "Format error". Furthermore, we suspect the binary triggers a specific payload when the sum of the coordinates exactly matches a hidden floating-point threshold, but standard shell math often suffers from precision loss that prevents triggering it.

Your objectives:
1. Debug and fix the format parsing edge-case in `/home/user/generate.sh` so that the binary successfully parses the generated `input.txt` without printing "Format error".
2. Use dynamic analysis tools (such as system call or library tracing) on the `/home/user/suspicious` binary to discover the hidden floating-point target sum it expects.
3. Modify `/home/user/generate.sh` to accurately generate numbers in `input.txt` that sum exactly to the hidden target, taking care to avoid bash precision loss. 
4. Run the binary with your crafted `input.txt` to trigger the payload.

The task is complete when the binary successfully drops its payload into `/home/user/flag.txt`. Make sure this file exists and contains the success key.