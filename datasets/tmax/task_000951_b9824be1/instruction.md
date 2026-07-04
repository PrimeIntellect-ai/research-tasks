**Ticket ID:** INC-88392
**Assignee:** IT Support / Systems Agent
**Subject:** Log aggregator crashes on filenames with spaces and times out on query

**Description:**
We have a multi-service logging pipeline that reconstructs event timelines across our fleet. Recently, some server hostnames were changed to include spaces (e.g., "web server 01"), which causes the log aggregator to fail to read the files. Furthermore, even when it does read files successfully, the query service times out because the log aggregator is extremely slow at sorting and converging the timeline for large log volumes. 

The pipeline is located in `/app/` and consists of three cooperating services:
1. **Generator:** A background Bash script that simulates log generation across multiple files.
2. **Aggregator:** A C-based TCP service (`/app/aggregator/aggregator.c`) running on port 8080. It reads log files, merges them chronologically, and returns the unified timeline.
3. **Query API:** A Python Flask service (`/app/query/api.py`) running on port 5000 that queries the aggregator.

**Your objectives:**
1. **Resolve the Space Issue:** The C aggregator currently parses configuration files or directories poorly, breaking when log filenames contain spaces. Fix the C code in `/app/aggregator/aggregator.c` so it can cleanly open and read these files.
2. **Resolve the Convergence / Performance Bug:** The aggregator uses an inefficient sorting algorithm to reconstruct the timeline, causing severe performance degradation. Replace it with an efficient algorithmic approach (e.g., standard library `qsort` or similar) so it handles large datasets quickly.
3. **Dependency Check:** Make sure the C aggregator correctly links against the local `libjson-c` version. You may need to fix its `Makefile` if there are conflicting library paths.
4. **Integration & Re-deployment:** Recompile the C aggregator and ensure all three services can be started and run together. 

**Verification:**
Once you have fixed the code, start all services using the provided `/app/start_services.sh` script. 
We will run an automated test that hits the Query API (port 5000) requesting the merged timeline of 100,000 log lines. 
Your fixed implementation must complete the request and return the correctly sorted JSON payload with a maximum latency of **0.5 seconds**. The default broken implementation takes over 15 seconds (if it doesn't crash first).

**Deliverables:**
Modify `/app/aggregator/aggregator.c` and `/app/aggregator/Makefile` as needed. Run `/app/start_services.sh` and leave the services running in the background when you are finished.