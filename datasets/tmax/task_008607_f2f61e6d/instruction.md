It is 3:00 AM and you have just been paged. The new C-based `log_ingestor` service is repeatedly crashing in production when processing certain binary log files, causing a complete halt in our telemetry pipeline. 

You have been granted access to the production debugging environment. 
In `/home/user/` you will find:
- `log_ingestor.c`: The source code for the log ingestor.
- `crash.bin`: A captured log file that reliably causes the ingestor to crash (Segmentation fault).
- `data.bin`: A normal log file for testing.

Your tasks are:
1. **Delta Debugging**: Isolate the exact minimal byte sequence from `crash.bin` that triggers the segmentation fault in the original `log_ingestor.c`. Save this exact minimal binary sequence to `/home/user/minimized.bin`. The file must be a valid standalone record (or records) according to the format, but as small as possible while still causing the crash.
2. **Format Parsing Edge-Case Repair**: Analyze `log_ingestor.c` to understand the root cause of the crash. Fix the bug in the C code. In the vulnerable parsing section, if the decoded output length would exceed the buffer size, you must cap the count so that it exactly fills but does not overflow the buffer (e.g., truncate the run-length expansion to fit the available space).
3. **Save Fixed Code**: Save your corrected source code to `/home/user/log_ingestor_fixed.c` and compile it to `/home/user/log_ingestor_fixed`.
4. **Data Transformation Verification**: Run your fixed binary on `data.bin` and save the output to `/home/user/data_fixed.bin`. 

The system relies on you to restore the pipeline. Ensure your fix correctly handles the edge cases without corrupting normal data transformations.