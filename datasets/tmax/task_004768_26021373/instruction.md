You are an engineer tasked with investigating a critical issue in a long-running mathematical service. The system resides in `/app/` and consists of three components:
1. A Redis message broker.
2. A FastAPI web service (`/app/api.py`) that accepts jobs and pushes them to Redis.
3. A background Python worker (`/app/worker.py`) that pops jobs, performs a complex recurrence relation calculation, and stores the results back.

Currently, the system is failing in several ways:
1. **Service Disconnect:** The startup script `/app/start.sh` fails to properly wire the services together. The worker cannot connect to Redis, and the API throws 500 errors. You need to configure the environment variables properly so the end-to-end flow works.
2. **Memory Leak:** When the worker runs continuously, it rapidly consumes memory and is eventually killed by the OOM killer. You must identify and fix this memory leak in `worker.py`.
3. **Mathematical Errors (Overflow & Boundary):** The recurrence relation in `worker.py` produces incorrect results for inputs. There is an off-by-one error in the loop boundary. Furthermore, the algorithm was originally designed for a 32-bit system, but a recent refactor introduced an incorrect bitwise operation that improperly handles signed 32-bit integer overflow bounds. 
4. **Missing Configuration:** A crucial cryptographic coefficient used in the recurrence relation was accidentally hardcoded to `0` in a recent commit. You will need to dig through the Git history in `/app/` to recover the correct hex value and restore it.

**Your Objectives:**
1. Debug and fix the multi-service setup so that running `/app/start.sh` successfully brings up all services, and submitting a job via `curl -X POST http://127.0.0.1:8000/compute -d '{"value": 100}'` returns the correct result.
2. Fix the memory leak, the boundary condition, and the integer overflow bug in `worker.py`.
3. Extract the core mathematical function from your fixed `worker.py` and create a standalone command-line script at `/home/user/fixed_math.py`. 
   - This script must accept a single integer argument (the sequence index) and print ONLY the resulting integer to standard output.
   - Example: `python3 /home/user/fixed_math.py 10` should output `1452` (hypothetical).

An obfuscated, compiled reference oracle is available at `/app/oracle`. Your standalone script's output must be bit-exact equivalent to the oracle's output for any integer input between 0 and 100,000. 

Please take your time to investigate the logs, read the git history, and carefully test your standalone script against the oracle before finalizing your solution.