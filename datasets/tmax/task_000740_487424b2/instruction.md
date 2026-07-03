You are a platform engineer troubleshooting a CI/CD pipeline failure. A CMake project is failing at the linking stage because a newly introduced security library is either missing or severely outdated on the build nodes. 

To unblock the CI pipeline immediately, you need to write a dynamic Bash script that creates a mock version of the shared library, ensuring the required symbols are exported so the linking phase can succeed.

Write a Bash script at `/home/user/deploy_mock_lib.sh` that performs the following steps:
1. Parse the JSON configuration file located at `/home/user/deps.json`. This file contains the library name, the minimum required semantic version, and the specific exported symbol the CMake project expects.
2. Read the currently installed version string from `/opt/sec_libs/version.txt`.
3. Perform a semantic version comparison between the installed version and the `min_version` specified in the JSON. 
4. If the installed version is greater than or equal to the minimum version, the script should simply write "SYSTEM_UP_TO_DATE" to `/home/user/pipeline.log` and exit.
5. If the installed version is strictly less than the minimum version, your script must:
   - Generate a minimal x86_64 assembly source file (e.g., GNU AS syntax) that defines a global function matching the exact `symbol` name parsed from the JSON. The function should simply return `0` (e.g., clear the RAX register and return).
   - Assemble and link this file into a shared library named `<lib_name>.so` (using the `lib_name` from the JSON) and place it in the directory `/home/user/build/`. 
   - Write "MOCK_BUILT" to `/home/user/pipeline.log`.

Make sure the script has execute permissions (`chmod +x`) and test it. The script must be fully dynamic; it should read the target symbol and library name exclusively from `/home/user/deps.json` and not hardcode them.

Available tools include standard coreutils, `jq`, `gcc`, `as`, and `ld`.