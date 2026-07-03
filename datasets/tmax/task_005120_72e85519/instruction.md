You are an infrastructure engineer managing a multi-service logging and backup pipeline. 

We have a local microservice setup located in `/app/microservices/`. The system consists of two main components:
1. A data generator (`/app/microservices/generator.py`) that rapidly creates 5,000 log files in `/home/user/data/raw/`.
2. A backup service (`/home/user/backup_service.py`) that compresses these files and moves them to `/home/user/data/backup/`.

Currently, the `backup_service.py` is implemented sequentially and is far too slow, causing a bottleneck in our pipeline. It takes over 15 seconds to process 5,000 files.

Additionally, we have an interactive CLI tool (`/app/microservices/cli_admin.py`) that requires interactive prompts to trigger a system restore.

Your tasks:
1. **Optimize the Backup Service:** Rewrite `/home/user/backup_service.py` in Python to use multiprocessing or multithreading. It must read all files from `/home/user/data/raw/`, compress them using the `gzip` module, save them to `/home/user/data/backup/` with a `.gz` extension, and delete the original files. The optimized script must process all 5,000 files in **under 2.0 seconds**.
2. **Automate Interactive CLI:** Write an Expect script at `/home/user/auto_restore.exp` that automates `/app/microservices/cli_admin.py`. The CLI tool asks "Enter admin password:" (the password is "admin123") and then "Confirm restore? (y/n):" (you must answer "y"). The Expect script must successfully complete the interaction and exit with code 0.
3. **Process Management:** Ensure that both the raw and backup directories exist before running your service. 

To complete the task, leave the highly optimized `/home/user/backup_service.py` and the functional `/home/user/auto_restore.exp` in place.