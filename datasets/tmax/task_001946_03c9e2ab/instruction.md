You are an ML engineer preparing training data for a new Radio Frequency (RF) deep learning model. We have a historical dataset of RF signals stored in HDF5 format, but we've discovered that a legacy preprocessing tool has corrupted some of the files by injecting a subtle frequency-domain anomaly. 

Your objective is to write a Python-based classifier that acts as a gatekeeper to sanitize our training data pipeline.

We have provided a small sample of known clean files in `/home/user/data/clean/` and known corrupted ("evil") files in `/home/user/data/evil/`. 
Additionally, the legacy preprocessing tool that caused this issue is available as a stripped binary at `/app/legacy_preprocessor`. You can use it as a black-box oracle to study how it corrupts clean signals if you need to generate more test cases.

Task details:
1. All data files are in HDF5 format (`.h5`). Each contains a single 1D floating-point dataset named `rf_signal`.
2. The signals are 2000 samples long, representing exactly 1 second of data (Sample Rate = 2000 Hz).
3. You must write a Python script at `/home/user/detector.py`.
4. Your script must take a single command-line argument (the path to an HDF5 file).
5. The script must analyze the signal using Fourier transforms / spectral analysis to detect the anomaly.
6. The script must exit with status code `0` if the file is clean, and exit with status code `1` if the file is corrupted (evil).

An automated verification suite will run your script against a hidden holdout dataset of clean and evil files. Your solution must correctly classify 100% of the hidden clean and evil corpora to pass.