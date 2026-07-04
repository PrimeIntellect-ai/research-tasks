You are a performance engineer tasked with debugging a statistical analysis tool that processes network telemetry.

You are provided with a packet capture file at `/home/user/telemetry.pcap` and a Go program at `/home/user/statscalc/main.go`.

The pcap file contains UDP traffic. Some of this traffic is telemetry data sent to destination port 9000. The payload of each UDP packet sent to port 9000 is a single 4-byte IEEE 754 single-precision float (float32) in Big-Endian format, representing a sensor reading.

The current Go program `main.go` reads string representations of these floats from standard input (one per line) and calculates the population standard deviation. However, it suffers from numerical instability due to catastrophic cancellation (it uses the naive sum of squares method with `float32`), which causes the variance to occasionally become negative and results in a `NaN` standard deviation.

Your tasks:
1. Extract the UDP payloads destined for port 9000 from `/home/user/telemetry.pcap`. You can use standard tools like `tcpdump` or `tshark` to extract the hex payloads.
2. Update `/home/user/statscalc/main.go` to read the hex strings (e.g., "41200000") from standard input, decode them into `float32` values, and compute the population standard deviation.
3. Fix the numerical instability in `main.go` by implementing Welford's online algorithm for calculating variance. Ensure your calculations use `float64` internally for precision.
4. Add intermediate assertion-based validation in your Go code to panic if the computed variance ever drops below 0.
5. Run your modified Go program using the extracted payloads as input.
6. Save the final calculated population standard deviation, rounded to exactly 4 decimal places (e.g., `0.1234`), to `/home/user/solution.txt`.

Ensure your Go code compiles and runs successfully. Do not use external Go libraries outside the standard library.