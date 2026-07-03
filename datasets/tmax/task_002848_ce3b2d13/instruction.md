You are a machine learning engineer preparing a robust training dataset for an audio classification model. We recently lost the source code for our legacy data augmentation and feature extraction pipeline, but we still have the compiled binary oracle we use for regression testing.

Your task is to perfectly reconstruct the missing Python module, `spectral_augment.py`, so that its output is bit-exact equivalent to the legacy system. 

First, you need to recover the missing configuration parameters. A previous engineer left an audio memo containing the specific calibration epsilon and the random seed used for the perturbation distribution.
1. Analyze the audio file located at `/app/system_recording.wav`. You may need to install audio processing or transcription packages (e.g., `pocketsphinx`, `SpeechRecognition`, or `whisper`) to extract the spoken parameters.

Second, write the replacement script at `/home/user/spectral_augment.py`. 
The script must act as a UNIX filter with the following exact specifications:
- It reads exactly 1024 `float32` values (little-endian) from `stdin`.
- It computes the Real Fast Fourier Transform (rFFT) to extract the frequency domain representation.
- It computes the Power Spectrum ($P = |X|^2$) for the 513 frequency bins.
- It performs a Monte Carlo perturbation: generate exactly 513 random samples from a Uniform(0, 1) distribution and add them to the Power Spectrum. You MUST seed your random number generator (using `numpy.random.seed()`) with the exact integer seed mentioned in the audio log *before* generating the noise array for each invocation.
- It ensures numerical stability by applying a floor to all values using a `max(val, epsilon)` operation, where `epsilon` is the calibration value mentioned in the audio log.
- It writes the resulting 513 `float32` values (little-endian) to `stdout` and exits cleanly.

Ensure your script is executable (`chmod +x`) and begins with `#!/usr/bin/env python3`. The automated testing suite will run regression tests by fuzzing your script against the compiled oracle using thousands of random `float32` input arrays. Your script must be numerically stable and produce bit-exact matches to pass.