I am a bioinformatics researcher working on a project that analyzes protein vibrational modes by coupling sequence data with simulated structural dynamics. I have a multi-service setup in `/app` that is partially incomplete and broken. I need you to compile the simulation backend, fix the Python API, and write a startup script to bring the system online.

Here is the structure of `/app`:
- `/app/src/sim_server.c`: A C program that acts as a TCP simulation backend.
- `/app/api.py`: A Python Flask API that acts as the frontend, but the sequence parsing and spectral analysis logic are broken.
- `/app/data/`: Contains several `.fasta` files (e.g., `protA.fasta`, `protB.fasta`).

**Step 1: Compile the Backend**
Compile `/app/src/sim_server.c` into an executable named `/app/bin/sim_server` (you may need to create the `bin` directory). It requires standard mathematical libraries.

**Step 2: Fix the Python API (`/app/api.py`)**
The Flask API runs on `127.0.0.1:8080`. It exposes the endpoint `GET /analyze?fasta_id=<id>`. 
You need to fix the implementation of this endpoint so that it does the following:
1. Validates the `Authorization` header. It must exactly match `Bearer biophysics2024`. If missing or incorrect, return a 401 status code.
2. Reads the first line of `/app/data/<fasta_id>.fasta` to get the sequence header (remove the leading `>` and trailing whitespace). If the file doesn't exist, return a 404.
3. Opens a TCP connection to the simulation backend at `127.0.0.1:9000`.
4. Sends the `<fasta_id>` string followed by a newline (`\n`) over the TCP socket.
5. Reads exactly 16,384 bytes from the socket. This data represents a $64 \times 64$ 2D matrix of 32-bit floats (little-endian). Convert this raw byte data into a `numpy` 2D array.
6. Performs a 2D Discrete Fourier Transform (FFT) on the matrix.
7. Computes the power spectrum (the squared absolute value of the FFT output).
8. Finds the `[row, col]` coordinates of the dominant frequency. *Important:* You must ignore the DC component (frequency 0 at index `[0, 0]`) by temporarily setting its power to 0 before finding the maximum.
9. Returns a JSON response with the HTTP 200 status code in this exact format:
   ```json
   {
     "fasta_header": "Header text here",
     "peak_freq": [row_index, col_index]
   }
   ```

**Step 3: Service Composition**
Write an executable bash script at `/app/start.sh` that:
1. Starts the C backend: `/app/bin/sim_server 9000 &`
2. Starts the Python API: `python3 /app/api.py &`
3. Waits for both background processes (e.g., using `wait`).

Please complete the code, build the binaries, and leave the services running or ready to run via `/app/start.sh`. Do not change the ports (8080 and 9000) or the authorization token.