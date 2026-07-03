You are an observability engineer tasked with deploying a custom video-based metrics exporter on a dashboard monitoring server. 

We have a legacy interactive configuration tool at `/app/legacy_configurator` that generates the required `config.json` for our service. It interactively prompts for a username, password, and a Dashboard ID. 
1. Use an `expect` script to automate running `/app/legacy_configurator`. The credentials you must supply are:
   - Username: `admin`
   - Password: `observability2024`
   - Dashboard ID: `DASH-99`
   The tool will output a `config.json` file in `/home/user/`.

2. We have a dashboard recording video located at `/app/dashboard_recording.mp4`. You need to write a Python application that:
   - Reads the `config.json` generated in step 1.
   - Uses `ffmpeg` (which is pre-installed) to extract the frames of the video and counts the number of "red alert" frames. A red alert frame is defined as a frame where the exact center pixel (width/2, height/2) has a pure red color (RGB: 255, 0, 0).
   - Starts an HTTP server on `127.0.0.1:9090`.
   - When a `GET` request is made to `/metrics` with the header `Authorization: Bearer DASH-99`, it must return a 200 OK with a JSON payload in this exact format:
     `{"dashboard_id": "DASH-99", "red_alerts_count": <the_integer_count>}`

3. Deploy this Python application as a user-level `systemd` service named `video-metrics.service`. 
   - Ensure the service file is placed in the correct directory for user-level systemd units.
   - The service must automatically start the Python server.
   - A common issue in our environment is that this service fails to start if it runs before the network is fully initialized. Ensure your systemd unit file includes the correct directives to only start *after* the `network.target`.
   - Enable and start the service using `systemctl --user`.

Ensure your final Python HTTP service remains running in the background via systemd so our automated verification suite can query it.