You are an engineer troubleshooting a failing build in a CI/CD pipeline environment. 

A coworker recently submitted a hotfix for a C application, but their machine crashed before they could commit the changes to version control. The current build is failing with a linker error.

Fortunately, we were running a network packet capture on their machine when they downloaded a snippet of the fix from an internal HTTP server. This packet capture has been saved to your environment.

Your environment is located in `/home/user/app`. Inside, you will find:
- `main.c` and `hash.c` (the application source code)
- `build.sh` (the build script, which currently fails)
- `traffic.pcap` (a network capture containing the HTTP response with the raw diff/patch)

Your tasks:
1. Interpret the compiler/linker error by running `./build.sh`.
2. Analyze the `traffic.pcap` file using standard shell utilities (like `strings`, `grep`, etc.) to locate and extract the unified diff payload transferred over HTTP.
3. Apply the reconstructed patch to the source code to fix the linker error.
4. Run `./build.sh` successfully.
5. Execute the compiled `./app` binary and redirect its standard output to `/home/user/app/success.log`.

Constraints:
- Do not manually edit the C files; you must extract and apply the patch from the pcap file.
- You are restricted to standard Linux command-line tools (e.g., coreutils, binutils, patch).