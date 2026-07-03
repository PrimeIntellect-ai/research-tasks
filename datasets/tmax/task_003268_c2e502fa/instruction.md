You are a network security engineer investigating a series of suspicious file uploads to your company's web application. The application accepts MP4 video uploads, but you suspect a threat actor is using these videos to bypass your firewall and deliver exploits to the backend, specifically targeting a path traversal vulnerability in the upload handler.

You have captured a highly suspicious video file at `/app/suspicious_upload.mp4`. 

Through preliminary traffic inspection, you believe the attacker is encoding binary files directly into the video frames. The encoding mechanism is suspected to be frame-color based:
- A predominantly RED frame (average R channel > 200, G < 50, B < 50) represents a binary `1`.
- A predominantly BLUE frame (average B channel > 200, R < 50, G < 50) represents a binary `0`.
- 8 frames make up a single byte (Big-Endian).
- The resulting bytes form a standard Linux ELF executable.

Your tasks are:
1. Extract the binary file hidden inside `/app/suspicious_upload.mp4` to a file named `/home/user/extracted_payload.elf`. Analyze it to understand the path traversal exploit it attempts to execute.
2. Develop a Python-based classifier script at `/home/user/classifier.py` that can automatically detect whether an uploaded video contains a malicious ELF payload. 
   - The script must take a single argument: the path to an MP4 file.
   - It must print `EVIL` to standard output if the video contains an ELF with a path traversal payload (e.g., attempting to access `/etc/passwd`, `/etc/shadow`, or using `../` sequences).
   - It must print `CLEAN` to standard output if the video contains a benign ELF or does not contain a valid ELF file.
   - The script must exit with code 0 in both cases.

We have provided a training/validation corpus of videos in `/app/corpus/`. 
Your `classifier.py` will be tested against two hidden directories in the automated grading environment.

Requirements:
- Do not use any external ML libraries; simple frame extraction (via `ffmpeg` or `cv2` if installed) and binary analysis (e.g., `strings`, `readelf`, or standard Python file reading) are sufficient.
- Save your final classifier to `/home/user/classifier.py`.