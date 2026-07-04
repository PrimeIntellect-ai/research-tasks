You are acting as an infrastructure engineer automating the provisioning of a network configuration validation pipeline. 

We have a multi-service architecture located in `/app/` that receives network device configurations, queues them, and parses them for validation. The architecture consists of:
1. A Redis instance acting as the message queue (port 6379).
2. A Flask webhook receiver (source provided in `/app/webhook.py`) running on port 8080.
3. A backend Python processing daemon that you must write, located at `/home/user/pipeline/parser_daemon.py`.

Your task is to:
1. **Environment & User Roles:** Create an application-level user access file at `/home/user/pipeline/users.json` mapping the user `netadmin` to the group `netops` and user `backup_svc` to `backup`. 
2. **Idempotent Configuration:** Write a bash script at `/home/user/pipeline/setup.sh` that safely creates the necessary directories (`/home/user/pipeline/backups/` and `/home/user/pipeline/logs/`), sets up the Redis configuration to require a password ("netpass"), and starts the Flask webhook receiver using Waitress or Gunicorn in the background. It must backup any existing `/app/webhook.py` to the backups directory with a timestamp before making any necessary adjustments to connect it to Redis.
3. **Daemon Implementation:** Write the `parser_daemon.py`. This script must continuously poll the Redis queue `config_queue`. When it pops a network configuration payload (a string), it must parse and normalize it. You are provided a compiled reference binary at `/app/oracle_parser`. Your Python parsing logic must produce *bit-exact* identical output to what `/app/oracle_parser` produces for any given string input. The daemon should write the normalized output to `/home/user/pipeline/logs/processed.log`.
4. **Process Monitoring:** Your `setup.sh` must start both the Flask app and your `parser_daemon.py`, ensuring they write their PIDs to `/home/user/pipeline/flask.pid` and `/home/user/pipeline/daemon.pid`.

Ensure all file paths are exact. Your parser daemon must take the raw string from Redis, process it, and output the exact string format expected. You can test your parser against `/app/oracle_parser` by passing strings via stdin.