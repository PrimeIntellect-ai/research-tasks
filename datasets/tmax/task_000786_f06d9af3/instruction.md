I am a web developer building a feature for a music streaming service that analyzes audio characteristics in real-time. I have a baseline implementation in Python, but it's too slow. I need you to create a high-performance C++ shared library (`libaudio_analyzer.so`) that provides a stable C-ABI for integration with our backend.

Here is what you need to do:
1. Under `/home/user/project`, create a custom C++ data structure to efficiently hold and process 16-bit PCM audio data.
2. Implement an audio analysis function that computes the Short-Time Fourier Transform (STFT) energy across the entire audio file provided at `/app/sample_audio.wav`.
3. Provide a C-ABI exposed function `double analyze_audio_energy(const char* filepath)` inside `libaudio_analyzer.so`.
4. Create a CMake build system (`/home/user/project/CMakeLists.txt`) that compiles your code into the shared library `libaudio_analyzer.so` and links any necessary math libraries.
5. Create a Python wrapper script `/home/user/project/run_analysis.py` using `ctypes` to load the library, call the function on `/app/sample_audio.wav`, and print the execution time and the result.
6. Your C++ implementation must process the audio file significantly faster than a naive pure-Python implementation, achieving an execution time of under 50 milliseconds.

The final output will be tested by running `python3 /home/user/project/run_analysis.py`. Ensure the output logs exactly the result and the time taken in milliseconds on separate lines.