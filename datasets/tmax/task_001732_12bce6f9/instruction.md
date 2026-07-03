You are an engineer investigating a severe memory leak in a long-running Go service used for mathematical video analysis. 

The service codebase is located in `/app/math-vid-service`. It extracts frames from a video file, computes a running spatial frequency matrix per frame, and serializes these metrics to disk. 

Currently, there are two major issues:
1. **Memory Leak**: The service consumes an ever-increasing amount of memory as it processes frames, quickly leading to OOM on longer videos. Trace the intermediate states (e.g., using `pprof`), identify the root cause of the memory leak in the Go code, and fix it.
2. **Corrupted Serialization**: A recent commit broke the binary encoding of the output metrics. Use git history forensics in the `/app/math-vid-service` repository to find the original, correct encoding logic (which used Go's `encoding/binary` properly) and restore it.

Once you have fixed the code, build the application and run it against the provided video artefact: `/app/input_video.mp4`. 

You must output the final serialized mathematical metrics to exactly: `/home/user/metrics.bin`. 

Your solution will be evaluated based on:
1. The mathematical accuracy of the output file compared to a reference standard.
2. The peak memory consumption of your fixed service while processing the full video.