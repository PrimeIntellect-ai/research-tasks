You are a system administrator tasked with automating a network health evaluator for your servers. 

The senior network engineer left a voicemail containing the logic for our new custom health evaluation algorithm, but they are currently on a flight and unreachable. You need to decode the voicemail, implement the logic, and set up an idempotent deployment script.

**Step 1: Decode the Algorithm**
An audio file containing the voicemail is located at `/app/net_instructions.wav`. You must transcribe and understand the health check logic described in it.

**Step 2: Implement the Health Evaluator**
Write a Python script at `/home/user/health_eval.py` that implements the exact algorithm described in the voicemail. 
- The script must accept exactly two positional command-line arguments:
  1. `ipv4_address` (string, e.g., `192.168.1.5`)
  2. `latency` (integer in milliseconds, e.g., `150`)
- The script must strictly print only the final evaluation result (as specified in the audio) to standard output. Do not print any additional debug text.

**Step 3: Idempotent Deployment Script**
Write an idempotent Bash script at `/home/user/deploy_health_check.sh` that performs the following setup operations without requiring root access:
1. Creates the directory `/home/user/health_checks/bin/` if it does not already exist.
2. Copies `/home/user/health_eval.py` into `/home/user/health_checks/bin/`.
3. Makes the copied script executable (`chmod 755`).
4. Adds a cron job for the current user (`user`) that runs `/home/user/health_checks/bin/health_eval.py 10.0.0.1 500` exactly every 5 minutes (`*/5 * * * *`).
*Crucial:* Your bash script must be strictly idempotent. If ran multiple times, it must not duplicate the cron job entry or fail.

Your Python script's logic will be rigorously verified. An automated tester will fuzz your script with thousands of random IP and latency inputs, comparing its standard output bit-for-bit against a compiled oracle of the engineer's exact algorithm.