You are a cloud architect migrating a legacy Interactive Voice Response (IVR) system to a new microservices architecture. The old system leaves behind unnormalized, low-volume audio prompts. Before fully migrating, you must build an ingestion and processing pipeline that normalizes the legacy audio, sets up a local health-check endpoint, and routes traffic using port forwarding.

Perform the following tasks:

1. **Audio Normalization (Python):**
   Write a Python script at `/home/user/normalize.py` that takes two arguments: an input WAV file path and an output WAV file path.
   - The script must read the input 16-bit PCM mono WAV file.
   - It must scale the audio samples so that the absolute maximum peak amplitude is exactly `26214` (which represents approximately 80% of the maximum possible value for a 16-bit signed integer).
   - The output must be saved as a standard 16-bit PCM WAV file.
   - Run your script on the legacy audio fixture located at `/app/ivr_greeting.wav` and save the result to `/home/user/processed_greeting.wav`.

2. **Health Check Service:**
   Write a simple HTTP server in Python at `/home/user/health_service.py` that listens on `127.0.0.1` port `9090`.
   - When a GET request is made to `/health`, it should respond with HTTP 200 and the plain text `MIGRATION_READY`.
   - Run this service in the background.

3. **Port Forwarding:**
   The legacy routing layer is hardcoded to ping port `8080`. Using a user-space tool like `socat`, set up a port forward so that any TCP traffic directed to `127.0.0.1:8080` is forwarded to your health service on `127.0.0.1:9090`. Run this in the background as well.

4. **Integration Verification:**
   Create a bash script at `/home/user/verify.sh` that uses `curl` to fetch `http://127.0.0.1:8080/health` and writes the output to `/home/user/health_status.log`. Run this script once so the log file is generated.

Your success will be evaluated based on the functional state of the port forward and the precise mathematical accuracy of your audio normalization (verified by a Mean Squared Error metric against a ground-truth scaled audio file).