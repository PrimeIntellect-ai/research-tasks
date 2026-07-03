You are a Site Reliability Engineer (SRE) investigating recurring crashes and bizarre metrics reported by your custom uptime monitoring service. 

The service, written in C, ingests UDP heartbeat packets from monitored servers, measures a simulated "latency" from the packet payloads, and calculates an Exponential Moving Average (EMA) of these latencies to monitor convergence.

However, two issues are occurring:
1. The service occasionally crashes with a Segmentation Fault or memory corruption when processing certain packets.
2. The EMA latency metric is completely wrong. Instead of converging to a stable average, the value blows up to infinity (convergence failure).

You have been provided with:
- The source code of the monitor: `/home/user/uptime_monitor.c`
- A packet capture of the traffic that triggers the crash: `/home/user/crash.pcap`

Your tasks:
1. Analyze the core logic in `/home/user/uptime_monitor.c`.
2. Identify and fix the boundary condition (off-by-one) error causing the buffer read overflow in the payload processing loop.
3. Identify and fix the formula implementation error in the Exponential Moving Average (EMA) calculation that prevents convergence. The standard EMA formula is `EMA_today = (alpha * value_today) + ((1 - alpha) * EMA_yesterday)`.
4. Recompile the program: `gcc -o uptime_monitor uptime_monitor.c -lpcap`
5. Run the compiled program against the packet capture: `./uptime_monitor /home/user/crash.pcap`
6. The program will print a `Final EMA: <value>` to standard output. Save ONLY the precise numeric output (exactly as formatted by the program, e.g., `42.1234`) to `/home/user/final_ema.txt`.

Do not modify the `alpha` value or the packet reading headers; only fix the bugs in the calculation loop and formula.