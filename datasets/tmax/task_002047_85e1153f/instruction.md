**URGENT: 3AM PagerDuty Alert - Drone Object Tracking Pipeline Down**

Hey, sorry to wake you up. Our automated drone tracking pipeline just went down in production and we need an emergency fix. The processing pipeline uses a custom visual tracking algorithm, but it's currently crashing on the latest payload video. 

The video artefact is located at `/app/drone_tracking.mp4`. 

The tracking script is at `/home/user/tracker/track.py`. It is supposed to extract frames using `ffmpeg` or `cv2`, run our custom recursive contour-matching and mean-shift algorithm, and output a JSON file containing the bounding box coordinates of the primary target for each frame. 

Currently, the script is completely locking up and timing out. Preliminary logs suggest it's hitting an infinite recursion or failing to converge on certain frames. We suspect some frames in this video payload are heavily corrupted (e.g., pure static or dropped packets), which our algorithm wasn't built to handle, causing the convergence loop to spin forever.

Your tasks:
1. Diagnose and fix the infinite loop / recursion issue in `/home/user/tracker/track.py`. Ensure the optimization algorithm actually terminates.
2. Implement handling for the corrupted frames. If a frame is corrupted (e.g., variance is extremely low or high noise), the script should detect this, recover gracefully, and interpolate the bounding box from the previous frames rather than crashing.
3. Add a regression test in `/home/user/tracker/test_tracker.py` that isolates the recursive optimization function and asserts it terminates within 50 iterations even with garbage data.
4. Run your fixed script on `/app/drone_tracking.mp4` to produce the final output at `/home/user/tracker/output.json`. 

The output JSON MUST be a list of lists representing the bounding box per frame (0-indexed). Format: `[[x, y, width, height], [x, y, width, height], ...]`.

The pipeline needs to be highly accurate. The output will be evaluated against a hidden ground-truth set of bounding boxes using Average Intersection over Union (IoU). You need to achieve an Average IoU >= 0.85 across all frames to resolve this incident. Good luck, the incident bridge is waiting.