You are a performance engineer tasked with profiling a legacy C application. The project is located in `/home/user/perf_app`. 

Currently, the application is in a broken state. Your goal is to successfully build the application, execute its profiling mode, and generate the required output file.

Here is what you know:
1. The build script (`/home/user/perf_app/build.sh`) is currently failing with linker errors. You will need to fix it so the application compiles successfully.
2. The application is designed to run in a special profiling mode that requires a legacy API key passed as a command-line argument (e.g., `./metrics_calc <API_KEY>`).
3. The API key was previously hardcoded in the source code but was recently removed for security reasons. You will need to recover this key from the git history of the repository.
4. Even with the correct key, the application currently crashes (Segmentation fault) during execution. You must use a debugger (like `gdb`) to find the memory issue, fix the C code, and recompile.

Your objective is complete when you successfully run the application with the correct key, and it generates the profiling report exactly at `/home/user/profile_results.txt`. Do not change the underlying mathematical logic in the C code; only fix the memory allocation bug that causes the crash.