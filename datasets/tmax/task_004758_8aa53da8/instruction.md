As a cloud architect, you are responsible for migrating our legacy infrastructure to a modern cloud-native environment. We have a legacy proprietary data node service provided as a compiled, stripped binary located at `/app/legacy_data_node`. 

The legacy binary runs as a background service, listens on an undocumented TCP port, and writes verbose logs to `/home/user/legacy_logs/node.log`. It expects a specific plaintext command to return its status data. 

Your task is to integrate this legacy binary into our new HTTP-based monitoring system securely and robustly.

Perform the following steps:
1. **Analyze the Binary**: Investigate `/app/legacy_data_node` to discover which port it binds to and what plaintext string command it expects to trigger a status response.
2. **Implement an Auth-Bridge Service**: Write a service (in the language of your choice) that listens on `127.0.0.1:8080`. 
   - It must handle HTTP `GET` requests to the `/status` endpoint.
   - It must enforce authentication: requiring the HTTP header `Authorization: Bearer cloud-migration-token`. Return HTTP 401 if unauthorized.
   - When an authorized request is received, your bridge must open a TCP connection to the legacy binary, send the discovered status command, read the legacy service's response, and return that exact response as the HTTP response body with an HTTP 200 status code.
3. **Service Lifecycle Management**: Create user-level systemd service units in `/home/user/.config/systemd/user/` to manage both the legacy binary (`legacy-node.service`) and your new bridge service (`legacy-bridge.service`). Ensure the bridge service declares a dependency on the legacy service. You do not need to enable them at boot, but they must be able to run via `systemctl --user start ...`.
4. **Log Rotation and Permissions**: The legacy binary does not manage its logs. 
   - Create a logrotate configuration file at `/home/user/logrotate.conf` to manage `/home/user/legacy_logs/node.log`. It must rotate the logs daily, keep 7 days of backups, and compress old logs.
   - Ensure the directory `/home/user/legacy_logs/` has strictly `700` permissions to prevent unauthorized local access.

Leave your bridge service running in the background listening on port 8080 when you finish the task.