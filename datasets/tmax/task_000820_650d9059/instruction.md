You are an operations engineer triaging a critical incident in our data pipeline. Over the last 24 hours, our legacy data processing service has experienced massive latency spikes, and some data payloads are getting corrupted during serialization. 

We need you to investigate the logs, reproduce the issue, and deploy a repaired, optimized C-based replacement.

Here is the current state of the system:
1. **Logs**: Unordered log files from three microservices are located in `/home/user/logs/`.
2. **Data**: The raw data dumps being processed are in `/home/user/data/raw_payloads.bin`.
3. **Legacy Processor**: The current production binary (stripped of debug symbols) is located at `/app/legacy_processor`. It reads raw binary data from `stdin` and writes a custom serialized hex string to `stdout`.
4. **New Processor Source**: A colleague started writing a replacement in C at `/home/user/src/fast_processor.c`. It currently fails to compile, has linker errors, contains failing assertions, and is extremely slow.

Your objectives:
1. **Log Reconstruction & Anomaly Detection**: Use bash text-processing tools to reconstruct a chronological timeline across all logs in `/home/user/logs/`. Identify the specific payload `chunk_id` that is causing processing times to exceed 5000ms. Write the anomalous `chunk_id` to `/home/user/anomalous_chunk.txt`.
2. **Serialization Troubleshooting**: Analyze how `/app/legacy_processor` serializes data. It applies a simple proprietary encoding before converting the output to hex.
3. **Fix the C Code**: 
   - Fix the compiler and linker errors in `/home/user/src/fast_processor.c`.
   - Fix the assertion failures related to the encoding logic so its output exactly matches `/app/legacy_processor` for any given input.
4. **Performance Optimization**: The current `fast_processor.c` implementation has a severe bottleneck. Optimize the C code so that it significantly outperforms the legacy binary.
   
**Success Criteria**:
- `/home/user/anomalous_chunk.txt` contains the correct `chunk_id`.
- You produce a compiled binary at `/home/user/src/fast_processor`.
- For any arbitrary binary input, `/home/user/src/fast_processor` must produce the exact same standard output as `/app/legacy_processor`.
- Your optimized binary must achieve a **speedup of at least 5.0x** compared to `/app/legacy_processor` when processing the entire `/home/user/data/raw_payloads.bin` file.

Do not use any external third-party C libraries; only standard POSIX libraries are permitted.