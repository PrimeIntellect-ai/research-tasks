You are a network engineer troubleshooting a failing CI/CD deployment pipeline. The deployment is getting blocked by intermittent firewall rules, and malicious routing manifests are being injected into the pipeline.

You need to perform three tasks to secure and restore the deployment process:

**1. Analyze the Deployment Video**
There is a diagnostic recording of the deployment dashboard's status indicator at `/app/deployment_monitor.mp4`. The indicator is normally green, but flashes solid red (RGB: 255, 0, 0) during network drops.
Write a script to analyze this video and count the exact number of frames that are completely solid red.
Output ONLY the integer count to `/home/user/red_frames.txt`.

**2. Create a Routing Manifest Sanitiser**
You must write a Python script at `/home/user/validate_manifests.py` that acts as a classifier for the CI/CD pipeline. 
The script must take a single file path as a command-line argument.
It should read the target JSON file, which contains a dictionary of network routes (e.g., `{"routes": [{"destination": "192.168.1.5"}, ...]}`).
*   A manifest is **EVIL** (must be rejected) if ANY destination IP address in the routes falls within the `198.51.100.0/24` subnet.
*   A manifest is **CLEAN** (must be accepted) if it contains no such IPs.
Your script must exit with status code `0` if the file is CLEAN, and exit with status code `1` if the file is EVIL.

**3. Configure a Scheduled Port Forward**
To bypass the blocked network segment, we need a local stage deployment bridge. 
Write a Python script at `/home/user/forward.py` that listens on `127.0.0.1:8888` and forwards all TCP traffic to `127.0.0.1:9999`.
Then, configure a user-level cron job that executes `/home/user/forward.py` every minute (e.g., `* * * * * python3 /home/user/forward.py`).