You are a performance engineer profiling a new spectroscopy analysis pipeline. We've received multiple community-submitted C implementations for integrating spectral signals, but we suspect several of them suffer from numerical instability due to naive floating-point reduction orders (e.g., basic `float` summation failing on large arrays).

Your task is to build an automated detector that filters out numerically unstable implementations.

1. **Signal Extraction:**
   There is a video file at `/app/spectroscopy.mp4` containing raw high-speed spectroscopy captures.
   Extract the mean grayscale intensity of each frame to form a 1D array of floating-point values (the signal).

2. **Test Harness:**
   Write a test harness in C that takes the extracted signal, repeats it `100,000` times to form a massive array, and passes it to an external integration function. 
   The integration functions to test will have the signature:
   `float integrate(float* data, int n);`

3. **Detector Script:**
   Create an executable bash script at `/home/user/detect.sh` that takes exactly one argument: the path to a C source file containing an `integrate` function.
   - Your script must compile the provided C file along with your test harness.
   - Run the compiled binary.
   - Compare the result of the `integrate` function against a mathematically robust baseline (which you must compute/implement in your harness).
   - The script must **exit with code 0** (accept) if the implementation is numerically stable (the result is within `0.1%` of the true sum).
   - The script must **exit with code 1** (reject) if the implementation is numerically unstable (suffers from catastrophic cancellation or reduction truncation).

You have been provided a testing corpus:
- `/app/corpus/clean/*.c` contains numerically stable implementations (e.g., Kahan summation, hierarchical reduction).
- `/app/corpus/evil/*.c` contains naive `float` implementations that will lose precision on large arrays.

Your `/home/user/detect.sh` script must successfully accept all files in the `clean` directory and reject all files in the `evil` directory.