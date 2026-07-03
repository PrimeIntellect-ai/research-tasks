You are a Machine Learning Engineer preparing a telemetry dataset for a new predictive maintenance model. Unfortunately, our data lake has been polluted with corrupted and synthetic data, and you need to build an automated filter to separate the good data from the bad.

You have been provided with a calibration video and a database of secondary sensor readings. The true physical relationship between our sensors is locked to the physical calibration frequency shown in the video.

Here are the details of your environment:
1. **Calibration Video:** `/app/calibration.mp4`. This is a 10-second, 30 fps video showing a calibration strobe light (alternating pure black and pure white frames). You must analyze this video to determine the strobe's frequency in Hertz (blinks per second). Let's call this frequency `F`. 
2. **Secondary Telemetry Database:** `/app/telemetry.db`. A SQLite database containing a table `sensor_data` with columns `timestamp` (float), `sample_id` (string), and `signal_2` (float).

Your objective is to write a classification script located at `/home/user/evaluate_sample.py` that evaluates a single primary sensor CSV file and determines if it is a "clean" sample or a "corrupted" sample.

**Requirements for `/home/user/evaluate_sample.py`:**
* The script must accept exactly one command-line argument: the absolute path to a primary sensor CSV file (e.g., `/some/path/sample_123.csv`).
* The CSV file contains a header and two columns: `timestamp` and `signal_1`. The `sample_id` is the base filename without the `.csv` extension (e.g., `sample_123`).
* The script must join the data from the CSV file with the corresponding `sample_id` records in `/app/telemetry.db`, matching exactly on `timestamp`.
* Once joined, the script must perform a linear regression modeling `signal_2` as a function of `signal_1` (i.e., `signal_2 = slope * signal_1 + intercept`).
* **Classification Rule:** In a valid (clean) sequence, the regression `slope` will be approximately equal to the calibration frequency `F` from the video. If the calculated slope is within `±0.1` of `F`, the script must terminate with exit code `0` (clean). Otherwise, it must terminate with exit code `1` (corrupted/evil).

You can use any language (Python is recommended) and install any packages you need. Do not hardcode the frequency `F`—if we swap the calibration video, your script shouldn't need to change, but for this task, you only need to ensure your script correctly classifies files based on the *current* video's frequency.

Please write and test your script. An automated test suite will later invoke your script on a hidden evaluation corpus of clean and corrupted CSV files to verify its accuracy.