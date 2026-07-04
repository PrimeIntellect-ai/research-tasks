You are a Site Reliability Engineer (SRE) investigating an issue with an internal uptime monitoring service. The monitoring script, located at `/home/user/app/monitor.py`, has been crashing intermittently with a Segmentation Fault when attempting to monitor certain URLs.

The script relies on a pre-compiled shared library, `/home/user/app/libuptime.so`, to perform rapid network checks. 

Your task is to:
1. Analyze the shared library and the Python script to determine the root cause of the segmentation fault. Use an interactive debugger or reverse engineering tools as needed.
2. Determine the maximum safe string length (number of characters) for the `hostname` parameter that can be passed to the `check_uptime` function in `libuptime.so` without corrupting memory.
3. Write this exact integer value to a file at `/home/user/app/limit.txt`.
4. Modify `/home/user/app/monitor.py` so that the `monitor_host(hostname)` function safely truncates any `hostname` string to this maximum safe length before passing it to the C library. The function must still return the integer status code from the library.
5. Create a regression test file at `/home/user/app/test_monitor.py` using Python's built-in `unittest` framework. The test must import `monitor_host` from `monitor.py` and verify that calling `monitor_host("super_long_hostname_that_would_normally_crash_the_service.internal.com")` does not crash and returns a status code of `200`.

Requirements:
- Do not modify the shared library (`libuptime.so`). You must implement the fix in Python.
- Provide the regression test exactly at `/home/user/app/test_monitor.py`.
- Ensure your changes in `monitor.py` are robust.