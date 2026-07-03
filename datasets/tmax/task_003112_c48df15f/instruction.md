You are an on-call engineer who just received a 3 AM PagerDuty alert. The internal payment gateway service crashed completely. To make matters worse, a rogue cleanup script deleted the service's log file right after the crash. 

You have two pieces of evidence left on your debugging workstation:
1. `/home/user/capture.pcap`: A network packet capture containing traffic to the service just before it crashed.
2. `/home/user/storage.img`: A raw ext4 filesystem image file that was attached to the container. The deleted log file (`gateway.log`) resided in the root of this filesystem.

Your task is to identify the root cause of the crash by doing the following:
1. **Analyze the Packet Capture:** Inspect `/home/user/capture.pcap` to find the source IP address that made an HTTP GET request to the specific endpoint `/api/v1/explode`.
2. **Recover the Deleted Log:** The file `gateway.log` was deleted from `/home/user/storage.img`. Recover its contents. (Hint: Since you do not have `sudo` privileges to mount the image, use the `sleuthkit` suite of tools, such as `fls` and `icat`, to extract the deleted file).
3. **Analyze the Traceback:** Find the log entry and stack trace in the recovered `gateway.log` that was triggered by the source IP address you found in step 1.
4. **Report:** Create a file at `/home/user/incident_report.txt` containing exactly two lines:
   - Line 1: The malicious IP address.
   - Line 2: The exact Python Exception type (e.g., `ValueError`, `KeyError`, `IndexError`) that was thrown in the traceback associated with that specific request.

Make sure the final file strictly follows the formatting above for automated verification.