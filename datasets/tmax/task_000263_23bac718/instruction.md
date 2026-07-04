You are a forensic developer tasked with debugging a critical telemetry extraction pipeline. We have a Go service called `meta-extractor` located at `/home/user/meta-extractor` that is supposed to parse binary telemetry data. However, the service is currently broken.

Your objectives are:

1. **Fix the Build:**
   The `meta-extractor` service currently fails to compile. Inspect the source code in `/home/user/meta-extractor`. You will need to diagnose the build failure, which involves fixing a precision loss error during timestamp conversion and an off-by-one boundary condition in the payload parser. Fix the code so it successfully compiles using `go build`.

2. **Build a Malicious Payload Detector:**
   Even when compiled, `meta-extractor` has a known vulnerability: it leaks goroutines and eventually crashes when processing specific malformed telemetry payloads. We have isolated samples of these payloads.
   - Clean payloads are located in `/home/user/corpus/clean/`.
   - Malicious payloads (which trigger the leak) are in `/home/user/corpus/evil/`.
   
   You must write a standalone Go program at `/home/user/detector.go` and compile it to `/home/user/detector`. 
   This tool will act as a filter. It must accept a single command-line argument (the path to a payload file).
   - If the file is safe/clean, it must exit with status code `0`.
   - If the file is malicious/evil, it must exit with status code `1`.
   Your detector must correctly classify 100% of both the clean and evil files.

3. **Video Forensics:**
   We have recovered a corrupted surveillance video at `/app/evidence.mp4`. The video contains flashes of solid red frames (RGB 255, 0, 0) inserted by the attacker to encode a sequence. 
   Use `ffmpeg` (which is preinstalled) to extract the frames. Analyze the frames and count the exact number of completely solid red frames in the video.
   Write the final integer count to `/home/user/red_frame_count.txt`.

Ensure your detector binary is built and the `red_frame_count.txt` file is present when you finish.