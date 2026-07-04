You are tasked with fixing a broken Nginx reverse proxy setup and implementing a missing backend service based on an audio instruction. 

Currently, an Nginx instance is supposed to be running using the configuration file at `/home/user/nginx.conf`. However, any requests to it result in a 502 Bad Gateway because the backend service is neither running nor implemented.

Your objectives:
1. **Understand the Backend Logic**: Listen to or transcribe the audio file located at `/app/backend_instructions.wav`. This file contains the spoken rules for how the backend logic must transform input text.
2. **Implement the Logic**: Create an executable program at `/home/user/backend_processor`. This program must read standard input, apply the exact transformation described in the audio, and print the result to standard output. You may write this in any language (e.g., Python, Bash, Perl) as long as it is executable and self-contained.
3. **Fix the Proxy and Run the Backend**: 
   - Start a simple HTTP server on port 8081 (the backend) that responds with a 200 OK. 
   - Create a process supervision script at `/home/user/supervisor.sh` that starts this backend HTTP server and restarts it automatically if it fails. Leave it running in the background.
   - Fix the provided Nginx configuration at `/home/user/nginx.conf` so that Nginx listens on port 8080 and correctly proxies requests to the backend on port 8081 without returning a 502 error. Start Nginx using this configuration.

Verify your setup by ensuring `curl http://localhost:8080` returns a successful response from your backend.

Note: Our automated verifier will strictly test the exact input-output behavior of `/home/user/backend_processor` against thousands of random inputs. It must be bit-exact to the hidden oracle implementation of the audio instructions.