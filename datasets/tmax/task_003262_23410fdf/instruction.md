You are a release manager tasked with auditing a recent deployment. The deployment pipeline generates a video audit log where each frame contains cryptographically encoded deployment telemetry in its top row of pixels.

Your goal is to build an automated pipeline that extracts this telemetry, parses the structured data, and checks the deployed component versions against a required manifest.

Here are your steps:

1. **Fix the Extractor:**
   In `/app/extractor/`, there is a C project designed to read a `.bmp` image and decode the telemetry hidden in the red channel of the first row of pixels.
   - The `Makefile` is broken and fails to build.
   - The `decoder.c` has a memory management bug causing segfaults on certain frames.
   Fix the C project so it compiles into `./decoder` and runs cleanly.

2. **Process the Video Audit Log:**
   The audit video is located at `/app/deploy_capture.mp4`.
   Use `ffmpeg` (which is pre-installed) to extract the frames as `.bmp` files.
   Process each frame using your fixed C `decoder`. 
   The decoder outputs a JSON string for frames containing telemetry (e.g., `{"component": "auth-service", "version": "1.4.2-beta"}`). Some frames have no telemetry and output nothing.

3. **Semantic Version Validation:**
   You are provided with a minimum required version manifest at `/app/manifest.json`.
   Write a script (in Python or Bash) that collects all telemetry from the frames.
   For each component found in the video telemetry, compare its deployed version to the minimum required version in the manifest using semantic versioning rules.
   
4. **Generate the Report:**
   Create a final report at `/home/user/report.json` with the following structure:
   ```json
   {
     "outdated_components": [
       "auth-service",
       "payment-gateway"
     ]
   }
   ```
   A component is "outdated" if its deployed version is strictly less than the minimum required version in `/app/manifest.json`.

Ensure your entire extraction and validation workflow can be run programmatically. The accuracy of your `report.json` will be evaluated against the ground-truth hidden data.