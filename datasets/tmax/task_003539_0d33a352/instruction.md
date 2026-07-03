You are stepping in for a senior systems engineer who left unexpectedly. Before they left, they were setting up a custom user-level systemd service (`health-monitor.service`) to perform network health checks, process monitoring, and disk storage monitoring. However, the service currently fails to start.

The previous engineer left a voice memo detailing the secret authorization token required by the service's configuration. The voice memo is located at `/app/voicemail.wav`.

Your objectives are as follows:

1. **Audio Extraction**: Transcribe the audio file at `/app/voicemail.wav` to retrieve the 6-digit authorization token.
2. **Service Diagnosis & Fix**: The systemd user service is located at `/home/user/.config/systemd/user/health-monitor.service`. It fails to start. Diagnose the issue, update the configuration file `/home/user/monitor_config.ini` with the correct token from the audio file, and ensure the service can start successfully.
3. **C Code Optimization**: The daemon's source code is located at `/home/user/src/monitor.c`. It currently implements the disk quota and process monitoring checks very inefficiently, taking over 5 seconds per iteration. You must optimize the C code so that the execution time for a full check iteration is significantly reduced. You are allowed to rewrite the monitoring logic in `monitor.c` using standard C libraries, as long as it still outputs the exact same health check JSON format to `/home/user/health_status.json`.
4. **Compile & Deploy**: Compile your optimized C program to `/home/user/bin/monitor` and restart the systemd service.

**Evaluation:**
An automated testing script will evaluate your solution. The test will measure the execution speedup of your optimized binary against the original unoptimized binary. You must achieve a speedup metric of >= 5.0x (meaning your program must run at least 5 times faster than the original). The output file `/home/user/health_status.json` will also be checked for correctness.