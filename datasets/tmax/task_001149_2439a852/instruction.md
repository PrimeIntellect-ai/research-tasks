You are an edge computing engineer deploying a new sensor data filtering daemon to a fleet of IoT devices. The devices receive JSON payloads from local sensors, but recent firmware bugs in the sensors have resulted in malformed and oversized payloads being written to disk, which is crashing our downstream analytics daemons.

You need to build a C-based filter program that will act as a gatekeeper, validating sensor logs before they are processed. We are using the `cJSON` library for parsing. 

Here are your tasks:

1. **Fix the Vendored cJSON Package**
   We have vendored the `cJSON` (version 1.7.15) source code in the container at `/app/cJSON-1.7.15`. However, the `Makefile` was accidentally checked in with an IoT cross-compiler hardcoded, causing the build to fail on our x86_64 build servers. 
   - Fix the `Makefile` in `/app/cJSON-1.7.15` so that it uses the standard system `gcc` compiler.
   - Run `make` to compile the library and produce the shared object `libcjson.so`.

2. **Implement the Sensor Filter in C**
   Write a C program at `/home/user/sensor_filter.c` that uses `cJSON` to validate incoming payloads.
   - The program must take exactly one command-line argument: the path to a JSON file.
   - It must read the file and attempt to parse it using `cJSON_Parse`.
   - To be considered a "valid" sensor reading, the JSON must strictly meet all of these conditions:
     1. It is a valid JSON object.
     2. It contains a key named `"sensor_id"` whose value is a string strictly less than 32 characters in length.
     3. It contains a key named `"value"` whose value is a number.
   - If the file meets all conditions, your program must exit with status code `0` (accept).
   - If the file fails to open, is malformed JSON, or violates any of the structural conditions above, your program must exit with status code `1` (reject).
   - Compile this program into an executable named `sensor_filter`, dynamically linking it against the `libcjson.so` you built in step 1.

3. **Validate Against the Corpora**
   We have provided two directories of test payloads:
   - `/app/corpus/clean/`: Contains valid sensor readings.
   - `/app/corpus/evil/`: Contains malformed logs, oversized strings, and incorrect types.
   Ensure your compiled `sensor_filter` successfully exits `0` for all files in the clean corpus, and exits `1` for all files in the evil corpus.

4. **Automate the Rolling Deployment**
   Write a bash script at `/home/user/deploy.sh` to deploy the filter binary. The script must execute the following rolling deployment steps:
   - Ensure the deployment base directory exists at `/home/user/opt/edge_sensor/releases/v2`.
   - If a symlink exists at `/home/user/opt/edge_sensor/current`, copy the directory it points to into `/home/user/opt/edge_sensor/backup` as a fallback.
   - Copy your compiled `sensor_filter` binary and the compiled `libcjson.so` into `/home/user/opt/edge_sensor/releases/v2/`.
   - Atomically create or update a symlink at `/home/user/opt/edge_sensor/current` to point to `/home/user/opt/edge_sensor/releases/v2`.
   
Once you have written `deploy.sh`, execute it to finalize the deployment.