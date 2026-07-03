You are acting as a cloud architect migrating a legacy port-forwarding service to a new Rust-based dynamic network router. You need to handle configuration backup, migration, code implementation, and a staged deployment without root privileges.

All work must be done within `/home/user`.

Phase 1: Configuration Migration and Backup Script
There is a legacy configuration file at `/home/user/legacy_proxy.conf` with the following format:
```
route_api=18080
route_web=18081
route_metrics=18082
```
Write a bash script at `/home/user/backup_and_convert.sh` that does the following idempotently:
1. Creates a directory `/home/user/backups/`.
2. Copies `/home/user/legacy_proxy.conf` to `/home/user/backups/legacy_proxy.conf.bak`.
3. Parses the legacy configuration and converts it into a JSON file at `/home/user/new_proxy.json` with the exact following structure:
```json
{
  "routes": [
    {
      "name": "route_api",
      "port": 18080
    },
    ...
  ]
}
```
Ensure the script is executable and run it to generate the JSON file.

Phase 2: Rust Service Implementation
Create a new Rust binary project at `/home/user/proxy_service` (using `cargo new`).
Modify the Rust project to do the following:
1. Read the `/home/user/new_proxy.json` file.
2. For each route in the JSON file, bind a TCP listener to `127.0.0.1:<port>`. 
3. The service should log exactly `Started <name> on <port>` for each successfully bound port, appended to `/home/user/proxy.log`.
4. The service must keep running and keep the ports bound.

You may use dependencies like `serde` and `serde_json` in your `Cargo.toml`.

Phase 3: Deployment Script
Write a deployment script at `/home/user/deploy.sh` that:
1. Builds the Rust project in release mode.
2. Starts the compiled Rust binary in the background.
3. Polls `/home/user/proxy.log` until all three routes (`route_api`, `route_web`, `route_metrics`) have logged their startup messages.
4. Once all three are verified to be running via the log, writes the exact string `status=MIGRATED` to `/home/user/migration_status.txt`.

Execute your deployment script. Keep the background Rust service running so the bound ports can be verified.