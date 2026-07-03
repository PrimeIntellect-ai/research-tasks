You are a data engineer working on an ETL pipeline for a legacy telemetry system. We have received an audio file containing an acoustic modem transmission, but the original decoding software was lost.

Your task is to build a C++ data processing tool to decode the telemetry data from the audio file.

Here are the details of the pipeline you need to implement:
1. **Analysis Environment Setup**: The system is a bare-bones Linux environment. You will need to install any necessary C++ development tools and numerical/audio libraries (e.g., `fftw3`, `libsndfile`) to process the audio.
2. **Audio Properties**: The file is located at `/app/data/signal.wav`. It is a 16kHz mono WAV file containing a noisy Frequency-Shift Keying (FSK) transmission. 
3. **Transmission Protocol**:
   - The signal consists of a sequence of bits.
   - Each bit is exactly 0.1 seconds long.
   - A bit value of `0` is represented by a 1000 Hz sine wave tone.
   - A bit value of `1` is represented by a 2000 Hz sine wave tone.
   - The signal is heavily degraded by white noise.
4. **Implementation**: Write a C++ program (e.g., `decoder.cpp`) that reads the WAV file, processes the audio in 0.1-second windows (e.g., using Fast Fourier Transform), and determines the bit value for each window based on the dominant frequency energy (1000 Hz vs 2000 Hz).
5. **Output**: Your C++ program must output the decoded binary sequence to `/home/user/decoded.txt`. The file should contain exactly one character (`0` or `1`) per line, corresponding to the sequence of bits in the audio file.

Your final accuracy will be evaluated programmatically. You must achieve an accuracy of >= 95% against the hidden ground truth.