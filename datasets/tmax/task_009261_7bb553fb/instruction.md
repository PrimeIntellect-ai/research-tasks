You are a support engineer investigating a failing deployment process on a Linux system. 

The main deployment script located at `/home/user/deploy_system.sh` reads a configuration file at `/home/user/services.conf` and attempts to converge the system state by ensuring specific lock files are created for "enabled" services. However, the build is currently failing, and the script exits with an error indicating that convergence was not reached.

Your analysis shows that the bash script has edge-case format parsing bugs. Specifically, it fails to correctly parse lines in `services.conf` that contain inline comments or trailing whitespace. Because of this, it skips services that should be enabled, leading to an assertion failure at the end of the script.

Your task:
1. Debug and fix the `/home/user/deploy_system.sh` script so that it correctly parses all lines in `/home/user/services.conf` (ignoring pure comment lines, empty lines, and properly stripping inline comments and trailing spaces from the parsed values).
2. Ensure the script runs successfully without exiting with an error code.
3. After the script runs successfully, gather diagnostics by creating a file named `/home/user/diagnostics.log`. This file must contain the absolute paths of all the `.lock` files created in the `/home/user/locks/` directory, printed one per line, sorted alphabetically.

Do not change the `services.conf` file, and do not change the `EXPECTED_ENABLED` value in the script. You must fix the parsing logic itself.