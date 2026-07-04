You are a Site Reliability Engineer responding to an alert. The uptime monitoring system reports that our text processing API stack is returning 502 Bad Gateway errors.

The stack is managed via Docker Compose in `/home/user/app/`. It consists of two services:
1. `gateway`: An Nginx reverse proxy listening on `127.0.0.1:8080`.
2. `processor`: A backend Python service that receives POST requests, uppercases the provided string, and appends `_ACK`.

Your objectives:
1. **Fix the network misconfiguration:** The services are currently isolated on different Docker networks (`front-tier` vs `back-tier`) in `/home/user/app/docker-compose.yml`. Modify the Compose file so the `gateway` can successfully route requests to the `processor` service (which Nginx expects to reach at `http://processor:5000`). Apply your changes so the stack is running correctly.
2. **Create a monitoring client:** Write a Bash script at `/home/user/client.sh` that tests the end-to-end flow. 
   - The script must take exactly one argument: a string payload.
   - It must send an HTTP POST request to `http://127.0.0.1:8080/process`.
   - The request must have the `Content-Type: application/json` header and a JSON body formatted exactly as: `{"data": "<the_argument_string>"}`
   - The backend will return a JSON response in the format: `{"status": "ok", "result": "OUTPUT_STRING"}`
   - Your script must parse this JSON response using standard Bash text processing tools (like `grep`, `sed`, or `awk`) and print **only** the value of `OUTPUT_STRING` to standard output. Do not print any other text.

Ensure your `client.sh` is executable. 

Example expected behavior of your script after the network is fixed:
```bash
$ ./client.sh "hello"
HELLO_ACK
```