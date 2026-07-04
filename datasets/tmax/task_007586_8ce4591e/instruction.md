You are a systems programmer working on a web security utility. We have a C-based custom URL encoder designed to sanitize inputs against XSS attacks, but the build system is broken due to compilation and linking errors.

The project is located in `/home/user/sec_lib/` and contains the following files:
- `urlsec.c`: The source code for our shared library containing the encoding logic.
- `urlsec.h`: The header file.
- `main.c`: The command-line interface that uses the library.
- `Makefile`: The broken build script.

Your task is to:
1. Fix the `Makefile` in `/home/user/sec_lib/` so that running `make` successfully builds the shared library `liburlsec.so` and the executable `urltool`. (Hint: You will need to add position-independent code flags for the shared library and correct the linking flags for the executable).
2. Write a Bash script at `/home/user/sec_lib/run_tool.sh` that accepts exactly one argument (a string). The script must execute the compiled `urltool` with the provided string, ensuring the runtime linker can find `liburlsec.so` (which resides in the same directory). The script should redirect the standard output of `urltool` to `/home/user/sec_lib/output.txt`. Make sure the script is executable.
3. Execute your script using the following web security payload as the argument: `"javascript:<script>alert(1)</script>"`

If successful, the sanitized encoded string will be saved in `/home/user/sec_lib/output.txt`.