You are an engineer investigating a critical issue in a long-running Python network service. The service analyzes network traffic and continuously calculates the population variance of packet lengths. Recently, the service has been crashing with `MemoryError` after running for several hours, and the metrics dashboard occasionally shows negative or highly inaccurate variance values when processing large baseline packet sizes (numerical instability).

The source code for the service is located at `/home/user/service/packet_processor.py`. 
A recent crash traceback is available at `/home/user/service/crash.log`.
A sample packet capture for testing is available at `/home/user/service/test_traffic.pcap`.

Your task is to:
1. Analyze the crash log and the source code to identify the memory leak and the numerical instability in the variance calculation.
2. Fix the Python script to resolve the memory leak (the service must use O(1) memory regarding the number of processed packets).
3. Fix the variance formula to be numerically stable (e.g., using Welford's online algorithm). Calculate the **population variance**.
4. Run your fixed script against the provided `/home/user/service/test_traffic.pcap` file.
5. Save ONLY the final calculated variance (rounded to 4 decimal places) into a file named `/home/user/solution.txt`.

Ensure your fixed script does not store the history of all packets and avoids catastrophic cancellation in its floating-point math.