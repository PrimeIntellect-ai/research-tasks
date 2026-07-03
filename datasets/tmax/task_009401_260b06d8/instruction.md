You are an engineer tasked with investigating a severe memory leak in a long-running data processing service. 

The service is located in a local Git repository at `/home/user/data_service`. The service is primarily written in Python (`worker.py`), but it offloads heavy processing to a C extension compiled as `libprocessor.so`. 

Recently, the service started consuming excessive memory and eventually crashing when running with multiple worker threads. The issue was introduced somewhere in the Git history, but we don't know which commit caused it.

Your task is to:
1. Use `git bisect` to identify the exact commit that introduced the memory leak. You can test for the leak by running `python3 worker.py --run-duration 3` (runs for 3 seconds) and monitoring its memory allocations or system calls. 
2. Trace the system calls (e.g., using `strace`) during a leaking run to identify the underlying allocation pattern causing the leak (e.g., repeatedly calling `mmap` without `munmap`).
3. Identify the exact C function in the source code (`processor.c`) that is leaking memory under concurrent execution. (Hint: look for a race condition or missing cleanup in the C code).

Once you have completed your investigation, create a file at `/home/user/investigation_report.json` with exactly the following JSON structure:

```json
{
  "bad_commit": "<full_40_character_git_sha>",
  "leaking_c_function": "<name_of_the_C_function>",
  "system_call_leaking": "<name_of_system_call_used_for_allocation_in_strace>"
}
```

Make sure your Git repository is left checked out at the `main` branch when you are done.