**URGENT: 3AM PAGE - EDGE SURVEILLANCE NODE OOM OUTAGE**

You are the on-call edge infrastructure engineer. Our C-based surveillance daemon (`videod`) running on remote edge nodes is experiencing massive memory leaks leading to OOM (Out Of Memory) kills. The crashes started recently after a series of upstream merges.

We've captured the exact video payload that triggers this rapid memory exhaustion. It has been saved to the node at `/app/incident_stream.mp4`. 

You have access to the daemon's source code in the local Git repository at `/home/user/videod_repo`. 
- The tag `v1.0` is known to be perfectly stable and does not leak memory.
- The current `HEAD` (master) is leaking heavily when processing `/app/incident_stream.mp4`.

**Your Mission:**
1. **Isolate the Regression:** Use Git bisection to identify the commit that introduced the memory leak. 
2. **Reverse Engineer & Diagnose:** Analyze the faulty commit. You will find an issue where a specific frame condition (simulating a dark frame anomaly or cancellation) triggers an error path. 
3. **Correct the Implementation:** 
   - Fix the resource leak in the error path.
   - You will also notice the faulty commit introduced a typo in the YUV Luma (Brightness) calculation formula. The correct industry standard formula is `Y = 0.299*R + 0.587*G + 0.114*B`. Correct this formula in the C code so that legitimate frames are not falsely flagged as anomalies.
4. **Deploy and Verify:** Recompile the daemon (`make` is provided) and ensure it can process `/app/incident_stream.mp4` successfully.
5. **Output Requirement:** Run the fixed binary on the video file and pipe the standard output to `/home/user/processed_frames.log`.

The automated system will verify your fix by running your compiled binary (`/home/user/videod_repo/videod`) against the incident video. The maximum resident set size (Peak RSS memory) must be strictly below 15,000 KB (15 MB), proving the leak under the error path has been completely resolved.