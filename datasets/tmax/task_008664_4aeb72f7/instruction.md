You are an edge computing engineer deploying a new sensor data pipeline to an IoT device. You need to set up the local processing logic, storage configuration, and networking setup for exposing the data. You do not have root access, so you will simulate system configurations in local files.

Your task consists of the following four steps:

**1. Sensor Data Processor (C++)**
Create a directory `/home/user/edge_app/`. Inside it, write a C++ program named `sensor_processor.cpp`. 
This program must read comma-separated lines from standard input in the format: `timestamp,sensor_id,value` (where value is a float).
It should read an environment variable named `MIN_THRESHOLD`. If the variable is not set, default to 0.0.
The program must output (to standard output) only the lines where the `value` is strictly greater than `MIN_THRESHOLD`.

**2. Task Automation Pipeline (Bash)**
Write a shell script at `/home/user/edge_app/run_pipeline.sh`. This script must:
- Compile `sensor_processor.cpp` into an executable named `processor` in the same directory.
- Export the environment variable `MIN_THRESHOLD=45.5`.
- Read raw sensor data from `/home/user/data/raw_sensors.log`.
- Pipe the raw data into the `processor` executable.
- Pipe the output of the processor into a text processing pipeline (using `awk`, `sed`, or standard tools) to reformat the valid lines into exactly this format: `[<sensor_id>] recorded <value>`
- Save the final formatted output to `/home/user/data/processed_sensors.txt`.

**3. Storage Configuration**
The IoT device expects a custom fstab file to handle mounting the data partition. 
Create or append to the file `/home/user/system_fstab`. Add a single standard fstab entry to mount the loopback file `/home/user/sensor_disk.img` to the mount point `/home/user/data` using the `ext4` filesystem. Use the mount options `rw,user,noatime` and set dump to `0` and pass to `2`. Ensure columns are separated by tabs or spaces.

**4. Load Balancer Configuration**
The edge device runs a user-space Nginx instance to serve the processed data from multiple backend workers.
Create an Nginx configuration file at `/home/user/edge_app/lb.conf`. It must contain:
- An `upstream` block named `sensor_backends` that balances traffic between `127.0.0.1:9001` and `127.0.0.1:9002`.
- A `server` block listening on port `8080`.
- A location block `/` that uses `proxy_pass` to route traffic to `http://sensor_backends`.

Make sure all files are created exactly at the specified paths. You do not need to run Nginx or create the raw sensor log file; an external test suite will provide the log file and execute your script to verify your setup.