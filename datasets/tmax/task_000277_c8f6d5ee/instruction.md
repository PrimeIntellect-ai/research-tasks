You are a release manager preparing an automated deployment pipeline. A critical part of our compliance process involves scanning audio artifacts for unauthorized operational commands before they are archived.

We have a proprietary audio format called `.cwav`. These are standard WAV files prefixed with a custom 50-byte metadata header. You have been provided the C source code for a library that can strip this header, located at `/app/src/libcwav.c`.

Your objective is to build an end-to-end Python pipeline that detects unauthorized commands in these audio files. Specifically, any audio containing the spoken word "launch" must be rejected. 

Please perform the following steps:
1. **Build the C Library**: Compile `/app/src/libcwav.c` into a shared library `/app/lib/libcwav.so`. Create a bash script `/app/build.sh` that performs this compilation and installs any necessary Python dependencies for your pipeline. 
2. **Create Python FFI Bindings**: Write a Python module that uses `ctypes` to interface with `libcwav.so`. The C function signature is `int extract_wav(const char* in_path, const char* out_path);` (returns 0 on success).
3. **Write the Detector**: Create `/app/audio_detector.py`. This script should take a directory of `.cwav` files as a command-line argument, e.g., `python /app/audio_detector.py /app/corpora/mixed`. 
    - For each `.cwav` file, it must unpack it to a temporary `.wav` file using your FFI bindings.
    - It must then transcribe the audio content to text. You should use a lightweight, offline transcription library (e.g., `SpeechRecognition` with the `pocketsphinx` engine, which you should install in your `build.sh`).
    - If the transcript contains the word "launch" (case-insensitive), the file is classified as "REJECT". Otherwise, it is "ACCEPT".
    - The script must output a JSON file named `results.json` in the current working directory. The JSON should be a dictionary mapping the base filename (e.g., `file1.cwav`) to its classification ("REJECT" or "ACCEPT").

We have provided a sample `.cwav` file at `/app/sample.cwav` for you to test your pipeline. We also have two directories of corpora located at `/app/corpora/clean/` and `/app/corpora/evil/` which you can use to validate your detector.

Ensure your code is robust and your `build.sh` script is executable and fully prepares the environment.