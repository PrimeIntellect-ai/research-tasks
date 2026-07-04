You have just inherited a legacy telemetry aggregation system for an industrial IoT setup. The system receives data from three different sensors over local network sockets, aggregates the data, and computes a rolling standard deviation of the temperature readings.

The code is located in `/home/user/sensor_net/`.
To start the system, you normally run `/home/user/sensor_net/start.sh`, which launches the 3 simulated sensor nodes and the `aggregator.py` process.

However, the aggregator consistently crashes within a few seconds of starting. The previous developer left some notes:
1. "Sometimes the aggregator just spits out Unicode errors and dies. I think one of the newer sensors might be sending weirdly encoded data, but I'm not sure which one."
2. "Occasionally, even when the encoding is fine, the aggregator crashes with a `math domain error`. I suspect one of the sensors is sending anomalous, massive statistical outliers that cause floating-point precision issues in our naive standard deviation formula (leading to a negative variance). We need to filter out any temperature readings that are outside the valid range of 0.0 to 100.0 *before* adding them to the rolling window."

Your task is to debug and fix `aggregator.py` so that it runs stably. 

Specific Requirements:
1. Identify and handle the encoding serialization issue. Some sensors may send data in `utf-8`, while others might send it in `utf-16le`. Your `aggregator.py` must decode the JSON payloads successfully regardless of which of these two encodings is used.
2. Fix the statistical anomaly crash. Add a filter in `aggregator.py` to silently drop any parsed JSON messages where the `"value"` is less than `0.0` or greater than `100.0`.
3. Do not change the files `sensor1.py`, `sensor2.py`, or `sensor3.py`. You must only fix `aggregator.py`.
4. Once fixed, run the system using `./start.sh` for at least 5 seconds. The aggregator should successfully write its periodic aggregated metrics to `/home/user/sensor_net/output/metrics.log`.

Verification:
The automated test will run your modified `aggregator.py` alongside the sensors for 10 seconds. It will parse `/home/user/sensor_net/output/metrics.log` to ensure:
- It contains at least 5 successful rolling window calculations.
- No values outside the 0.0-100.0 range were included in the calculations.
- The `aggregator.py` script exits cleanly or stays running without crashing.