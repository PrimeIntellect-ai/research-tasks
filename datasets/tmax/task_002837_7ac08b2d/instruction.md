You are a forensics analyst investigating a compromised host. The attacker has been forging authentication tokens to gain administrative privileges on a microservice architecture. You have been provided with forensic artifacts and need to build a security filter to stop the attack.

Your environment contains the following:
1. `/home/user/forensics/proc_dump/`: A directory simulating a snapshot of the `/proc` filesystem at the time of the attack.
2. `/home/user/app/`: The application directory containing a Flask backend running on port 5000, and an Nginx reverse proxy configuration at `/home/user/app/nginx.conf`.
3. `/home/user/corpus/`: A directory containing intercepted authentication tokens.
   - `/home/user/corpus/clean/tokens.txt`: A list of legitimate base64-encoded tokens.
   - `/home/user/corpus/evil/tokens.txt`: A list of malicious base64-encoded tokens used by the attacker.

### Step 1: Token Cryptanalysis
The authentication system uses a custom token generation scheme. Legitimate tokens are JSON objects containing `user`, `role`, and `exp` claims. The application encodes these JSON strings using a repeating-key XOR cipher, followed by Base64 encoding. 
The secret XOR key was inadvertently leaked via command-line arguments to a background worker process. You must analyze the `proc_dump` to recover this secret key.

### Step 2: Build an Offline Classifier
Using the recovered key, write a Python script at `/home/user/classifier.py` that can distinguish between legitimate and forged tokens. 
Legitimate tokens always have the role `"user"`. The attacker has forged tokens with the role `"admin"`.
Your script must accept two command-line arguments: an input file path and an output file path.
`python3 /home/user/classifier.py <input_file> <output_file>`

The input file will contain one base64-encoded token per line. Your script must process each token, decrypt it, and write either the exact word `CLEAN` or `EVIL` to the output file (one classification per line, corresponding to the input lines).

### Step 3: Secure the Microservice (Multi-Service Compose)
The application stack currently allows direct access. You must implement a real-time defense.
1. Write a Python HTTP server (e.g., using Flask) at `/home/user/auth_service.py` that listens on port `8080`.
2. This service should inspect the `auth_token` cookie of incoming requests.
3. If the token is valid and `CLEAN`, the service must return a `200 OK` HTTP status.
4. If the token is missing, invalid, or `EVIL`, the service must return a `401 Unauthorized` HTTP status.
5. Modify the Nginx configuration at `/home/user/app/nginx.conf` to use the `auth_request` directive. Nginx (listening on port 8000) should forward authentication checks to your new service on port 8080 before proxying requests to the backend API on port 5000.
6. Start all services (Backend Flask, your Auth Service, and Nginx).

Ensure your `classifier.py` perfectly classifies the provided corpora, and your end-to-end Nginx setup correctly blocks malicious cookies while allowing clean ones.