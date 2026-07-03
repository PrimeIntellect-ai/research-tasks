I am porting our legacy Bash-based data processing tool to run in a minimal Linux container, but I'm running into two major issues preventing it from working. I need your help to debug and fix the system.

The tool processes log files using a custom bash state machine and filters entries based on semantic versioning. It interacts with a custom C-based shared library for the version parsing. 

Here are the problems:
1. **Circular Import:** When I run `/home/user/app/run.sh`, it immediately crashes with a deep recursion/nesting error. I suspect there is a circular `source` dependency between the Bash modules in `/home/user/app/lib/`. You need to find and remove the circular inclusion without breaking the functionality.
2. **Shared Library Linkage:** The bash scripts rely on a compiled binary `/home/user/app/bin/vercheck` to do the heavy lifting of semantic version comparison. However, the ABI/shared library management is broken. It expects a shared library named `libsemver.so.1`, which was compiled into `/home/user/app/lib/` as `libsemver.so.1.0`, but the system cannot find it when the binary runs. You need to fix the symlinks and runtime library path configuration so the `vercheck` binary executes successfully when called by the scripts.

**Objective:**
1. Fix the Bash circular import issue in `/home/user/app/lib/`.
2. Fix the shared library loading issue for `/home/user/app/bin/vercheck`.
3. Execute `/home/user/app/run.sh`. This script will automatically read `/home/user/data/input.txt` and generate `/home/user/processed_data.json`.

Ensure that `/home/user/processed_data.json` is successfully generated and contains the valid filtered JSON output. Do not modify the core logic of the state machine or the C source code, only fix the import/linking issues.