You are an edge computing engineer tasked with automating the deployment of a new sensor service on an IoT device. Because you are deploying to legacy edge hardware, part of the configuration requires interacting with a legacy text-based interface, taking backups of existing data, and managing the service lifecycle manually.

Write a Python automation script located at `/home/user/deploy_edge.py` that performs the following steps in order:

1. **Interactive Configuration (Expect Scripting)**:
   There is a mock legacy configuration utility located at `/home/user/mock_device_cli.py`. Your Python script must use the `pexpect` library to run and interact with this utility. 
   - It will prompt: `Enter Device ID:` -> You must send `EDGE-404`
   - It will prompt: `Enable remote telemetry? (Y/N):` -> You must send `Y`
   - It will prompt: `Enter service port:` -> You must send `8080`
   If successful, the utility will silently generate a `/home/user/config.json` file.

2. **Backup Strategy**:
   Before starting the new service, you must back up the existing data. 
   Compress the entire directory `/home/user/sensor_data/` into a tarball located at `/home/user/backup/data_backup.tar.gz`. 
   (Create the `/home/user/backup/` directory in your script if it does not exist).

3. **Service Lifecycle Management**:
   A previous version of the service might be running on port 8080. Your script must find any process listening on `localhost:8080` and terminate it safely.
   Then, start the new service by executing `/home/user/edge_service.py` in the background. The service reads `/home/user/config.json` to start on the correct port.

4. **Connectivity Diagnostics**:
   Wait up to 5 seconds for the service to initialize. Then, have your script perform an HTTP GET request to `http://127.0.0.1:8080/health`. 

5. **Reporting**:
   Based on the success of the above steps, your script must generate a JSON file at `/home/user/deploy_report.json` with the exact following keys:
   - `"config_generated"`: boolean (true if `/home/user/config.json` exists)
   - `"backup_created"`: boolean (true if `/home/user/backup/data_backup.tar.gz` exists)
   - `"health_status"`: string (the exact text body returned by the `/health` endpoint, e.g., `"OK"`)

**Constraints**:
- Your script must be written in Python 3 and use `pexpect` for the interactive portion.
- Do not modify `/home/user/mock_device_cli.py` or `/home/user/edge_service.py`.
- Ensure your script is executable and can be run with `python3 /home/user/deploy_edge.py`.

(Note: You will need to create the files and run your script to complete the task).