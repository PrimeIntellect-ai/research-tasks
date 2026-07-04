You are tasked with building a custom C++ Kubernetes pseudo-operator that dynamically scales deployments based on an audio feed of network sonar data. The system consists of an API endpoint, an SSH tunnel, a bash automation script, and a highly accurate C++ audio processing core.

Your final goal is to process the provided audio file, compute the specific load metrics, generate rolling deployment scaling numbers, and submit them to a mock API server.

**Step 1: Environment Setup & SSH Tunneling**
1. Create a script `/home/user/start_api.sh` that starts a mock Kubernetes API server. This server should simply be a Python HTTP server running on port `8080` in the background.
2. Establish a local SSH tunnel forwarding port `9090` to `localhost:8080`. Your operator will send payloads to `9090`. 

**Step 2: C++ Audio Operator Implementation**
You have been provided an uncompressed 16-bit PCM WAV file at `/app/sonar_data.wav` (Mono, 44100 Hz).
Write a C++ program at `/home/user/operator.cpp` that reads the WAV file and processes it in sequential chunks of exactly `4410` samples (0.1 seconds per chunk).

For each chunk, your C++ program must:
1. Parse the WAV header correctly to locate the raw PCM data.
2. Calculate the Root Mean Square (RMS) of the 16-bit integer samples in the chunk. The RMS should be calculated using double-precision floats.
3. Calculate the target replica count using the formula: `Replicas = max(1, integer_part(RMS / 500))`
4. Append the precise floating-point RMS value and the target Replica count to a file `/home/user/scaling_plan.txt` in the format: `Chunk_ID,RMS,Replicas` (e.g., `0,1250.45,2`).

Compile your program to `/home/user/operator_bin`.

**Step 3: Staged Deployment Automation**
Write a bash script `/home/user/deploy.sh` that:
1. Executes `/home/user/operator_bin` to generate the `/home/user/scaling_plan.txt`.
2. Reads `/home/user/scaling_plan.txt` line by line.
3. For each line, formats a JSON payload: `{"chunk": <Chunk_ID>, "replicas": <Replicas>}` and uses `curl` to POST it to `http://localhost:9090/scale` (through the SSH tunnel).

**Verification**
The automated test will evaluate the mathematical precision of your C++ RMS calculation. It will compute the Mean Squared Error (MSE) between the RMS values in your `/home/user/scaling_plan.txt` and the absolute mathematical ground truth for the audio file. Your MSE must be strictly less than 0.1 to pass.