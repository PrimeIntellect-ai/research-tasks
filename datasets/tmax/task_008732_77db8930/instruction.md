You are a monitoring specialist tasked with setting up a custom alert system for a set of internal services. These services have been failing to communicate properly, and their logs are a mess because they are running with different locale and timezone configurations. 

You need to write a Go application that processes these logs, standardizes the timezones, correlates errors with service ownership, and generates a structured alert file.

Here are the requirements:

1. **Input Files**:
   - The services generate a log file at `/home/user/logs/services.log`. (Assume this file already exists). 
     Format: `[YYYY-MM-DD HH:MM:SS TIMEZONE] SERVICE_NAME STATUS MESSAGE`
     Example: `[2023-10-25 14:30:00 PDT] auth-service ERROR Connection Refused`
   - There is a service ownership configuration file at `/home/user/config/service_groups.conf`. (Assume this file already exists).
     Format: `service_name:admin_group`
     Example: `auth-service:sec-ops`

2. **The Go Application**:
   - Write a Go program at `/home/user/monitor.go`.
   - The program must parse the `services.log` file.
   - It should identify only the log lines where the STATUS is `ERROR` and the MESSAGE exactly starts with `Connection Refused`.
   - For these matched lines, the program must convert the timestamp to UTC and format it as a strict RFC3339 string (e.g., `2023-10-25T21:30:00Z`). Recognize at least `UTC`, `PDT`, `EST`, and `JST` timezones (assume standard non-daylight savings offsets if necessary for simplicity: PDT=UTC-7, EST=UTC-5, JST=UTC+9).
   - The program must look up the `SERVICE_NAME` in the `service_groups.conf` file to find the responsible `admin_group`. If a service is not found, use `unknown`.

3. **Output File**:
   - The Go program must write the results to `/home/user/alerts.json` as a JSON array of objects, ordered exactly as they appeared in the log file.
   - The JSON objects must have the following schema:
     `{"timestamp": "RFC3339_UTC_STRING", "service": "SERVICE_NAME", "group": "ADMIN_GROUP"}`

4. **Orchestration**:
   - Create a shell script at `/home/user/run_monitor.sh` that:
     1. Compiles `/home/user/monitor.go` into an executable named `/home/user/monitor_bin`.
     2. Sets the environment variable `TZ=Europe/London` (to ensure your system locale doesn't accidentally make local time parsing succeed without explicit timezone handling).
     3. Executes `/home/user/monitor_bin`.
   - Ensure the shell script is executable.

Your final goal is to create `/home/user/monitor.go` and `/home/user/run_monitor.sh`, and then run `/home/user/run_monitor.sh` so that `/home/user/alerts.json` is successfully generated.