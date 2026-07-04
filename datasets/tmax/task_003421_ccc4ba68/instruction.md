You are acting as a security researcher analyzing an intercepted Command and Control (C2) infrastructure simulator. We have recovered the source code for the simulator, located in `/app/c2_sim/`. 

The system is a multi-service architecture composed of:
1. A Frontend Gateway (`/app/c2_sim/gateway.py`): A Python HTTP server designed to listen on `127.0.0.1:8080`. It receives intercepted binary payloads.
2. A Backend Crypto Node (`/app/c2_sim/crypto_node.py`): A Python TCP daemon designed to listen on `127.0.0.1:8081`. It performs a custom Proof-of-Work (PoW) convergence algorithm to generate cryptographic signatures for the payloads.

**The Problem:**
We are trying to replicate the C2 server's behavior to analyze a specific class of payloads, but our simulator is broken. When we send a high-entropy binary payload to the Gateway, it times out. 
1. The `crypto_node.py` backend seems to be failing to converge on a valid signature for certain inputs. We suspect there is a signed integer overflow bug occurring during the binary unpacking phase (similar to x86 signedness bugs), which pollutes the state of the convergence algorithm.
2. The exception handling in `crypto_node.py` is poorly written, swallowing tracebacks and making standard logging useless.
3. The `gateway.py` might be misconfigured and not properly communicating with the backend socket.

**Your Objectives:**
1. Start the multi-service system using `/app/c2_sim/start.sh`.
2. Use interactive debugging (e.g., `pdb`) and logging analysis to trace the execution flow inside `crypto_node.py`. Identify where the payload unpacking produces negative integers instead of the expected 32-bit unsigned integers.
3. Fix the unpacking logic in `crypto_node.py` to use unsigned integers so the convergence algorithm completes successfully.
4. Fix any configuration/wiring issues in `gateway.py` so it properly routes requests to the TCP backend on port 8081.
5. Ensure both services remain running in the background and correctly process requests.

Once you are done, the frontend must listen on `127.0.0.1:8080` (HTTP) and the backend on `127.0.0.1:8081` (TCP raw). When an automated verification script POSTs a 16-byte binary payload to `http://127.0.0.1:8080/analyze`, it should receive a 200 OK with a JSON response containing `{"status": "success", "signature": "<calculated_integer>"}`.