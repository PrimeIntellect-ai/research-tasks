You are a release manager preparing a new deployment for a secure web application. Part of your deployment pipeline requires verifying the integrity and security of the binaries and configurations being shipped. 

You must write a Bash script named `/home/user/release/prepare_release.sh` that performs the following checks and testing routines. The script must be executable.

Your script must perform the following tasks:

1. **ABI Security Check**: 
   Analyze the shared library `/home/user/release/libauth.so`. Determine if it contains an undefined external symbol named `MD5_Init` (which is deprecated and insecure). 
   - If `MD5_Init` is found as an undefined symbol, the script should record `abi_secure: false`. Otherwise, `abi_secure: true`.

2. **Assembly-level Analysis**:
   Analyze the provided object file `/home/user/release/handler.o`. Find the hex address offset of the function `<check_auth>`. Keep this hex string (without leading zeros, just the hex part, e.g., `4a` or `112`).

3. **Expression Parsing and Evaluation**:
   Read `/home/user/release/thresholds.conf`. This file contains mathematical expressions for security limits in the format `KEY = EXPRESSION` (e.g., `max_retries = (5 * 2) - 3`).
   Evaluate the mathematical expression for `max_retries` using standard bash arithmetic evaluation.

4. **Integration Testing & Reporting**:
   Based on the above steps, create a JSON report file at `/home/user/release/report.json` with the exact following structure:
   ```json
   {
     "abi_secure": false,
     "check_auth_offset": "hex_value_here",
     "max_retries_value": 7
   }
   ```
   (Replace `false`, `"hex_value_here"`, and `7` with the actual computed values).

Write the script, make it executable, and run it to produce the `report.json` file. Ensure your script handles the file parsing robustly.