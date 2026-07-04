You are a systems engineer diagnosing a failing user-space deployment service. The service, which handles staged deployments of mailing list configurations, is crashing because its configuration validator (`/app/mail_config_validator`) is a legacy stripped binary that no longer works correctly with the new deployment automation scripts.

Your objective is to reverse-engineer this black-box binary and write a clean C++ replacement that strictly mirrors its behavior, allowing our deployment pipeline to resume.

Here is what you know:
1. The legacy binary is located at `/app/mail_config_validator`. 
2. The binary takes a single command-line argument: the absolute path to a configuration file.
3. It parses the file, validates its structure, and prints a specific string to standard output, returning exit code `0` on success and `1` on failure.
4. You must write a C++ program at `/home/user/new_validator.cpp` that implements the EXACT same validation logic (producing identical standard output and exit codes for any given input file).
5. Compile your C++ program to `/home/user/new_validator`.

You can use standard tools (`strings`, `hexdump`, `objdump`, `gdb`, or a bash task automation script generating inputs) to analyze how `/app/mail_config_validator` processes different files. 

Constraints:
- You must use C++ for your replacement implementation (`/home/user/new_validator.cpp`).
- You may write bash scripts to automate the testing and comparison of your C++ program against the legacy binary.
- Do not attempt to run this as root or use `sudo`; everything must be done within `/home/user`.
- The final executable must be exactly at `/home/user/new_validator`.