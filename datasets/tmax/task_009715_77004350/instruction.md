You are a FinOps Analyst working on optimizing cloud storage costs. You have noticed that several local cache directories used by different teams are growing too large for the expensive "hot" NVMe storage tier. You need to automate the process of identifying large team directories and staging them for a move to a "cold" storage tier.

Your task is to write a Python script and configure the necessary system files to handle this automatically.

Here are the requirements:
1. There is a directory located at `/home/user/s3_cache/` which contains multiple subdirectories. Each subdirectory represents a team's dataset.
2. Write a Python script at `/home/user/finops_tiering.py`. This script must calculate the total size of each subdirectory inside `/home/user/s3_cache/`.
3. For any subdirectory whose total size is strictly greater than 10 Megabytes (10 * 1024 * 1024 bytes), the script must do two things:
    a) Append an fstab-compatible entry to the file `/home/user/finops_fstab` to bind-mount the directory to a cold storage path. The exact format must be:
       `/home/user/s3_cache/<team_dir> /home/user/cold_tier/<team_dir> none bind 0 0`
    b) Append an environment variable to the file `/home/user/finops_env.sh` so the team's tools know about the tier change. The format must be:
       `export <TEAM_DIR_UPPERCASE>_STORAGE_TIER=cold`
       *(e.g., if the directory is named `analytics`, the variable is `ANALYTICS_STORAGE_TIER`)*.
4. Set up a user-level systemd service to run this script. Create the systemd unit file at `/home/user/.config/systemd/user/finops-tiering.service`. The service must:
    - Have a `[Service]` block with `Type=oneshot`.
    - Execute your Python script using `/usr/bin/python3 /home/user/finops_tiering.py`.
5. Finally, run your Python script once manually so that `/home/user/finops_fstab` and `/home/user/finops_env.sh` are generated based on the current contents of `/home/user/s3_cache/`.

Ensure that you create any necessary parent directories for your configuration files before creating the files themselves.