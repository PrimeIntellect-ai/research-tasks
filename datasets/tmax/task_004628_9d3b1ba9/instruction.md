You are assisting a technical writer in organizing and preparing documentation for an upcoming open-source software release. You need to process a video tutorial to extract figures, and create a security filter to prevent internal leaks in the written documentation.

**Part 1: Video Figure Extraction**
There is a tutorial video located at `/app/tutorial.mp4`. 
The technical writer has provided a metadata file at `/home/user/metadata.json` containing an array of timestamps where important UI screens are shown. 
1. Parse the `/home/user/metadata.json` file.
2. For each timestamp listed in the `extract_frames` array, use `ffmpeg` to extract a single frame.
3. Save these frames as JPEG images in `/home/user/docs/images/`. Name them `figure_1.jpg`, `figure_2.jpg`, etc., corresponding to the chronological order of timestamps in the JSON.
4. The output JPEGs must be standard 24-bit color, without any exotic compression.

**Part 2: Documentation Leak Detector**
The writer has hundreds of markdown files, but some draft files accidentally contain internal corporate server names or hardcoded test credentials. 
You must write a command-line leak detection script at `/home/user/docs/leak_detector.py` (or `.sh`, `.rb`, etc. - your choice of language).

Your script must take exactly one argument: the absolute path to a text file.
It must read the file and search for the following proprietary patterns:
1. Internal API endpoints of the exact format: `api.internal.corp:8080/vX` (where X is any single digit from 1 to 9).
2. Hardcoded test credentials of the format: `test_user_YYYY:ZZZZZZZZZZZZ` (where YYYY is any sequence of lowercase letters, and ZZZZZZZZZZZZ is exactly 12 alphanumeric characters).

**Detector Requirements:**
* If the file contains ONE OR MORE of these patterns, your script must exit with status code `1` (Reject).
* If the file does NOT contain any of these patterns, your script must exit with status code `0` (Accept).
* Your script must run cleanly and quietly (standard output/error is ignored, only the exit code matters). Ensure it has executable permissions (`chmod +x`).

The automated verification will run your script against a hidden test suite of clean and contaminated documentation files.