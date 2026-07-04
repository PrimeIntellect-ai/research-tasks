You are acting as a performance engineer investigating a recent crash of our internal Python analytics service. The service crashed under heavy load and produced a core dump. We need to identify the exact malicious payload that caused the crash.

You have been provided with the following files:
- `/home/user/logs/service_a.log`: Logs from the API router.
- `/home/user/logs/service_b.log`: Logs from the data processor.
- `/home/user/dump.core`: The memory dump generated at the time of the crash.

Your tasks are:
1. Reconstruct the timeline of events immediately preceding the crash. The final crash is recorded in `service_a.log` with the message "Segmentation fault (core dumped)". You need to find the precise timestamp of this crash.
2. Identify the `ReqID` (Request ID) that was being processed right before the crash. You will need to chronologically interleave the two log files to find the last `ReqID` mentioned across any service before the crash timestamp.
3. Extract the malicious payload from the core dump. The memory dump contains the string `PAYLOAD_<alphanumeric_string>` located close to the final `ReqID`. Extract this precise payload string.

Once you have identified these three pieces of information, write them to `/home/user/report.txt` in the following exact format:

Crash Time: <YYYY-MM-DDTHH:MM:SS>
Request ID: <ReqID>
Payload: <PAYLOAD_...>

Use standard shell utilities (like `sort`, `grep`, `strings`, `awk`) to complete this task.