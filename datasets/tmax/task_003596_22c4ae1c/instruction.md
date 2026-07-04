You are an incident response engineer investigating a memory leak that caused a long-running background service to crash with an Out-Of-Memory (OOM) error. 

The service is driven by a Bash script located at `/home/user/log_processor.sh`. A partial process memory dump was captured just before the crash and is available at `/home/user/service_mem.dump`.

Your objectives are:

1. **Memory Dump Analysis**: 
   Analyze the binary dump file `/home/user/service_mem.dump`. Identify the specific log string that was leaked and duplicated thousands of times in memory, exhausting the system RAM. The leaked payload always starts with a session ID in brackets (e.g., `[SESSION_...]`). Extract this exact, unique malformed string and save it to `/home/user/leaked_payload.txt` (just the string itself, one line, no extra whitespace).

2. **Root Cause Analysis & Recursion Fixing**:
   Review `/home/user/log_processor.sh`. You will find a text processing function that handles incoming messages. It has a critical bug: when it receives a specific type of malformed message (similar to the one you found in the dump), it falls into infinite recursion, appending to a global array until memory is exhausted.
   Modify `/home/user/log_processor.sh` to fix this infinite recursion. If a message is malformed (missing its closing tags), the function should simply echo "Malformed message" and return 1, without recursing or accumulating state.

3. **Data Transformation Diff**:
   Once you have fixed `/home/user/log_processor.sh`, generate a unified diff patch between the original buggy script and your fixed version. Save this patch to `/home/user/processor.patch`.

Ensure your fixed script behaves correctly. If we run `/home/user/log_processor.sh "<the_leaked_payload>"`, it should safely terminate in under 1 second rather than hanging indefinitely.