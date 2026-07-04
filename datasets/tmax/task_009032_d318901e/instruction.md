I am a capacity planner analyzing resource usage on our local storage. I need you to set up a monitoring endpoint for a specific directory, manage its access, and expose the metrics via a forwarded port. 

Please perform the following tasks:
1. Ensure the directory `/home/user/shared_data` has a specific Access Control List (ACL) entry: grant the user `nobody` read and execute permissions (`r-x`). 
2. Create a monitoring script (you can use Python or Node.js) at `/home/user/monitor.py` (or `.js`). The script must calculate the total disk usage in bytes of `/home/user/shared_data` (recursively including all files).
3. The script should start an HTTP server on `127.0.0.1:9090`. When a `GET /` request is received, it must return a JSON response exactly in this format: `{"usage_bytes": <integer>}`.
4. Run this monitoring script in the background.
5. Set up local port forwarding to forward TCP port `8080` to your HTTP server on port `9090`. You may use `socat` or any standard port forwarding tool available in user space. Run this in the background as well.
6. Verify your setup by querying the forwarded port (`http://127.0.0.1:8080/`) and save the exact JSON output to `/home/user/capacity_report.json`.
7. Finally, run `getfacl /home/user/shared_data` and save its output to `/home/user/acl_report.txt`.

Ensure all background processes are running and the files `/home/user/capacity_report.json` and `/home/user/acl_report.txt` are created with the correct information.