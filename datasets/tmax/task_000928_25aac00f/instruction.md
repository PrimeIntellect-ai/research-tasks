You are an on-call engineer who just got paged at 3 AM. The primary authentication service is down in the staging environment. 

A junior developer accidentally deleted the source code for the authentication library (`auth.cpp`) and the compiled shared object (`libauth.so`). The main service binary, `/home/user/auth_service`, is now failing to start due to a missing library and undefined symbols. 

Here is what you need to do to resolve the incident:

1. **Recover the Source Code:** The file `auth.cpp` was recently deleted, but its plaintext contents are still present in a raw disk dump located at `/home/user/disk_image.bin`. Extract the C++ source code from this binary dump and save it as `/home/user/auth.cpp`. The source code starts with the comment `// AUTH_MODULE_START` and ends with `// AUTH_MODULE_END`.

2. **Fix Linker Errors:** The recovered `auth.cpp` has a slight naming error made by the junior developer just before it was deleted. If you compile it as-is, `auth_service` will fail to resolve the required symbol at runtime. You must analyze the `auth_service` binary to determine the exact C++ function signature and namespace it expects. Modify your recovered `auth.cpp` to match this signature so that it links correctly. 

3. **Rebuild the Library:** Compile your fixed `auth.cpp` into a shared library named `/home/user/libauth.so`. 

4. **Reproduce Intermittent Failures:** Even when successfully linked, the authentication module has a known intermittent bug that causes `auth_service` to crash randomly (non-zero exit code). Write a bash script at `/home/user/reproduce.sh` that repeatedly executes `./auth_service` (make sure to set `LD_LIBRARY_PATH=/home/user`). As soon as `auth_service` crashes, the script should append the exact word `CRASHED` to `/home/user/status.log` and exit successfully. 

Run your `reproduce.sh` script to confirm it catches the crash and writes to the log. 

Ensure the final state of the system contains:
- The fixed source code at `/home/user/auth.cpp`
- The compiled library at `/home/user/libauth.so`
- The script at `/home/user/reproduce.sh`
- The log file `/home/user/status.log` containing the word `CRASHED`