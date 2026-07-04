I am an engineer investigating a critical memory leak in our long-running video processing service. 

The source code for the service is located in a local Git repository at `/home/user/service_repo`. 
When running in production, the service crashes with an Out-of-Memory (OOM) error. I need your help to fix the service so it processes video streams reliably without unbounded memory growth.

Here is what you need to do:
1. **Recover the Configuration**: The script `video_processor.py` imports a secret API key from `config.py`. However, `config.py` was accidentally deleted in a recent commit, and the service currently crashes on startup. You need to use Git history forensics to find the lost API key and recreate `/home/user/service_repo/config.py`.
2. **Diagnose and Fix the Memory Leak**: Run the service on the test video fixture located at `/app/stream.mp4`. Use memory profiling tools (like `tracemalloc`) or trace intermediate states to identify why memory usage continuously grows per frame. Modify `video_processor.py` to fix the memory leak. 
3. **Verify Functionality**: Your patched code must process the entire video and output its analysis to `/home/user/results.json` without altering the core mathematical logic or final values calculated by the original implementation.

**Success Criteria:**
An automated suite will evaluate your solution by running:
`python /home/user/service_repo/video_processor.py /app/stream.mp4`

It will check that:
- The output in `/home/user/results.json` perfectly matches the expected results.
- The Peak Resident Set Size (RSS) during execution is **strictly less than 150 MB**. (The current buggy implementation scales linearly with the number of frames and will easily exceed 1GB).

Please investigate the repository, recreate the missing configuration, patch the leak, and ensure the script runs within the tight memory threshold.