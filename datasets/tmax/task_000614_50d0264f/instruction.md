You are an edge computing engineer deploying a custom monitoring solution for IoT devices. These devices run a critical sensor process that occasionally crashes. You need to build a C++ monitoring utility that checks the process health, integrates with the device's local configuration and environment, and generates a local email-spool alert when the process fails.

Your task has several phases:

1. Environment and Configuration Setup:
   - Append an environment variable `EDGE_NODE_ID=IOT-992` to `/home/user/.bashrc`.
   - Create a configuration file at `/home/user/iot_config.ini` with the exact following contents:
     ```
     AdminEmail=ops@edge.local
     SpoolDir=/home/user/mail_spool/outbox
     ```
   - Create the directory `/home/user/mail_spool/outbox`.

2. C++ Monitor Implementation:
   - Write a C++ program in `/home/user/monitor.cpp`.
   - The program must accept exactly one command-line argument: the path to a PID file (e.g., `/home/user/sensor.pid`).
   - It must read the `EDGE_NODE_ID` environment variable. If not set, default to `UNKNOWN`.
   - It must parse `/home/user/iot_config.ini` to extract `AdminEmail` and `SpoolDir`.
   - It should read the integer PID from the provided PID file.
   - It must check if the process with that PID is currently running (e.g., by checking if `/proc/<PID>` exists or using `kill(pid, 0)`).
   - If the process is running, the program should print "OK" to standard output and exit with code 0.
   - If the process is NOT running (or the PID file does not exist), the program must generate an alert email file in the `SpoolDir`.
     - The filename must be `alert.eml` (i.e., `/home/user/mail_spool/outbox/alert.eml`).
     - The contents of this file must be exactly:
       ```
       To: ops@edge.local
       Subject: ALERT: Node IOT-992 offline
       
       The sensor process is down.
       ```
       (Use the actual values parsed from the config and environment).
     - After generating the alert, print "ALERT GENERATED" to standard output and exit with code 1.

3. Compilation and Execution:
   - Compile your C++ code to an executable at `/home/user/monitor` using `g++` (e.g., `g++ -std=c++11 /home/user/monitor.cpp -o /home/user/monitor`).
   - We have provided a test script at `/home/user/run_test.sh` that simulates the sensor lifecycle. Source your `.bashrc` and execute this script. It will start a fake sensor process, create a PID file, run your monitor, kill the sensor, and run your monitor again to trigger the alert.

Ensure all file paths, output formats, and exit codes are exactly as specified.