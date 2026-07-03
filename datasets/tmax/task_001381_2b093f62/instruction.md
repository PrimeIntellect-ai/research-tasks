You are a backup operator tasked with restoring a corrupted audio recording retrieved from an old server archive. The retrieved audio file is located at `/app/noisy_backup.wav`. It contains a lot of high-frequency white noise that was introduced during a faulty tape backup process.

Your objective is to build a C++ restoration utility that filters this noise, configure the system to securely process it, and schedule the restoration job.

Perform the following steps:

1. **Write the C++ Restoration Tool**:
   Create a C++ program at `/home/user/restore.cpp` that reads a 16-bit PCM WAV file and applies a simple Moving Average Filter to the audio samples. 
   - The program must parse a configuration file at `/home/user/filter_config.ini` to read the window size for the moving average. The config file should have the format `window_size=X` (you will need to determine a good value for X, typically between 3 and 15, to remove the noise without overly muffling the audio).
   - The program should take the input file and output file paths as command-line arguments.
   - Compile this program to an executable named `/home/user/restore_bin`.

2. **Network/Port Forwarding Simulation**:
   The backup daemon configuration requires a secure local tunnel. Use `socat` to create a local port forward from `tcp-listen:9090,bind=127.0.0.1` to `tcp:127.0.0.1:8000`. Run this in the background. (This simulates a secure tunnel required by our legacy tape backup verification tools).

3. **Scheduled Task**:
   Create a shell script at `/home/user/run_restore.sh` that:
   - Checks if the local tunnel on port 9090 is open (e.g., using `nc` or `curl`).
   - If it is, executes `/home/user/restore_bin /app/noisy_backup.wav /home/user/final_restored.wav`.
   Set up a user cron job to run this script every minute.

Wait for the cron job to execute and generate `/home/user/final_restored.wav`. 

To succeed, your filtered audio file (`/home/user/final_restored.wav`) must closely match the original clean audio. An automated verifier will calculate the Mean Squared Error (MSE) between your output and the hidden clean reference. The MSE must be below the required threshold.