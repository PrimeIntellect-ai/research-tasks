You are a cloud architect preparing to migrate a legacy email processing backend to a new load-balanced environment. 

Your task is to write an idempotent setup script in Bash located at `/home/user/setup_migration.sh`. When executed, this script must perform the following actions:

1. **Reverse Proxy & Load Balancer Setup**:
   Idempotently generate an HAProxy configuration file at `/home/user/haproxy.cfg`. The configuration must contain:
   - A `defaults` section with `timeout connect 5000ms`, `timeout client 10000ms`, and `timeout server 10000ms`.
   - A `frontend` named `email_front` that binds to `127.0.0.1:8080`.
   - A `backend` named `email_back` that load-balances (using roundrobin) between two backend services: `node1` at `127.0.0.1:8081` and `node2` at `127.0.0.1:8082`.

2. **Storage Monitoring Script**:
   Create a bash script at `/home/user/storage_monitor.sh` that acts as a localized disk quota monitor. When executed, it must:
   - Calculate the total size of the directory `/home/user/mail_spool` in kilobytes.
   - If the total size is strictly greater than 1024 KB (1 MB), it must append the exact line `[WARN] Storage quota exceeded. Clearing spool.` to `/home/user/migration.log` and then delete all files inside `/home/user/mail_spool/`.
   - If the total size is 1024 KB or less, it must append the exact line `[OK] Storage within limits.` to `/home/user/migration.log` and leave the files intact.

Requirements:
- Ensure the setup script makes `/home/user/storage_monitor.sh` executable.
- The directory `/home/user/mail_spool` will already exist on the system.
- Once you have written `/home/user/setup_migration.sh`, execute it so that the configuration and monitor script are generated. 
- You do not need to start HAProxy or run the monitor script in a loop. The automated testing suite will invoke `/home/user/storage_monitor.sh` directly to verify its behavior and parse the HAProxy config.