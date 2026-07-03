You are a performance engineer tasked with debugging and deploying a two-tier mathematical microservice. The service consists of an HTTP Gateway and a raw TCP Backend. Recently, the service has been experiencing severe latency issues and timeouts, causing the system to fail its SLAs.

You have been provided with the following artifacts in the `/app` directory:
1. **`/app/config_spec.png`**: An image containing the system configuration. You must extract the required Gateway HTTP Port, Backend TCP Port, and the "Modulus Constant" from this image.
2. **`/app/gateway.py`**: The HTTP Gateway service code.
3. **`/app/backend.py`**: The TCP Backend service code.
4. **`/app/traffic.pcap`**: A packet capture demonstrating a historical successful communication between the gateway and the backend.

Your objectives are:
1. **Analyze and Configure**: Extract the port numbers and the Modulus Constant from `/app/config_spec.png`. Update the gateway and backend scripts (or write new ones in the language of your choice) to use these exact ports and the modulus.
2. **Protocol Conformance**: Analyze `/app/traffic.pcap` to understand the raw TCP protocol used between the Gateway and Backend. Ensure your backend implementation strictly adheres to this binary protocol (which involves sending and receiving little-endian 64-bit integers).
3. **Performance Debugging**: The current `backend.py` has a severe performance bottleneck causing requests to hang. Use system call tracing (`strace`), profiling, or log analysis to identify the root cause. (Hint: look for blocking I/O or entropy pool depletion). Fix the performance issue so that the backend responds in under 10 milliseconds.
4. **Deploy**: Start both the Gateway and the Backend services in the background. They must listen on `127.0.0.1` using the ports extracted from the image. 

The Gateway must expose an HTTP GET endpoint at `/compute?val=<integer>`. It should forward the value to the backend over TCP, receive the computed result, and return an HTTP 200 JSON response in the format: `{"result": <computed_value>}`. The backend computation is known to be `(val^2) % Modulus_Constant`.

Leave both services running in the background when you are finished. Do not use any authentication tokens. Ensure all required dependencies (like `tesseract-ocr` if you need it) are installed or utilized correctly.