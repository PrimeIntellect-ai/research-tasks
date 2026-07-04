We have an interactive bash script at `/home/user/setup_mounts.sh` that our team uses to generate user-space mount configurations. We are migrating our server provisioning to an automated CI/CD pipeline, and this interactive script is blocking our automation.

Your task is to write an `expect` script that automates the execution of `/home/user/setup_mounts.sh`.

Requirements:
1. Create an expect script named `/home/user/auto_mount.exp`.
2. The expect script must execute `/home/user/setup_mounts.sh` and answer the prompts exactly as follows:
   - Device path: `/dev/vdc1`
   - Mount point: `/home/user/data_backup`
   - Filesystem type: `xfs`
   - Mount options: `rw,noexec,nodev`
3. Make sure your expect script is executable and run it once so that the target configuration file (`/home/user/my_fstab.conf`) is generated successfully.

Do not modify the original `/home/user/setup_mounts.sh` script. Use `expect` to handle the interactive prompts.