You are an ML engineer preparing acoustic spectroscopy data for a new deep learning model. We have a pipeline that processes raw acoustic returns, but it has been suffering from non-reproducible results due to floating-point reduction order variations across different worker nodes. 

Your objective is to build a rock-solid, reproducible Python processor that identically matches our reference stable implementation.

Step 1: Extract Calibration Parameters
We have an audio recording from the field engineers containing the calibration metadata for this batch of data. Listen to or transcribe the file located at `/app/calibration_signal.wav`. It contains a spoken sentence specifying the `calibration_frequency` (in Hz). 

Step 2: Implement the Reproducible Processor
Create a Python script at `/home/user/process_signal.py`. The script will be invoked with a single command-line argument: the path to a text file containing raw signal measurements (one floating-point number per line).

For each measurement $x_i$ at line index $i$ (starting at $i=0$), your script must:
1. Apply the calibration modulation: $y_i = x_i \times \cos(2 \pi \cdot f_c \cdot i / 16000)$, where $f_c$ is the calibration frequency you extracted from the audio, and $16000$ is the assumed sample rate.
2. Sum all modulated values $y_i$ into a single aggregate value. 

CRITICAL REQUIREMENT: Standard sequential addition (`+` in a loop or `sum()`) is mathematically correct but suffers from floating-point accumulation errors that vary by platform/reduction order. To be perfectly reproducible and match our oracle, you MUST accumulate the exact sum without precision loss using Python's `math.fsum()` on the sequence of modulated values.

Step 3: Output
The script must print ONLY the final sum to standard output, formatted to exactly 10 decimal places (e.g., `123.4567890123`).

Your script will be aggressively fuzzed against our internal oracle binary with thousands of random inputs to ensure absolute bit-exact equivalence.