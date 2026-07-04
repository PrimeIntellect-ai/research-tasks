Wake up, you're on-call and we just got a Sev-2 page at 3:00 AM. Our nightly video processing pipeline is completely down.

Here is the situation:
1. **Anomaly Detection**: A security camera recorded an incident, located at `/app/incident.mp4`. The pipeline failed to identify the anomalous frame. You need to extract the frames from this video (at 1 fps is fine, or all frames if it's short), calculate the mean grayscale pixel intensity of each frame, and find the frame index (0-indexed) with the largest statistical anomaly (highest absolute z-score of mean intensity). Write this frame index to `/home/user/anomaly_frame.txt`.

2. **Build Failure**: The source code for our new `event_parser` is in `/home/user/src/`. The build script `build.sh` is failing mysteriously. You will need to diagnose the build failure (hint: you might need to trace its system calls to see what file or dependency it's silently failing to find or what it's trying to execute). Fix the build process so that it successfully compiles to `/home/user/event_parser`.

3. **Logic Replication**: The new `event_parser` has some missing logic. We have the old, unreadable legacy binary at `/app/legacy_parser`. Your final `/home/user/event_parser` must behave **exactly** identically to `/app/legacy_parser` when given the same command-line arguments. The executable takes a single hex-encoded string as an argument and prints a processed result to standard output. Use whatever debugging or tracing tools you need on `/app/legacy_parser` to figure out its internal logic and implement it in the new source code. 

To resolve the page:
- Write the anomalous frame index to `/home/user/anomaly_frame.txt`.
- Produce the fully correct compiled binary at `/home/user/event_parser`. Our automated verification system will extensively fuzz your `/home/user/event_parser` against `/app/legacy_parser` with random hex strings to ensure bit-exact equivalence.