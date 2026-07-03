You are a deployment engineer tasked with rolling out a new automated health check and routing failover system. 

The lead network architect left a voicemail with the precise business logic required for the new deployment, but unfortunately, they did not document it anywhere else. 

Your tasks are:
1. Transcribe the audio file located at `/app/architect_notes.wav` to recover the business logic. You may install and use any transcription tools (like Python's `speech_recognition` module, `ffmpeg`, or `whisper`) in your user environment to extract the text.
2. Based on the rules described in the audio, write a robust Bash script at `/home/user/health_eval.sh`.
3. The script must take exactly three arguments representing a health check metric:
   - Argument 1: Interface name (e.g., `eth0`, `vpn0`, `ens33`)
   - Argument 2: Link status (either `UP` or `DOWN`)
   - Argument 3: Latency in milliseconds (integer, e.g., `45`, `0`, `120`)
4. The script must output a single word to `stdout` (`IGNORE`, `ERROR`, `FAILOVER`, or `OK`) based *exactly* on the rules laid out in the audio recording, followed by a newline.
5. Your script must be robust, handling unexpected inputs gracefully by defaulting to `ERROR` if the input format is fundamentally invalid (e.g., missing arguments).

An automated testing suite will fuzz your script with thousands of simulated network interface states and compare its output bit-for-bit against an authoritative oracle binary. Ensure your script implements the logic perfectly. Make sure the script is executable (`chmod +x /home/user/health_eval.sh`).