You are investigating a memory leak and infinite loop issue in our video processing service. The service parses custom metadata logs extracted from videos, but occasionally hangs or exhausts memory due to malformed edge cases in the logs.

Your task has two parts:
1. Video analysis: We have a video file located at `/app/test_video.mp4`. Use `ffprobe` to extract the duration of the video (in seconds) and save it to `/home/user/video_duration.txt` (just the number).
2. Adversarial Filter: We need a sanitiser to protect our backend. Write a C++ program at `/home/user/filter.cpp` and compile it to `/home/user/filter`. 
   - The program must take a single command-line argument: the path to a text file.
   - It must read the file and determine if it is a "clean" log or an "evil" log (which contains the malformed syntax that causes our parser to infinite-loop/leak).
   - If the file is clean, the program must exit with code `0`.
   - If the file is evil, the program must exit with code `1`.
   
We have provided sample files in `/app/corpus/clean/` and `/app/corpus/evil/`. You can inspect these files to identify the anomaly (e.g., nested structures or format parsing edge cases) that differentiates them. Your filter must not crash, leak memory, or loop infinitely on any input.

Requirements:
- Your filter must be compiled to `/home/user/filter`.
- Do not use external C++ libraries beyond the standard library.
- `/home/user/video_duration.txt` must contain exactly the video duration.