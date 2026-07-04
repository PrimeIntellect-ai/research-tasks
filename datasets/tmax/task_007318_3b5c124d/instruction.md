You are acting as a storage administrator. We are running low on disk space, and we suspect a specific noisy service is filling up our compressed log backups.

In `/home/user/logs/`, there are several gzip-compressed log files (`*.log.gz`). 
Each log file contains multi-line log records formatted exactly like this:
```
===RECORD===
Timestamp: 2023-10-12T10:00:00Z
Service: <ServiceName>
Message: <Some log message>
===END===
```

You also have a configuration file at `/home/user/config.ini` which specifies the service we want to analyze. It looks like this:
```
[Target]
Service=Database
```

Your task is to write and execute a Bash script (or use shell commands) to do the following:
1. Parse `/home/user/config.ini` to extract the target Service name (e.g., `Database`).
2. Search through all `*.log.gz` files in `/home/user/logs/` *without* permanently decompressing them to disk (process them as compressed streams).
3. Count the total number of multi-line records across all the compressed files that belong to the target Service. Write this total integer count to `/home/user/summary.txt`.
4. If a compressed log file contains *at least one* record from the target Service, rename that file by appending `.archived` to its name (e.g., `app_1.log.gz` becomes `app_1.log.gz.archived`). Leave files that do not contain the target Service unchanged.

Requirements:
- Only output the single integer count in `/home/user/summary.txt`.
- Do not extract the `.gz` files to disk (use `zcat`, `zgrep`, or similar stream processing).