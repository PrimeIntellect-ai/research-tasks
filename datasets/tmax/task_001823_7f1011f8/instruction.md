You are a DevOps engineer debugging a multi-service logging and metrics pipeline. 

We have a system consisting of three services located in `/home/user/app/`:
1. **Redis**: An intermediate cache service.
2. **Aggregator (`aggregator.py`)**: A Python service that receives JSON payloads from sensors over HTTP, parses them, updates a running calculation of the variance of the sensor readings in Redis, and serves the current variance on `GET /metrics`.
3. **Sensor Mock (`sensor.py`)**: A script that continuously sends sensor data to the Aggregator.

Currently, the system is failing in a few ways:
1. **Service Disconnection**: The Aggregator is failing to connect to Redis. You need to inspect the startup script `/home/user/app/start.sh` and the configuration in `aggregator.py` to ensure they are communicating on the correct ports.
2. **Format Parsing Edge-Cases**: The aggregator occasionally crashes or drops data. We captured the network traffic during a recent crash in `/home/user/app/traffic.pcap`. You must analyze this packet capture to understand the exact payload structures the sensors are sending. Some payloads have minor formatting anomalies (e.g., unexpected trailing commas, NaN representations, or scientific notation strings) that the current `json.loads` or manual parsing in `aggregator.py` does not handle. You must repair `aggregator.py` to robustly parse all formats seen in the pcap.
3. **Floating-Point Precision Loss**: The Aggregator uses a naive running sum of squares algorithm to calculate variance. Over time, catastrophic cancellation occurs, resulting in wildly inaccurate variance metrics. You need to replace the naive calculation in `aggregator.py` with a numerically stable algorithm (e.g., Welford's online algorithm).

**Your objective:**
1. Fix the service composition so Redis and the Aggregator communicate successfully.
2. Modify `/home/user/app/aggregator.py` to correctly parse all edge-case sensor formats present in `traffic.pcap`.
3. Fix the variance calculation logic in `/home/user/app/aggregator.py` to be numerically stable.

When you are done, ensure the services can be started via `/home/user/app/start.sh` without crashing, and that `aggregator.py` accurately tracks variance without floating point drift. 
An automated test will run your modified `aggregator.py` against a held-out dataset of 100,000 requests and compare its final computed variance against a high-precision reference. You must achieve a Mean Squared Error (MSE) of less than `1e-10`.