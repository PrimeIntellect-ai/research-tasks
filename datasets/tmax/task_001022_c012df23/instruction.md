**PagerDuty Alert - 03:14 AM - CRITICAL**
**Service:** `audio-anomaly-detector`
**Host:** `forensics-prod-01`
**Description:** The emergency acoustic processing pipeline is segfaulting on incoming audio artifacts. The latest failing artifact has been isolated to `/app/incident_809.wav`.

You are the on-call engineer. The pipeline consists of a Python wrapper (`/home/user/service/pipeline.py`) that calls a highly optimized C++ library (`/home/user/service/audio_ops.cpp`) to compute an acoustic anomaly score. 

**Your objectives:**
1. **Diagnose the crash:** Run `python /home/user/service/pipeline.py /app/incident_809.wav`. It currently produces a core dump or segfault.
2. **Fix the C++ code:** Inspect `audio_ops.cpp`. There is a memory/pointer boundary bug in the formula implementation calculating the RMS energy and an assertion failure that triggers on certain file sizes. Fix the bounds check and the arithmetic. 
3. **Resolve compilation issues:** The provided `build.sh` script in the directory is failing due to a linker error (undefined references to math functions). Fix the build script so `libaudio.so` compiles successfully.
4. **Run the pipeline:** Once fixed and rebuilt, process `/app/incident_809.wav` through `pipeline.py`. 
5. **Output Verification:** The script will automatically generate `/home/user/service/anomaly_score.txt` containing a single floating-point number.

Do whatever it takes to fix the pipeline and generate the correct anomaly score for the incident audio.