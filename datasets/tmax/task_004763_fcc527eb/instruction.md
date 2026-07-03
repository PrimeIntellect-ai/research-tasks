You are a data engineer responsible for analyzing pipeline telemetry and enforcing best practices in machine learning ETL workflows. Your task involves two primary objectives:

**Part 1: Video Telemetry Extraction**
An automated pipeline monitoring system has generated a visual telemetry log: `/app/telemetry.mp4`. We use visual markers to track pipeline restarts. A "restart" is defined as a frame that is completely red (average Red channel value > 250, Green < 10, Blue < 10). 
Use standard tools (like `ffmpeg` and python) to analyze the video and count the total number of restart frames. 
Save this integer count to `/home/user/restart_count.txt`.

**Part 2: Data Leakage Detector**
Junior engineers frequently introduce data leakage by applying scaling transformations (like `fit_transform` or `fit`) on the entire dataset *before* splitting it into training and testing sets. 
You must build a static analysis tool or regex-based detector to catch this.

Write a bash script at `/home/user/check_leakage.sh` that takes a single Python file path as an argument:
`bash /home/user/check_leakage.sh <path_to_python_script.py>`

The script must:
1. Exit with code `0` (Success) if the pipeline is "clean" (i.e., `train_test_split` occurs *before* any scaler's `fit` or `fit_transform` method is called on the data).
2. Exit with code `1` (Failure) if the pipeline is "evil" / leaking (i.e., a scaler's `fit` or `fit_transform` is called on the full dataset variable *before* `train_test_split` is used).

Your script will be tested against a hidden adversarial corpus of dozens of clean and evil pipeline scripts. You must ensure 100% of the clean scripts exit with 0, and 100% of the evil scripts exit with 1. 

**Deliverables:**
- `/home/user/restart_count.txt` containing the video frame count.
- `/home/user/check_leakage.sh` functioning as a leakage detector executable.