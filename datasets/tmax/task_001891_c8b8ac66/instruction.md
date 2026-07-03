You are an observability engineer tasked with fixing and tuning a custom C++ metrics backend that sits behind a routing layer. The routing layer currently returns a 502 error because it cannot connect to the backend's UNIX socket.

There is a topology diagram located at `/app/topology.png`. This image contains handwritten notes from the lead architect specifying:
1. The correct UNIX socket path that the C++ backend should bind to.
2. The specific Timezone required for the dashboard timestamps.

Your tasks are as follows:

1. **Investigate the Topology**: Read `/app/topology.png` (you can use preinstalled tools like `tesseract`) to find the required socket path and timezone.
2. **Fix the Router Config**: Update the router configuration file at `/home/user/router.conf`. It currently points to `/tmp/wrong.sock`. Change it to the socket path found in the image.
3. **Fix and Optimize the C++ Backend**: 
   - The C++ source code is located at `/home/user/backend/server.cpp`.
   - Update it to bind to the correct UNIX socket.
   - The server currently parses incoming metric strings very inefficiently (it uses pass-by-value for large strings in a tight loop). Optimize the `process_metric` function so it can handle high throughput.
   - Ensure the server uses the timezone specified in the image when it processes time. You can enforce this by setting the `TZ` environment variable in the shell before launching the compiled server, or configuring it in the code.
4. **Compile and Run**: Compile the backend using `g++ -O3 server.cpp -o server` and start it in the background.
5. **Generate an Alert Report**: The router has a simulated error log at `/home/user/router_error.log`. Use `awk` and `grep` to extract all lines containing "502 Bad Gateway" and write them to `/home/user/502_report.txt`. 
6. **Secure the Report**: Use ACL or `chmod` to set `/home/user/502_report.txt` strictly to read-only for the owner (0400).

To pass the verification, the C++ backend must successfully process the load test with an average processing time under a specific threshold, and the router must successfully connect to the socket.

Run `/home/user/benchmark.sh` to test your setup. It will output the time taken to process 10,000 metrics. Ensure your backend is running before executing this.