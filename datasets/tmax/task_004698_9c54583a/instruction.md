You are an infrastructure engineer acting as a capacity planner. We have received an audio memo from the lead architect detailing the new resource limits and the port allocation for our new capacity planning API. 

Your objective is to deploy a Python-based capacity planner service that adheres to the specifications hidden within the audio memo, configure its access controls, and manage it via user-level systemd.

Follow these instructions exactly:

1. **Extract Audio Specifications:**
   Analyze the audio file located at `/app/capacity_memo.wav`. You may use any available Python library (like `SpeechRecognition` or `pydub`) or command-line tool (like `whisper` or `ffmpeg` if you need to extract metadata) to decode the spoken voice memo. The memo will state two critical numbers: the "CPU threshold percentage" and the "API port". 

2. **Initialize the Local Database:**
   We have an interactive setup script at `/app/init_capacity_db.sh`. You must automate the interaction with this script using an `expect` script or Python `pexpect`. 
   The script will prompt for:
   - `Enter CPU threshold:` (Use the value transcribed from the audio)
   - `Enter admin PIN:` (The PIN is the octal file permission of `/app/init_capacity_db.sh` repeated twice, e.g., if permissions are 755, enter 755755)
   Successfully running this will generate a configuration file at `/home/user/capacity_config.json`.

3. **Secure the Configuration:**
   Apply ACLs (Access Control Lists) to `/home/user/capacity_config.json` so that ONLY the user `user` has read access, and remove all other default group/others permissions.

4. **Develop the Capacity API:**
   Write a Python HTTP service at `/home/user/planner_api.py`.
   - It must listen on `127.0.0.1` and the port specified in the audio memo.
   - It must expose a GET endpoint at `/api/v1/capacity`.
   - It must require an HTTP header for authentication: `X-Planner-Auth: <admin PIN>`.
   - When requested with the correct header, it must read `/home/user/capacity_config.json` and return a JSON response exactly matching its contents, plus a dynamic field `"status": "analyzing"`. 

5. **Service Management:**
   Create a systemd user service unit file at `~/.config/systemd/user/capacity-planner.service` to manage the execution of `/home/user/planner_api.py`. 
   Enable and start the service so it runs continuously in the background.

Ensure the final HTTP service is robust and correctly responds to authenticated requests based on the initialized database.