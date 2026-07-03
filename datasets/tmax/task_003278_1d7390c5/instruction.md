You are an on-call engineer and just received a PagerDuty alert at 3:00 AM. 

The legacy Geofencing service has crashed in production. The system state has been captured in a raw memory dump, and the failing calculation logic has been localized to a specific C file. 

You need to diagnose the crash data, fix the algorithmic bug, and prove the fix works.

Here is what you have on your system:
1. `/home/user/crash.dump` - A raw, binary memory dump from the crashed process. The last request processed before the crash is stored as an ASCII string within this dump, starting with the prefix `LAST_REQ: ` followed by comma-separated coordinate pairs.
2. `/home/user/haversine.c` - The source code for the distance calculation logic that caused the fault. The developer who wrote it left a bug in the formula implementation.

Your tasks:
1. **Analyze the Memory Dump:** Extract the coordinates from the `LAST_REQ: ` string in `/home/user/crash.dump`.
2. **Correct the Formula:** Inspect `/home/user/haversine.c`. There is a mathematical bug in how the Haversine formula is implemented. Fix it.
3. **Create a Minimal Reproducible Example:** Write a new C program at `/home/user/mre.c` that includes/uses the fixed `haversine.c` logic. Have it call the distance function using the exact coordinates you extracted from the memory dump.
4. **Compile and Run:** Compile your MRE. Note: You might encounter compiler/linker errors related to missing libraries; you must interpret and resolve these to successfully build the binary.
5. **Log the Output:** Run the compiled MRE and write the final calculated distance (in kilometers) to `/home/user/recovery_distance.txt`. The output should contain strictly the distance as a floating-point number, rounded to exactly two decimal places (e.g., `1234.56`).

Do not use any external dependencies other than standard C libraries.