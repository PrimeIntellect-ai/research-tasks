You are tasked with recovering and configuring a local artifact repository system for curating binary distributions. The system consists of three microservices and a native C processing tool. Recently, the environment was partially corrupted: configuration files were scrambled, and the source code for the primary archive-filtering tool was lost (though a stripped compiled binary remains).

Your objective is to complete the following two stages:

### Stage 1: Service Reconfiguration
The artifact system uses three services located in `/app/services/`:
1. **Redis**: Needs to run on port 6379. Update `/app/services/redis/redis.conf` to set the password to `artf_secure_99`.
2. **Nginx**: Serves the binary chunks. Update `/app/services/nginx/nginx.conf` so that it listens on port 8080 (instead of 80) and serves files directly from `/home/user/repo/data`. Ensure it runs entirely in user-space (no root privileges) by moving its pid and temp paths to `/home/user/repo/run/`.
3. **Registry API**: A Flask application in `/app/services/registry/app.py`. Modify its environment variables or configuration so it connects to Redis with the new password and routes download requests to `http://127.0.0.1:8080`.

You must start all three services in the background and ensure the Registry API successfully responds to a `GET /health` request on port 5000.

### Stage 2: Archive Filter Implementation (C)
The Registry API relies on a C utility to process custom `.arf` archives before making them available. The source code is gone, but a reference oracle exists at `/app/bin/filter_oracle`.

You must write a C program at `/home/user/filter_archive.c` and compile it to `/home/user/filter_archive`.
The program must perfectly emulate the behavior of the oracle. 

**Observed Oracle Behavior:**
- Usage: `./filter_archive <input_file> <output_file>`
- The input is a binary file composed of consecutive chunks.
- Each chunk has:
  - Magic bytes: `ARTF` (4 bytes)
  - Chunk Type: 1 byte (0x00 = Header, 0x01 = Code, 0x02 = Debug Symbols, 0x03 = Signature)
  - Payload Size: 4 bytes (unsigned integer, little-endian)
  - Payload: N bytes (equal to Payload Size)
- The tool must parse the file, **discard any chunk of type 0x02 (Debug Symbols)**, and write the remaining chunks to the `<output_file>`.
- **Constraint:** To prevent partial reads by the Nginx server during processing, the tool must write its output to a temporary file in the same directory as the output file (using `mkstemp` or similar) and then atomically rename it to the target `<output_file>`.
- Exit with code 0 on success, or 1 if the input file is malformed (e.g., bad magic bytes) or cannot be read.

Ensure your compiled binary precisely matches the input/output behavior of the oracle on arbitrary valid or invalid files. The automated testing suite will randomly fuzz both your program and the oracle with thousands of inputs to assert bit-exact output equivalence.