You are a site administrator managing user account requests. You have a raw log file of account requests and need to automate the extraction of approved users, format them into JSON using a custom C++ utility, and serve the result over a local forwarded port.

Perform the following steps:

1. **Text Processing Pipeline**:
   Read the file `/home/user/raw_requests.txt`. This file contains logs in the format: `[DATE] [STATUS] [USERNAME] [EMAIL]`.
   Use command-line text processing tools (like `awk`, `grep`, or `sed`) to extract only the rows where the status is exactly `APPROVED`. Output the `USERNAME` and `EMAIL` fields separated by a comma (e.g., `jsmith,jsmith@example.com`) to a new file at `/home/user/approved_users.csv`.

2. **C++ Processing Utility**:
   Write a C++ program at `/home/user/json_generator.cpp`. 
   This program must:
   - Read `/home/user/approved_users.csv`.
   - Parse each line to extract the username and email.
   - Generate a valid JSON array of objects, where each object has the keys `"username"` and `"email"`.
   - Write the resulting JSON string to `/home/user/public_html/users.json`.
   Compile your C++ program to an executable named `/home/user/json_generator` and run it.

3. **Service & Port Forwarding**:
   - Start a simple HTTP server on port `8080` that serves the `/home/user/public_html` directory in the background (e.g., using `python3 -m http.server 8080 --directory /home/user/public_html &`).
   - Create a local port forward using `socat` to forward traffic from local port `9090` to local port `8080`. Run this in the background (e.g., `socat TCP-LISTEN:9090,fork TCP:127.0.0.1:8080 &`).

4. **Verification**:
   Retrieve the generated JSON file through the forwarded port by running `curl -s http://127.0.0.1:9090/users.json > /home/user/final_output.json`.

Ensure that `/home/user/final_output.json` contains the correctly formatted JSON array of the approved users.