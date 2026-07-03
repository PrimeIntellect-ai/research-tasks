You are a data analyst working for an autonomous vehicle research team. We have encountered an issue where some of our telemetry logs (CSV files) have been subtly manipulated by a third-party testing vendor to hide anomalous driving events, while others are genuine. 

We have a verified baseline video recording of a vehicle's dashboard during a test run located at `/app/baseline_dash.mp4`. The video displays a simple moving bar graph representing speed and RPM at 1-second intervals (the video is 30 seconds long, 1 fps). 

You need to build a robust, reproducible pipeline that accomplishes two things:
1. **Video Extraction**: Extract the frames from `/app/baseline_dash.mp4` and determine the baseline correlation matrix between Speed and RPM. (Assume the height of the left bar in pixels is Speed, and the right bar is RPM).
2. **Adversarial Detection**: We have a directory of telemetry logs. You must write a Python script `/home/user/detector.py` that acts as a classifier. It should load a given CSV log, handle any missing values (using median imputation), compute the covariance/correlation matrix, use a simple probabilistic or Bayesian check against the baseline correlation derived from the video, and determine if the log is "clean" (authentic) or "evil" (manipulated).

Your script must implement the following CLI signature:
`python3 /home/user/detector.py --input <path_to_csv>`

It must print exactly one line to standard output: either `CLEAN` or `EVIL`.

To help you develop this, we have provided two small corpora:
- `/home/user/data/training/clean/`: Contains examples of genuine telemetry CSVs.
- `/home/user/data/training/evil/`: Contains examples of manipulated CSVs (outliers injected, covariance structure broken).

Your final script will be tested against a hidden holdout set of both clean and evil CSVs. Ensure your pipeline is fully reproducible and your outlier handling is robust.