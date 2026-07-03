You are a release manager preparing our latest API for deployment. The security team has left an urgent voicemail regarding a new attack pattern that must be blocked before we go live. 

Your tasks are:
1. **Analyze the Security Report**: Transcribe and analyze the audio file located at `/app/voicemail.wav`. It details a specific structural pattern in malicious JSON payloads. 
2. **Build a Standalone Detector**: Create an executable CLI program at `/home/user/detector`. It must accept a single argument: the path to a JSON file. 
   - It should parse the JSON and analyze its structure based on the rules described in the audio.
   - It must exit with code `0` if the payload is safe (clean), and exit with code `1` if it matches the malicious pattern (evil).
   - *Hint*: You may need to implement a state machine or recursive parser to properly track the structural conditions mentioned in the voicemail.
3. **Configure a Reverse Proxy**: Set up a reverse proxy listening on TCP port 8080 that routes traffic to our backend API at `http://127.0.0.1:9090`. 
   - All incoming HTTP POST requests to port 8080 will contain JSON bodies.
   - The proxy must inspect the JSON body. If the payload is malicious (as defined by the voicemail), the proxy must immediately return a `403 Forbidden` response and NOT forward the request.
   - If the payload is safe, it must forward the request to the backend and return the backend's response.
   - You may use any software (e.g., Nginx with Lua, a custom Node/Python/Go middleware, HAProxy) as long as it correctly filters the traffic.

Ensure your `/home/user/detector` is executable (`chmod +x`) and properly implements the logic. Our automated CI/CD pipeline will test your detector against a large, hidden corpus of clean and evil payloads, and will test your proxy with live traffic.