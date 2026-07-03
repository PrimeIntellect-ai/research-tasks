You are a Site Reliability Engineer investigating a recent rolling deployment failure. During the deployment window, the CI/CD pipeline silently failed to update several nodes due to an SSH configuration issue that rejected key-based logins. 

We have a screen recording of the internal deployment monitoring dashboard from the time of the incident, located at `/app/deployment_monitor.mp4`. 

Your task has two parts:

**Part 1: Video Analysis**
The video `/app/deployment_monitor.mp4` shows a deployment dashboard. At various points, server nodes (labeled "Node-1" through "Node-5") flash red due to the SSH key rejection. 
Use `ffmpeg` and any other text/image processing tools you need to analyze the video. Create a file at `/home/user/failed_nodes.txt` containing the exact frame numbers where "Node-3" displays a "KEY_REJECTED" error overlay. Write one frame number per line.

**Part 2: Log Analyzer Tool**
To prevent this in the future, we are integrating a new log analysis step into our CI/CD pipeline. You must write a Python script at `/home/user/parse_deployment_logs.py`.
This script will be executed with a single command-line argument: a raw string representing an SSH verbose log output. 

Your script must:
1. Accept the raw string as `sys.argv[1]`.
2. Extract all IPv4 addresses that immediately follow the phrase `Connection closed by ` or `Disconnecting from `.
3. Count the occurrences of the exact substring `publickey`.
4. Output a strictly formatted JSON object to `stdout` with exactly two keys:
   - `"failed_ips"`: A sorted list of unique extracted IPv4 addresses.
   - `"key_failures"`: An integer representing the count from step 3.

Example output:
`{"failed_ips": ["10.0.0.5", "192.168.1.10"], "key_failures": 3}`

Your script must be perfectly robust. We will run an automated fuzzing test against your script using thousands of randomized log strings, comparing its output directly to our reference implementation. Your script must match the reference output bit-for-bit for all valid and invalid inputs.