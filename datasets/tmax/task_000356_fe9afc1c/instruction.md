I am a performance engineer working on an acoustic monitoring system for a server farm. We are trying to detect a specific hardware failure mode (a failing cooling fan bearing) that emits a high-frequency acoustic anomaly. We need a highly optimized classification pipeline to run on edge devices.

We have captured a pure sample of this anomaly, located at `/app/reference_signal.wav`. 

I need you to perform the following steps:
1. **Experimental Data Visualization & Signal Processing**: Analyze `/app/reference_signal.wav` to identify the peak frequency characteristic of the failure. Generate a Power Spectral Density (PSD) plot and save it to `/home/user/psd.png`.
2. **Observational Data Reshaping**: We have a training set of acoustic logs. Normal operational sounds are in `/app/corpus/clean/` and sounds containing the fan failure are in `/app/corpus/evil/`. You will need to extract the spectral features of these files.
3. **Optimization**: Write a script to analytically find the optimal threshold for the power magnitude at the target frequency that perfectly separates the clean training data from the evil training data.
4. **Implementation**: Create a fast executable at `/home/user/classifier`. It can be a Python script (with `#!/usr/bin/env python3` and `chmod +x`) or a compiled C++ binary.
    * It must accept a single argument: the path to a WAV file. Example: `/home/user/classifier /path/to/audio.wav`
    * If the file is classified as "clean" (normal), it must exit with status code `0`.
    * If the file is classified as "evil" (contains the anomaly), it must exit with status code `1`.

Your solution will be evaluated against a hidden, held-out adversarial corpus of clean and evil audio files to verify that it correctly classifies 100% of the files without overfitting to the training set. Speed and accuracy are critical.