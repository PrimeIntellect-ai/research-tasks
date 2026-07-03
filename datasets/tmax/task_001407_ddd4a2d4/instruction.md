I need your help fixing a local audio processing pipeline that is failing to start. 

We have a systemd user service intended to process an incoming audio file, compute its Root Mean Square (RMS) amplitude, and write the output, but the whole pipeline is broken.

Here is what you need to do:
1. **Directory Structure & Symlinks:** 
   - Create the directories `/home/user/inbox` and `/home/user/outbox`.
   - Create a symbolic link from `/app/input.wav` (an existing 16-bit PCM Mono WAV file) to `/home/user/inbox/target.wav`.

2. **C++ Audio Analyzer:**
   - I started writing a C++ program at `/home/user/analyzer.cpp` but it's incomplete. 
   - Complete the C++ program so that it reads a 16-bit PCM Mono WAV file (passed as the first command-line argument). It should skip the 44-byte WAV header, read the remaining raw audio data (as signed 16-bit integers), calculate the Root Mean Square (RMS) amplitude of the audio samples, and write the float value (formatted to 2 decimal places) to a file specified by the second command-line argument.
   - Compile this program to `/home/user/bin/analyzer` (create the `bin` directory).

3. **Service Management:**
   - Create a systemd user service file at `/home/user/.config/systemd/user/audio-analyzer.service`.
   - The service must execute your compiled `analyzer` binary, taking `/home/user/inbox/target.wav` as input and writing the result to `/home/user/outbox/rms.txt`.
   - Ensure the service starts successfully and stays in a completed/successful state.
   - Write a shell script at `/home/user/health_check.sh` that uses `systemctl --user status audio-analyzer.service`, extracts the `Active:` line using `grep` and `awk`, and appends it to `/home/user/health.log`. Run the script once.

Please implement the C++, build the binary, set up the directories, configure the systemd service, and ensure the final RMS value is accurately written to `/home/user/outbox/rms.txt`.