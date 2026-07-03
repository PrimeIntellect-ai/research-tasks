You are an edge computing engineer deploying a data processing pipeline on an IoT device. You need to configure the environment, write a C-based data processor, and set up process supervision.

You have been provided with an image of a configuration snippet at `/app/config.png`.

Perform the following tasks:
1. Extract the configuration from the image. It contains two lines specifying a timezone (`TZ`) and a magic byte (`MAGIC_BYTE`, an integer in base 10).
2. Create a file `/home/user/env.sh` that exports the `TZ` environment variable to the exact timezone value found in the image.
3. Write a C program `/home/user/processor.c` and compile it to an executable at `/home/user/processor`.
   This program must act as a stream filter:
   - It reads binary data from standard input until EOF.
   - For each byte read:
     - If the byte represents an ASCII digit ('0' through '9'), output it unchanged.
     - Otherwise, XOR the byte with the `MAGIC_BYTE` extracted from the image, and output the result.
   - It must write the processed bytes to standard output and flush appropriately.
4. Write a shell script `/home/user/supervisor.sh` (make it executable) that does the following:
   - Sources `/home/user/env.sh`.
   - Creates a named pipe at `/home/user/sensor_data` (if it does not already exist).
   - Enters an infinite loop where it runs `/home/user/processor` with its standard input connected to the `/home/user/sensor_data` pipe and its standard output redirected (append mode) to `/home/user/processed.log`.
   - If the `processor` process terminates for any reason, the supervisor must immediately restart it in the next loop iteration.
5. Create a network routing configuration file `/home/user/route.conf` containing exactly this text (representing the device's uplink route):
   `default via 192.168.1.1 dev eth1`

Your C program (`/home/user/processor`) must be perfectly accurate, as it will be rigorously tested against a reference oracle with random binary inputs to ensure bit-exact equivalence.