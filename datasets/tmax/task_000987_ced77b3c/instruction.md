You are tasked with debugging a failing build for a legacy application project located in `/home/user/project`. 

When you run `/home/user/project/build.sh`, the build fails due to a configuration parsing error. Upon inspection, you will notice that the bash-based configuration parser (`parse_config.sh`) is failing to correctly process edge cases in the `config.ini` file, specifically inline comments and floating-point multipliers. This causes precision loss or outright syntax errors when calculating the memory threshold using `bc`.

Additionally, the build script requires a deployment API key to simulate a successful build artifact upload. This key was accidentally committed to the Git repository in the past, but was subsequently removed. 

Your objectives:
1. **Git Forensics:** Find the removed deployment API key in the git history of the `/home/user/project` repository. Save the raw secret key string into `/home/user/api_key.txt`.
2. **Format Parsing & Precision Fix:** Modify `/home/user/project/parse_config.sh` so that it correctly strips inline comments (anything after and including `#` on a line) and successfully passes the pure floating-point numbers to `bc` for calculation. The build should complete successfully (exit code 0) after your fixes.
3. **MRE Creation:** Create a Minimal Reproducible Example script at `/home/user/project/mre.sh` that takes a single string as an argument, strips any trailing inline comments and whitespace, and echoes the clean floating-point value. For example, running `./mre.sh "1.75 # multiplier"` should output exactly `1.75`. Make sure `mre.sh` is executable.

The final system state will be verified by:
- Checking the contents of `/home/user/api_key.txt`.
- Running `/home/user/project/build.sh` and ensuring it returns a 0 exit code.
- Running `/home/user/project/mre.sh "3.14159 # pi"` and checking that it outputs `3.14159`.