You are an edge computing engineer configuring an IoT device. You need to deploy a local C++ sensor daemon, fix a misconfigured UNIX socket path (which is currently causing upstream gateway connection errors akin to an Nginx 502 error), and configure a backup job for the sensor data.

Here are your tasks:

1. **Fix and Compile the Edge Daemon:**
   - There is a C++ source file located at `/home/user/edge_daemon.cpp`. 
   - Currently, it hardcodes the UNIX socket path to `/tmp/app.sock`. This is incorrect and causes the local API gateway to fail to connect.
   - Modify `/home/user/edge_daemon.cpp` so that it binds the UNIX socket to `/home/user/run/edge.sock`.
   - Compile the program using `g++` and output the executable to `/home/user/edge_daemon`.

2. **Run the Daemon and Trigger Data Generation:**
   - Start your compiled `/home/user/edge_daemon` in the background.
   - Run the provided Python gateway script: `python3 /home/user/client.py`. 
   - The python script will connect to your daemon via `/home/user/run/edge.sock` and request data. If successful, the daemon will write sensor readings to `/home/user/data/sensor.log`.

3. **Configure a Scheduled Backup Script:**
   - Standard cron jobs are disabled on this edge device due to container constraints. You must create a shell script at `/home/user/backup_job.sh` that simulates a scheduled backup sequence.
   - When executed, `/home/user/backup_job.sh` must do the following in order:
     a. Compress `/home/user/data/sensor.log` into a tar.gz archive at `/home/user/backups/backup_1.tar.gz`.
     b. Sleep for exactly 1 second.
     c. Compress the log into `/home/user/backups/backup_2.tar.gz`.
     d. Sleep for exactly 1 second.
     e. Compress the log into `/home/user/backups/backup_3.tar.gz`.
   - Ensure the tarballs are created correctly. You may use `tar -czf`.
   - Run your `/home/user/backup_job.sh` script to generate the backups.

4. **Clean up:**
   - Gracefully stop the `edge_daemon` process once the backups are generated.

Ensure all requested files are in their exact specified absolute paths.