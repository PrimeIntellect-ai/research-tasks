We are in the process of migrating a legacy data processing backend from Python 2 to Python 3. The new Python 3 backend (which will run on port 9000) is vulnerable to a specific legacy shellcode exploit embedded in some of our historical binary payloads. 

To protect the new backend during the migration, we need to place a custom reverse proxy in front of it. 

Your task is to write a reverse proxy in Go that filters out malicious payloads.

Requirements:
1. Write a Go program at `/home/user/proxy.go` and compile it to `/home/user/proxy`.
2. The proxy must listen on `127.0.0.1:8080` and forward all HTTP requests to the Python 3 backend at `http://127.0.0.1:9000`.
3. The proxy must read the incoming request body (specifically for POST requests). If the body contains a specific malicious byte sequence, the proxy must immediately return an HTTP `403 Forbidden` status code and NOT forward the request to the backend. Otherwise, it should forward the request normally.
4. We have lost the original documentation for the exact byte sequence of the exploit, but the previous lead engineer left a scan of a sticky note at `/app/malware_note.png`. You will need to extract the x86 assembly instructions written in that image and determine their compiled binary representation (opcodes/hex bytes). The proxy must search for this exact compiled byte sequence in the request body.
5. Your proxy should gracefully handle concurrent requests.

Ensure the compiled binary `/home/user/proxy` is ready to be executed by our automated end-to-end test orchestrator, which will start your proxy and send a corpus of clean and malicious payloads through it to verify correct behavior.