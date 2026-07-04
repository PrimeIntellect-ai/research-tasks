You are a security researcher analyzing a suspicious Go service that appears to intentionally leak goroutines during cancellation as part of a denial-of-service payload. 

You have three objectives:

**Objective 1: Repair the Video Extraction Environment**
You have been provided a custom Python package at `/home/user/ocr_extractor` that performs fast text extraction from video frames. However, the package currently fails to install due to compiler and linker errors in its C-extension (it is failing to link against the math library and has a misconfigured include path).
1. Diagnose and fix the misconfiguration in `/home/user/ocr_extractor/setup.py`.
2. Successfully install the package in your environment using `pip install -e /home/user/ocr_extractor`.

**Objective 2: Video Debugging and Analysis**
There is a screen recording of the malware's execution in the terminal located at `/app/suspicious_execution.mp4`. 
1. Use `ffmpeg` to extract the frames from this video.
2. Use the repaired `ocr_extractor` module to parse the text from the frames. The module provides a CLI: `python -m ocr_extractor <image_path>`.
3. Identify the exact frame number where the phrase "goroutine leak triggered at" first appears, and extract the hex memory address associated with it.
4. Save your findings in `/home/user/video_analysis.json` with the exact format:
```json
{
  "frame_number": 142,
  "leak_address": "0x0000000"
}
```

**Objective 3: Adversarial Log Classifier**
Based on your analysis, you need to build a regression test / detector to classify log files. 
You are provided with a small sample of training data:
- `/app/training_data/evil/` (Logs where the malicious cancellation leak occurs)
- `/app/training_data/clean/` (Logs of normal Go service execution, including benign panics)

Write a Python script at `/home/user/detector.py` that takes a single file path as a command-line argument.
- It must print exactly `MALICIOUS` to standard output if the log exhibits the malicious goroutine leak.
- It must print exactly `BENIGN` to standard output if the log is normal.
- We will evaluate `/home/user/detector.py` against a hidden adversarial corpus.

Your script must accurately distinguish the root cause (malicious cancellation leaking goroutines) from normal application errors.