You are an on-call engineer responding to a 3:00 AM PagerDuty alert. The core telemetry parsing service, `telemd`, is repeatedly crashing with a Segmentation Fault (specifically, a Stack Overflow) under high load.

The source code for the service is located in `/home/user/telemd`.

Initial forensic analysis suggests that under heavy concurrent load, the linked list used to track incoming events is becoming corrupted (creating a cycle). Later, a worker thread attempts to recursively process the list and falls into an infinite recursion, exhausting the stack and crashing the service.

Your task:
1. Navigate to `/home/user/telemd`.
2. Analyze `queue.c` and `worker.c` to understand the codebase.
3. Identify the race condition in the event queue insertion logic that allows the list corruption.
4. Identify the recursive loop termination issue in the event processing logic.
5. Fix the C code to resolve both the concurrency race condition AND make the recursive processing robust against infinite loops (e.g., by adding a recursion depth limit of 1000, or tracking visited nodes, or replacing it with an iterative approach—whatever securely prevents the stack overflow).
6. Recompile the service using the provided `Makefile` (`make clean && make`).
7. Run the provided test suite `/home/user/telemd/test_telemd.sh`.
8. Once the tests pass successfully, create a log file at `/home/user/resolution.log` containing the exact text `SYSTEM_RESTORED_SUCCESS`.

Constraints:
- Do not modify the `Makefile` or `test_telemd.sh`.
- The entrypoint for the application is `main.c`, which you should not need to modify.
- You must use standard C libraries.