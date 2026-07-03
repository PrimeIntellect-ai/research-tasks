You are an IT support technician tasked with resolving Ticket #8841. 

**Ticket Context:**
Our IoT sensor data pipeline container has been crashing intermittently, and the downstream analytics team reports severe precision loss in the calculated averages before the crashes occur. 

We have isolated a packet capture of the incoming traffic (`/home/user/ticket_8841/traffic.pcap`) and the processing script used inside the container (`/home/user/ticket_8841/process_data.sh`). There is also a partial container log (`/home/user/ticket_8841/container.log`) showing the error output before the crash.

**Your objectives:**

1. **Extract the Data:** The sensors send ASCII text payloads over UDP port 8080. Use `tshark` (or similar tools) to extract just the ASCII text payload from the UDP packets in `/home/user/ticket_8841/traffic.pcap`. Save the raw extracted text to `/home/user/ticket_8841/extracted_payloads.txt`.
   - Each extracted payload should be on a new line.
   - The payload format is `SENSOR_ID,VALUE` (e.g., `S1,45.67`).

2. **Debug and Fix the Script:** The script `/home/user/ticket_8841/process_data.sh` is supposed to read the extracted payloads, track intermediate states, and calculate the exact average for each `SENSOR_ID`. 
   - Analyze the script and the `container.log` to fix the cause of the container crash (it currently fails when it encounters malformed or empty network payloads).
   - Fix the precision loss bug. The script currently truncates decimal values during its internal calculations, causing severe precision loss. The final averages must be accurate to exactly 2 decimal places (e.g., `45.67`).

3. **Generate Final Output:** Run your fixed `process_data.sh` using `/home/user/ticket_8841/extracted_payloads.txt` as the input. 
   - The script must output the corrected averages to `/home/user/ticket_8841/final_averages.txt`.
   - The format of `final_averages.txt` must be one sensor per line: `SENSOR_ID:AVERAGE` (e.g., `S1:42.50`), sorted alphabetically by SENSOR_ID.

Ensure your fixed bash script handles intermediate state tracing cleanly (if it uses temporary files, ensure they don't cause subsequent runs to fail or calculate incorrectly).