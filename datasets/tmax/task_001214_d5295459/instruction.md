A legacy log processing system in our DevOps pipeline relies on an undocumented, compiled C++ binary located at `/app/log_anomaly_detector`. This binary processes raw access logs, performs a specific data transformation to normalize the log entries, and calculates a statistical anomaly score based on the sequence of response sizes and timestamps. 

Unfortunately, we don't have the source code, and the binary was compiled stripped. Lately, it has been occasionally crashing (segfaulting) on certain malformed log lines, causing our entire log pipeline to halt. We have extracted a core dump from a recent crash, but our primary goal is to completely replace this fragile binary with a robust Python implementation.

Your task is to reverse-engineer the behavior of `/app/log_anomaly_detector` by treating it as a black box and analyzing its outputs across various synthesized log inputs. You must write a Python script at `/home/user/anomaly_detector.py` that behaves EXACTLY like the binary for any valid input.

Here is what we know about the expected behavior:
1. The binary takes a single argument: the path to a text-based log file.
   Usage: `/app/log_anomaly_detector <path_to_log_file>`
2. The input log file contains one entry per line in the format: `[TIMESTAMP] IP_ADDRESS METHOD /PATH HTTP_VERSION STATUS_CODE RESPONSE_SIZE` (e.g., `[1634567890] 192.168.1.100 GET /api/data HTTP/1.1 200 1024`).
3. The binary outputs a normalized, tab-separated version of the logs, dropping the HTTP version, followed by a final line containing a calculated anomaly score: `ANOMALY_SCORE: <float>`.

You need to figure out exactly how the anomaly score is calculated (it involves an exponentially weighted moving average or a similar statistical technique applied to the response sizes) and how the normalization handles edge cases. 

Create the script at `/home/user/anomaly_detector.py`. It should take a file path as its first positional argument and print the exact bit-for-bit equivalent output to stdout as the legacy binary would (ignoring the cases where the binary segfaults). 

Note: You can use `objdump`, `strings`, or `gdb` on the binary if it helps, but black-box fuzzing and diff analysis of the outputs is highly recommended.