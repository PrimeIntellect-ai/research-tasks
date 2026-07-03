You are a release manager preparing a deployment for a multi-architecture application. As part of your CI/CD pipeline, you need to automate a conditional build step and implement memory profiling to catch architecture-specific memory leaks before release.

We have a source file located at `/home/user/src/worker.c`. This file contains conditional compilation directives (`#ifdef`) that alter its memory management behavior based on the target architecture. 

Your task is to write a Python script at `/home/user/ci_pipeline.py` that acts as an automated CI step. The script must perform the following actions:

1. **Conditional Build**: 
   - Compile `/home/user/src/worker.c` into a binary named `/home/user/bin/worker_x86` using the GCC flag `-DARCH_X86`.
   - Compile the same source into a binary named `/home/user/bin/worker_arm` using the GCC flag `-DARCH_ARM`.
   *(You may assume `gcc` is installed. Ensure the `/home/user/bin` directory exists before compiling).*

2. **Memory Profiling**:
   - Execute both binaries.
   - Profile the peak Resident Set Size (RSS) memory usage of each process in Kilobytes (KB). You can use `/usr/bin/time -v`, Python's `resource` module, or any other method you prefer to capture the max RSS.

3. **Reporting**:
   - Determine which binary suffers from a memory leak (the one with significantly higher peak memory usage).
   - Generate a JSON report at `/home/user/memory_report.json` with the exact following structure:
     ```json
     {
       "worker_x86": <peak_rss_kb_integer>,
       "worker_arm": <peak_rss_kb_integer>,
       "leak_detected": "<name_of_leaking_binary>"
     }
     ```
     *(Example for `leak_detected`: "worker_arm" or "worker_x86")*

You are free to test your script by running `python3 /home/user/ci_pipeline.py` in your terminal to ensure it correctly builds the binaries and produces the JSON report.