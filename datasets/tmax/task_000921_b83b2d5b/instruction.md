You are a Site Reliability Engineer tasked with monitoring network uptime and analyzing automated incident logs. 

We have a diagnostic video feed from our core router's status panel, saved at `/app/router_diag.mp4`. When the network link drops, the status LED at exact pixel coordinates (X: 100, Y: 100) turns red (where Red > 200, Green < 50, Blue < 50). 
Your first task is to extract frames from this video (you may use `ffmpeg`) and write a Rust program to process them. Count the total number of frames where the router link is down. Save this integer count to `/home/user/downtime_frames.txt`.

Second, our automated network monitoring generates log snippets, but it's prone to false positives. We have an adversarial corpus of logs. Real incidents ("evil") indicate a DDoS attack (e.g., they contain the exact phrase "UDP FLOOD" or show more than 50 connections from a single IP address). Benign logs ("clean") might show high traffic but lack these malicious signatures.
Write a Rust binary project in `/home/user/classifier/` whose executable takes a single file path as a command-line argument. It must print exactly `EVIL` to stdout if the log is an attack, and `CLEAN` to stdout if it is benign.

Third, to ensure we can capture alerts reliably, set up a local mail spool environment. 
1. Create a 50MB sparse file at `/home/user/mail.img`.
2. Write the exact `fstab`-formatted line that would be required to mount this image as an `ext4` loopback filesystem at `/home/user/mail_backup` with default options. Save this single line to `/home/user/fstab_line.txt`.
3. Create the directory `/home/user/mail_backup`.
4. Launch a detached rootless container using `podman` (use the `alpine:latest` image). The container must run a sleep command (`sleep 3600`), be named `mail_spooler`, and bind-mount the host directory `/home/user/mail_backup` to `/var/mail` inside the container.

Ensure your Rust code compiles cleanly and your container is running.