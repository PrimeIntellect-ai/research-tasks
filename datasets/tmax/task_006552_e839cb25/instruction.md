You are a mobile build engineer maintaining a CI/CD pipeline for a legacy cross-platform app. To avoid encoding issues with special characters in the build logs and CI artifacts, the mobile team uses a custom hex-encoded data structure for application resources (like strings and feature flags).

Your task is to write a Bash script that acts as a custom resource compiler. 

Create an executable Bash script at `/home/user/resource_compiler.sh`.

When executed, your script must do the following:

1. **Read the encoded resource manifest** located at `/home/user/raw_resources.txt`. 
   Each line in this file follows a custom data structure: `<TYPE>:<HEX_ENCODED_KEY>:<HEX_ENCODED_VALUE>`
   Example: `STR:4150505f4e414d45:4d79417070` (which decodes to `STR:APP_NAME:MyApp`).

2. **Generate a build system configuration file** at `/home/user/build/res_map.sh`.
   For each line in the manifest, decode the hex key and value, and write an export statement to this file. 
   Format: `export <DECODED_KEY>="<DECODED_VALUE>"`

3. **Generate a unit test stub** at `/home/user/tests/test_res.sh`.
   This script must:
   - Include a shebang `#!/bin/bash`.
   - Source the generated configuration file (`source /home/user/build/res_map.sh`).
   - For every resource parsed from the manifest, add a test check. The check should verify that the variable matches the decoded value.
   - If it matches, echo `PASS: <DECODED_KEY>`. If it fails, echo `FAIL: <DECODED_KEY>`.
   - Ensure `/home/user/tests/test_res.sh` is made executable.

4. **Execute the test stub** as the final step of `/home/user/resource_compiler.sh` and redirect its standard output to `/home/user/build/test_results.log`.

Make sure you create the `/home/user/build` and `/home/user/tests` directories inside your script before writing to them. Use pure Bash and standard Unix utilities (like `xxd` or `sed`) to accomplish this. Do not use external scripting languages like Python or Perl.

Run your script once you have finished writing it so that `/home/user/build/test_results.log` is generated.