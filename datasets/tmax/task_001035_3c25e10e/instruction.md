Wake up! It's 3:00 AM and you are on-call. 

The new "FastMath" aggregation service in our production pipeline is repeatedly crashing with a core dump. We've managed to capture a snippet of the network traffic hitting the service right when the crashes occur, saved at `/home/user/traffic.pcap`.

The worker process is a Python script located at `/home/user/math_worker.py`. In production, a reverse proxy extracts the JSON body from incoming UDP packets and pipes it directly into the standard input of this script.

Your objectives:
1. **Analyze the PCAP**: Extract the JSON payloads being sent to the service (UDP port 8080).
2. **Reproduce the Crash**: Identify which of the payloads causes `/home/user/math_worker.py` to abort. You may want to use `strace` or analyze the script to understand how it fails.
3. **Minimize the Payload (Delta Debugging)**: The crashing payload contains a large array of integers under the `"data"` key. Reduce this array to the absolute minimum elements (smallest subset of the array) that still cause the script to predictably abort. 
4. **Report**: Save this minimal reproducible payload to `/home/user/minimal.json`. The file must contain valid JSON in the exact format `{"data": [x, y, z, ...]}`. To ensure deterministic verification, **sort the integers in the array in ascending order**.

You have a standard Linux environment. You can use any tools or write any helper scripts you need to accomplish this task.