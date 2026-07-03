You are helping fix a broken custom build and packaging script for a distributed system. 

In `/home/user/system_build/`, there is a Python script named `build_pack.py` and a directory called `configs/` containing configuration files for multiple services. The script is supposed to read these JSON configs, assign a unique port to each service based on their constraints, serialize the configuration into a custom binary format, and finally append a CRC32 checksum to ensure integrity.

However, `build_pack.py` is currently broken:
1. The naive port assignment logic fails to find a valid assignment because it doesn't handle overlapping constraints properly (some services strictly require a port that another service might greedily take).
2. The binary serialization format is implemented incorrectly.
3. The CRC32 calculation is flawed.

Your task is to fix `/home/user/system_build/build_pack.py` so that it successfully generates `/home/user/system_build/output.pack` according to the following strict specifications:

**Constraint Satisfaction (Port Assignment):**
Each JSON file in `configs/` has an `allowed_ports` list. You must assign exactly one port to each service such that:
- Every service gets a port from its `allowed_ports` list.
- No two services are assigned the same port.

**Serialization Format (Binary):**
The output file `output.pack` must be exactly structured as follows (Big-Endian for all integers):
1. Magic Header: The ASCII string `PACK` (4 bytes).
2. Service Count: Number of services packed (2-byte unsigned integer).
3. For each service (sorted alphabetically by service name):
   - Name Length: Length of the service name (1-byte unsigned integer).
   - Name: The service name string (ASCII).
   - Assigned Port: The uniquely assigned port (2-byte unsigned integer).
   - Config Data Length: Length of the raw JSON string from the file (4-byte unsigned integer).
   - Config Data: The raw JSON string from the file (UTF-8).
4. Checksum: A 4-byte unsigned integer representing the CRC32 of all preceding bytes (from the magic header down to the end of the last service's config data). Use `zlib.crc32`.

Once you have fixed `build_pack.py`, execute it so that `/home/user/system_build/output.pack` is created. Do not modify the JSON files in `configs/`.