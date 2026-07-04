You are an operations engineer triaging a critical incident. Our containerized real-time event processing microservice has suddenly started crash-looping in production. The CI/CD pipeline is also currently failing to build the emergency hotfix branch. 

Your objective is to fix the build, diagnose the crash, patch the code, write a regression test, and successfully process the backlogged events.

Workspace: `/home/user/event_service/`

**Phase 1: Build Failure Diagnosis**
Navigate to the workspace and attempt to compile the project using `make`. You will notice it fails. Diagnose the compilation/linking errors. Modify the `Makefile` and/or C++ source files to successfully compile the `event_processor` binary.

**Phase 2: Core Dump / Crash Analysis**
Once compiled, run the service against the backlogged events: `./event_processor backlog.txt`. The application will crash (Segmentation fault). 
Use interactive debugging tools (`gdb`) or code inspection to determine the root cause of the crash within the `EventProcessor::add_event` method in `src/processor.cpp`.

**Phase 3: Algorithmic Fix**
Fix the bug in `src/processor.cpp`. The application maintains a rolling window of recent event metrics using a fixed-size ring buffer. The bug is algorithmic, related to how array indices are calculated when dealing with certain types of event IDs present in `backlog.txt`. Make sure the logic correctly wraps around the 10-element buffer for *all* valid integer IDs without going out of bounds.

**Phase 4: Regression Test Construction**
Create a new C++ file `/home/user/event_service/src/test_regression.cpp`. 
Write a simple `main` function that:
1. Instantiates `EventProcessor`.
2. Feeds it an event that explicitly triggers the previous crash condition.
3. Exits with code `0` if successful, or code `1` if it fails/crashes.
Add a `test` target to the `Makefile` that compiles this file into a binary named `test_runner` and executes it.

**Phase 5: Final Execution**
Rebuild the main application and run it against `backlog.txt`. 
The program is designed to output a final summary line. Save this exact final summary output to `/home/user/final_state.txt`.

Ensure:
- The project builds cleanly with `make`.
- `make test` successfully compiles and runs your regression test.
- `/home/user/final_state.txt` contains the correct final output string.