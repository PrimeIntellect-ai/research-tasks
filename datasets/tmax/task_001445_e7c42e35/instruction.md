You are a platform engineer responsible for maintaining the CI/CD pipeline of `libjit-video`, a hybrid C and Python project that dynamically generates and executes bytecode for video processing. The pipeline is currently failing at multiple stages, and you need to investigate and fix the issues.

**Stage 1: Shared Library Linking Error**
The C component of the project is located in `/home/user/libjit`. It consists of `jit_compiler.c` and a `Makefile`. Currently, running `make` fails to properly build the shared object `libjit.so` due to ABI and linker errors. 
- Modify the `Makefile` so that it successfully compiles and links the C code into a dynamically loadable shared library named `libjit.so` in the same directory.
- Ensure the compiled code is position-independent, as required for shared libraries in Linux.

**Stage 2: CI Video Artefact Analysis**
During a recent pipeline failure, the UI test runner captured a video artefact located at `/app/ci_run.mp4`. Our test framework signals pipeline status by flashing a status color in the absolute top-left pixel (x=0, y=0) of the video frame.
- Extract the frames from `/app/ci_run.mp4` (you may use `ffmpeg`, which is preinstalled).
- Write a Python script to analyze the frames and identify the exact frame indices (0-indexed) where the top-left pixel is strictly pure red (RGB: 255, 0, 0).
- Save these 0-indexed frame numbers to `/home/user/red_frames.txt`, with one integer per line, sorted in ascending order.

**Stage 3: Adversarial Payload Sanitizer**
The API accepts serialized x86-64 machine code from clients to optimize video transforms. Recently, malicious actors have been submitting shellcode to break out of the JIT sandbox.
- Write a Python script at `/home/user/sanitizer.py` that acts as a pre-execution sanitizer.
- The script must accept a single command-line argument: the path to a JSON file.
- The JSON file contains a single object with a `payload` key mapping to a hex-encoded string of x86-64 machine code. (e.g., `{"payload": "9090c3"}`).
- The script must deserialize the file, decode the hex payload, and perform an assembly-level analysis.
- **Rules:** If the bytecode contains any of the following restricted system call instructions at any byte offset, it must be rejected:
  - `0F 05` (`syscall`)
  - `0F 34` (`sysenter`)
  - `CD 80` (`int 0x80`)
- **Output:** 
  - If the payload contains any restricted byte sequence, print exactly `EVIL` to standard output and exit with status code `1`.
  - If the payload is safe, print exactly `CLEAN` to standard output and exit with status code `0`.

Your sanitizer will be tested against a hidden evaluation corpus to ensure it correctly identifies all malicious payloads while allowing all safe optimization payloads to pass.