You are a cloud architect migrating a legacy video processing service to a new staged deployment architecture. The legacy service retrieves traffic camera footage from a secure vault and optimizes it for low-bandwidth network transmission.

Your objective is to build the new automated pipeline as a standard user. You will use Bash, Expect, and systemd user services to complete the migration.

Step 1: Network Authentication (Expect)
There is a simulated legacy authentication tool located at `/app/legacy_vault` (which you can assume exists and acts as an interactive CLI). When executed, it prompts:
"Username: " -> you should send "cloud_admin"
"Migration Pin: " -> you should send "8821"
"Action: " -> you should send "GET_TOKEN"
It will then output a network token. Write an Expect script at `/home/user/auth.exp` that automates this interaction and prints ONLY the final token to standard output.

Step 2: Storage Configuration (fstab)
The new architecture requires a staged NFS mount. Create a file `/home/user/fstab.staged` and add exactly one line representing an NFSv4 mount:
Mount the remote share `10.0.5.50:/var/video_archive` to the local path `/mnt/video_staged`. Use the `nfs4` filesystem type. The mount options must be `rw,soft,intr,noatime,x-systemd.automount`. Use `0` for both dump and pass.

Step 3: Video Optimization (Bash & ffmpeg)
We have provided a sample raw traffic camera video at `/app/traffic_cam.mp4`.
Write a Bash script at `/home/user/optimize_stream.sh` that:
1. Calls your `/home/user/auth.exp` script to get the token (though you won't actively use the token in the ffmpeg command, you must assign it to a variable `AUTH_TOKEN`).
2. Uses `ffmpeg` to compress `/app/traffic_cam.mp4` and save the output to `/home/user/migrated_stream.mp4`.
You must optimize the network bandwidth by reducing the bitrate/resolution of the video. However, the resulting video MUST maintain high structural similarity to the original. The automated verifier will calculate the SSIM (Structural Similarity Index) between `/app/traffic_cam.mp4` and your `/home/user/migrated_stream.mp4`. Your video must achieve an SSIM score of >= 0.90 while being as small as possible.

Step 4: Service Lifecycle (systemd)
Create a systemd user service to manage this script. Create the service file at `/home/user/.config/systemd/user/video-migrator.service`.
It must:
- Have a description "Staged Video Migrator"
- Run `/home/user/optimize_stream.sh`
- Use `Type=oneshot`
- Be wanted by `default.target`
You do NOT need to start the service, just ensure the unit file is syntactically correct and placed in the exact path above.

Ensure all scripts are executable and test your `ffmpeg` compression to guarantee it produces `/home/user/migrated_stream.mp4` successfully.