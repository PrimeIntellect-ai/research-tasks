You are an engineer debugging a failing CI pipeline. We have a Python script `/home/user/sensor_analyzer.py` that analyzes network packet captures (PCAPs) from IoT sensors. The script extracts numerical data from UDP packets on port 9999 and calculates the population standard deviation of the readings. 

Recently, the build pipeline started failing during the fuzz testing phase. There are two primary issues you need to resolve:
1. **Numerical Instability**: The fuzz test occasionally causes the script to crash with a `ValueError: math domain error`. This happens because of numerical instability / catastrophic cancellation in the naive variance calculation formula, which results in a slightly negative variance before the square root is taken.
2. **Statistical Anomalies**: Even when the script doesn't crash, the computed standard deviations are sometimes wildly incorrect. The sensor protocol specifies that the 4-byte payload is a **big-endian 32-bit signed integer**, but the parser might be mishandling the data type, causing negative sensor readings to appear as massive positive outliers.

Your objectives:
1. Fix the payload parsing bug in `/home/user/sensor_analyzer.py` to correctly interpret the data as signed 32-bit integers.
2. Fix the numerical instability in the variance calculation. You can rewrite the calculation to use a stable algorithm (like Welford's) or simply use a safer formulation that prevents negative variances from floating-point errors.
3. We have provided a test file at `/home/user/test.pcap`. Once you have fixed both bugs, run the analyzer on this file and redirect standard output to `/home/user/result.txt`.

Example command to generate the final output:
`python3 /home/user/sensor_analyzer.py /home/user/test.pcap > /home/user/result.txt`

The automated test will verify that the bugs are fixed and that the contents of `/home/user/result.txt` contain the correct standard deviation for the test PCAP. You can test your fixes locally using the provided `/home/user/fuzz.sh` and `/home/user/generate_fuzz.py` scripts.