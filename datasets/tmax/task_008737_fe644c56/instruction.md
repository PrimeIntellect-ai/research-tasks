You are an SRE monitoring a critical SLA pipeline. The uptime calculation system crashed last night during the Daylight Saving Time (DST) fallback transition. Your monitoring dashboards showed anomalous uptime drops right before the crash.

You need to investigate and fix the system located in `/home/user/uptime_monitor`.

Here is what you must do:

1. **Memory Dump Analysis & String Extraction:** 
   The crashed process left behind a binary dump at `/home/user/uptime_monitor/crash_dump.bin`. You must extract the last processed timestamp from this file. The timestamp is stored as a string in the format `LAST_PROCESSED_TS: YYYY-MM-DD HH:MM:SS`. Write this exact extracted string (just the date and time, e.g., `2023-11-05 01:23:45`) to a file named `/home/user/uptime_monitor/recovered_ts.txt`.

2. **Fix `monitor.py` (Timezone & Precision Bugs):**
   The script `/home/user/uptime_monitor/monitor.py` reads a start time, an end time, and a list of small downtime fractions (in seconds) to calculate the SLA uptime percentage. 
   - **Timezone Bug:** The input strings are in the `US/Eastern` timezone. During the DST fallback (e.g., Nov 5, 2023), the naive datetime subtraction currently in the code incorrectly calculates the total interval duration (wall-clock time vs. actual elapsed time). You must fix `calculate_uptime` to correctly account for the `US/Eastern` timezone and DST transitions so the total elapsed seconds are accurate.
   - **Floating-Point Precision:** The downtimes are extremely small floating-point numbers. The current naive summation `+=` loses precision, causing false SLA alerts. Fix the logic to use robust floating-point summation.

3. **Regression Test Construction:**
   Create a regression test suite at `/home/user/uptime_monitor/test_monitor.py` using `pytest`. Write at least two tests:
   - One verifying the exact DST fallback elapsed time behavior (e.g., crossing 1 AM to 2 AM on the fallback day should equal 7200 seconds of elapsed time, not 3600).
   - One verifying that the sum of ten million `0.0000001` second downtimes equals exactly `1.0` second.

4. **Run the Pipeline & Export Report:**
   After fixing the code, run the provided script `generate_report.py` which imports your fixed `calculate_uptime` function. It will process `/home/user/uptime_monitor/events.json` and generate `/home/user/uptime_monitor/report.json`.

Ensure your fixes are applied directly to `/home/user/uptime_monitor/monitor.py`. The automated verification suite will check `recovered_ts.txt`, run your `test_monitor.py` via `pytest`, and validate the floating point and timezone correctness in `report.json`.