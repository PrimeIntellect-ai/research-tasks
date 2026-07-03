You are a deployment engineer rolling out a new update for an internal monitoring system. As part of this update, the audible alert system needs to be reconfigured. The current raw alert audio is too loud, and the new configuration requires serving a dampened version of the alert over an internal HTTP endpoint with specific port forwarding.

Your tasks are as follows:

1. **Process the Audio in C**: 
   There is a raw alert audio file located at `/app/alert_raw.wav` (standard RIFF/WAV format, 16-bit signed PCM, Mono, 16000 Hz).
   Write a C program that reads this file, reduces the volume of the audio by exactly 50% (divide each 16-bit sample value by 2, rounding towards zero), and writes the result to `/home/user/alert_quiet.wav`. Make sure to copy the 44-byte WAV header exactly as it is from the input file to the output file before processing the samples.

2. **Web Server Setup**:
   Write a simple C program that acts as an HTTP web server listening on `127.0.0.1:8080`. It should accept incoming HTTP GET requests and serve the `/home/user/alert_quiet.wav` file. The server must return a basic `200 OK` HTTP response with the correct `Content-Length` and `Content-Type: audio/wav`, followed by the binary file content. Run this server in the background.

3. **Port Forwarding Configuration**:
   The internal application expects the alert to be available on port `9090`. Since you do not have root privileges to use `iptables`, use `socat` to set up a port forward that listens on TCP port `9090` and forwards all traffic to your C web server on port `8080`. Run this `socat` process in the background.

Ensure your C web server and the `socat` tunnel are actively running and serving the correct file at `http://127.0.0.1:9090/alert_quiet.wav` when you finish.