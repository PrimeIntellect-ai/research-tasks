You are a performance engineer tasked with optimizing and debugging a multi-threaded C application that processes high-frequency sensor data. 

In `/home/user/workspace`, you will find a C project consisting of `sensor_aggregator.c`, `Makefile`, and a large binary data file `data.bin`. 

The application reads sensor records from `data.bin` using multiple pthreads. Each record is 8 bytes:
- 1 byte: Magic header (`0xAA`)
- 2 bytes: Sensor ID (`uint16_t`, little-endian)
- 4 bytes: Sensor reading (`float`, little-endian)
- 1 byte: Checksum/Padding

The current implementation has three major bugs:
1. **Corrupted Input Handling**: Occasionally, `data.bin` contains corrupted sequences (missing the `0xAA` magic byte). The current parser simply prints an error and aborts the thread. You must modify the parser to recover by scanning forward byte-by-byte until it finds the next valid `0xAA` magic byte, and resume processing from there.
2. **Race Condition**: Multiple threads are accumulating data into a `global_sum` and `global_count` without proper synchronization, resulting in data races and incorrect totals. However, simply wrapping the global updates in a mutex kills performance. You must fix the race condition using thread-local accumulators that are only merged into the globals when a thread finishes.
3. **Precision Loss**: The application processes millions of `float` values. Because `global_sum` is a 32-bit `float`, it suffers from catastrophic precision loss (absorption) as the sum grows large. Upgrade the aggregation logic to use double-precision (`double`) for all accumulators and the final average calculation to fix this.

**Your Goal:**
1. Debug and modify `/home/user/workspace/sensor_aggregator.c` to fix the three issues above.
2. Recompile the application using `make`.
3. Run the application: `./sensor_aggregator ./data.bin`
4. Write the final computed total count and average into a file named `/home/user/workspace/metrics.log` in the exact following format:
`Total Count: <count>`
`Average Value: <average formatted to 4 decimal places>`

Ensure your final C code compiles without warnings and runs efficiently.