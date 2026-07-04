You are a security researcher investigating a suspicious container build that failed abruptly. The malicious actor tried to cover their tracks by deleting the core C module from the filesystem before the container crashed.

Your objective is to recover the deleted file, diagnose the build failure, fix the bugs, and execute the malware runner to generate the final payload.

You have been provided with an investigation directory at `/home/user/investigation/` containing:
1. `fs.ext4`: An unmounted ext4 filesystem image from the container. The attacker deleted a file named `core.c` from the root of this filesystem.
2. `build.log`: The captured standard error and standard output of the failed container build process.
3. `malware_runner.py`: A Python script that the attacker was trying to build and run. It uses `ctypes` to compile and load `core.c`.

Perform the following steps:
1. Recover the deleted `core.c` file from `fs.ext4` and place it at `/home/user/investigation/core.c`. You may use tools like `sleuthkit` to inspect the ext4 image and extract the deleted inode.
2. Read `build.log` to understand why the build process crashed. 
3. Diagnose and fix the bug in `/home/user/investigation/malware_runner.py` that caused the build/run to fail. 
4. The `build.log` leaks the specific environment variable configuration the attacker used during the crash. Use this exact leaked secret key to run the fixed `malware_runner.py`.
5. Redirect the standard output of the successful run of `malware_runner.py` to `/home/user/investigation/report.txt`.

Ensure `/home/user/investigation/report.txt` contains the exact final output printed by the script.