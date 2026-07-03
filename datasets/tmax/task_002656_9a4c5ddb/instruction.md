I am trying to set up a local audio processing API, but I'm running into configuration issues. I have an Nginx configuration file at `/home/user/nginx.conf` that is supposed to listen on port 8080 and route requests to a Go backend service via a Unix socket. However, right now, requesting `http://127.0.0.1:8080/decode` returns a 502 Bad Gateway because the upstream socket path is misconfigured.

Your objectives:
1. Fix the Nginx configuration at `/home/user/nginx.conf` so that it correctly proxies requests to the Unix socket located at `/tmp/dtmf.sock`.
2. Write a Go web service in `/home/user/server.go` that listens on the Unix socket `/tmp/dtmf.sock`.
3. When the Go service receives a `GET /decode` request, it must analyze the provided audio file at `/app/signal.wav` to extract the sequence of DTMF (Dual-tone multi-frequency) tones present in the audio. 
4. The Go service should return the decoded DTMF digits as a plain text string (e.g., `15551234567`). You may install and invoke external tools (like `multimon-ng`) from your Go code to perform the decoding.
5. Create a simple bash script at `/home/user/start.sh` that compiles the Go service, starts it in the background, and starts Nginx in the background using the corrected configuration file. Ensure the script manages environment variables and starts Nginx as the current user (e.g., `nginx -c /home/user/nginx.conf -g "pid /home/user/nginx.pid;"`).

Run your `start.sh` script so that the API is fully operational. I will test the system by sending a GET request to `http://127.0.0.1:8080/decode` and evaluating the accuracy of the decoded DTMF sequence.