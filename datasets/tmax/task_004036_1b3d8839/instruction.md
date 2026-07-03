You are tasked with debugging a failing build for our drone vision pipeline. 

The project is located in `/home/user/vision_pipeline/`. If you run `make test`, you will notice that the test suite hangs indefinitely. This is a multi-threaded C program that processes raw image data to calculate a statistical "anomaly score" for each frame. 

Your objectives are:
1. **Fix the Deadlock:** Use system call tracing (e.g., `strace`) or standard debugging tools to identify why the test suite is hanging. Fix the synchronization bug in the C code so that `make test` completes.
2. **Fix the Formula Implementation:** Even after fixing the deadlock, the tests will fail because the computed anomaly scores are incorrect. Read `/home/user/vision_pipeline/README.md` for the exact mathematical formula. Identify the statistical anomaly calculation bug in the C code and correct it. The program must compile to `/home/user/vision_pipeline/bin/scorer` and cleanly pass `make test`.
3. **Video Analysis:** We have a test flight video located at `/app/drone_feed.mp4`. Use `ffmpeg` to extract the frames from this video as raw 64x64 grayscale images (e.g., using `-s 64x64 -f rawvideo -pix_fmt gray`). 
4. **Integration:** Pipe each extracted raw frame into your fixed `/home/user/vision_pipeline/bin/scorer` program. The program reads exactly 4096 bytes from `stdin` and writes a single 32-bit floating point number (the anomaly score) formatted as a text string to `stdout`. 
5. Find the 1-based index of the frame (e.g., 1 for the first frame, 2 for the second) that produces the highest anomaly score. Write this exact integer to a file named `/home/user/max_anomaly_frame.txt`.

Ensure your final compiled binary at `/home/user/vision_pipeline/bin/scorer` is strictly equivalent to the correct mathematical formulation, as it will be rigorously verified against an oracle using random binary fuzzing.