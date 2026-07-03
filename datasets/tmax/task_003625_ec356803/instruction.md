You are an AI assistant tasked with cleaning up a heavily corrupted binary artifact repository for our CI/CD pipeline. Our backup scripts have been hanging indefinitely due to infinite symlink loops, and we've discovered that several artifacts are either deprecated or suffered network corruption during transfer.

You need to analyze three different data sources to determine which artifacts are safe to keep. There are 600 artifacts in total, labeled `art_000` through `art_599`.

An artifact is considered **VALID** only if it passes ALL three of the following checks:

1. **Structural Integrity (Directory Traversal)**
   The extracted contents of each artifact are located in `/home/user/artifact_store/art_<ID>/`. Some of these directories contain malicious or accidental symlink loops (e.g., `a -> b` and `b -> a`, or linking to a parent directory in a way that causes infinite recursion). You must identify and exclude any artifact whose directory contains a symlink loop.

2. **Administrative Status (Multi-line Log Parsing)**
   We have an administrative log file located at `/home/user/artifact_meta.log`. It contains multi-line records for each artifact. 
   Format example:
   ```
   [Artifact: art_015]
   Author: dev_team
   Checksum: 8a9d...
   Status: ACTIVE
   ---
   ```
   You must parse this file (using Python, sed/awk, or standard tools) and exclude any artifact whose Status is listed as `DEPRECATED`.

3. **Network Corruption (Video Frame Analysis)**
   During the mass upload, a hardware glitch caused network drops. We have a diagnostic video recording of the upload packets mapped to frames at `/app/artifact_feed.mp4`. 
   - The video contains exactly 600 frames. 
   - Frame indices correspond exactly to the artifact IDs (e.g., Frame 0 corresponds to `art_000`, Frame 1 to `art_001`, etc.).
   - A frame indicates a corrupted artifact if the 50x50 pixel block in the absolute top-left corner is predominantly red (specifically, the average pixel values in that 50x50 region must have Red > 200, Green < 50, and Blue < 50).
   - Use Python and `ffmpeg` (or `cv2` if installed/installable) to extract and analyze these frames. Exclude any artifact that shows this corruption.

**Your Deliverable:**
Once you have determined the valid artifacts, write their IDs (e.g., `art_042`), one per line, sorted in ascending order, to `/home/user/valid_artifacts.txt`. 

Your output will be scored programmatically based on the F1-score of your valid artifact list against the hidden ground truth. You must achieve an F1-score of >= 0.95 to pass.