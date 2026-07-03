You are acting as a capacity planner and deployment engineer. Your task is to create a multi-language deployment script that handles rolling/staged deployments while strictly monitoring and enforcing a local directory "quota" to save disk space.

Write a Python 3 script located at `/home/user/deploy.py` that implements an idempotent staged deployment with storage monitoring. 

The script must fulfill the following requirements:
1. It must accept exactly one command-line argument: a release version string (e.g., `python3 /home/user/deploy.py v2.1`).
2. It must copy the entire contents of the directory `/home/user/app_source/` into a new release directory at `/home/user/releases/<version>/`. 
3. The copying operation must be idempotent. If the destination release directory already exists, it should overwrite/update the files inside it without failing.
4. It must create or update a symlink at `/home/user/releases/current` to point to the newly deployed release directory (`/home/user/releases/<version>/`).
5. **Storage Monitoring & Quota Enforcement:** After creating the new release and updating the symlink, the script must calculate the total size (in bytes) of everything inside the `/home/user/releases/` directory.
6. If the total disk usage of `/home/user/releases/` exceeds `204800` bytes (200 KB), the script must automatically delete the oldest release directories (based on the directory's modification time) one by one until the total size is `204800` bytes or less.
7. **Crucial exception:** The script must *never* delete the release directory that the `current` symlink points to, even if the total size cannot be reduced below the quota.

Ensure the script has executable permissions (`chmod +x /home/user/deploy.py`). Do not execute the script yourself; an automated test suite will run it to simulate multiple deployments and verify your implementation.

Directory setup:
- Source directory: `/home/user/app_source/` (You can create this and place dummy files in it for your own testing if desired).
- Deployments directory: `/home/user/releases/` (Create this directory if it doesn't exist).