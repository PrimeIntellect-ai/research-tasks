You are an operations engineer triaging a broken internal telemetry processing service.

We have a C-based daemon, `telemetry_parser`, that aggregates sensor data from network traffic. Recently, a new sensor type was deployed, and the service started reporting garbage values for variance (sometimes negative or `NaN`) and failing to parse records correctly.

The project is located in `/home/user/forensics`. You will find:
- `telemetry_parser.c`: The source code.
- `Makefile`: To build the project.
- `traffic.pcap`: A network capture containing a sample of the UDP telemetry traffic sent to port 9000.

Your investigation reveals two distinct issues:
1. **Format Parsing Bug:** The custom text-based protocol sends payloads in the format `[SENSOR_NAME] VALUE TIMESTAMP`. The previous sensors had names without spaces (e.g., `[TempSensor]`). The new sensor has spaces in its name (e.g., `[Pressure Sensor A]`). The current parsing logic breaks on names with spaces, causing fields to be read incorrectly or dropped.
2. **Numerical Instability:** The sensor values for this new type are very large with very small fluctuations (e.g., `1000000.01`, `1000000.03`). The current naive variance calculation ($E[X^2] - E[X]^2$) suffers from catastrophic cancellation, resulting in huge precision loss and returning invalid variances.

Your task:
1. Debug and modify `telemetry_parser.c` to correctly parse sensor names containing spaces.
2. Modify the variance calculation to use a numerically stable method (such as Welford's online algorithm or a robust two-pass method). Use `double` precision for all statistical accumulators. Sample variance should be calculated (divide by N-1).
3. Recompile the program using `make`.
4. Run the updated program on `traffic.pcap`.
5. The program should output the final aggregated statistics for the sensor. Redirect or write this exact output to `/home/user/forensics/report.txt`.

The format of `/home/user/forensics/report.txt` must be exactly:
```
Sensor: <Parsed_Sensor_Name>
Count: <Number_of_valid_records>
Mean: <Mean_value_to_2_decimal_places>
Variance: <Variance_value_to_4_decimal_places>
```
*(e.g., `Mean: 1000000.02`, `Variance: 0.0002`)*

Note: Do not install external libraries other than the standard C library and `libpcap` (which is already provided via standard package managers). You may need to install `libpcap-dev` if it is missing.