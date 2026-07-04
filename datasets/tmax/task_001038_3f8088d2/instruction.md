You are taking over a partially finished C project located at `/home/user/dsp_server`. It is a WebSocket-based Digital Signal Processing (DSP) bytecode emulator. 

Currently, the project is broken in several ways, and you must fix it, organize it, and implement a critical security filter.

**1. Project Organization & Build Fixes**
The project directory is disorganized. You must:
* Move all `.c` files into a `src/` subdirectory.
* Move all `.h` files into an `include/` subdirectory.
* Update `CMakeLists.txt` to reflect these paths.
* The project fails to build because `CMakeLists.txt` cannot link a missing shared library (`libmongoose.so` for WebSocket communication). The precompiled library and its header are actually located at `/app/deps/libmongoose.so` and `/app/deps/mongoose.h`. Fix the CMake configuration to successfully find and link this library, ensuring the target executable `dsp_server` compiles cleanly when you run `cmake . && make`.

**2. Bytecode Validator Implementation**
The emulator receives DSP bytecodes over WebSockets, but it currently executes anything it receives, which is a security risk. You need to implement a filter.
The previous lead developer left a voice note detailing the strict validation rules. You will find this audio file at `/app/voicenote.wav`. You must extract the spoken rules from this audio file (you may install tools like `ffmpeg` or Python speech recognition packages to process it).

Once you know the rules, implement the function:
`int validate_bytecode(const uint8_t* code, size_t len);`
inside `src/validator.c` (you should create this file if it doesn't exist, and put its declaration in `include/validator.h`).
* Return `1` if the bytecode sequence is clean and valid.
* Return `0` if the bytecode violates ANY of the rules mentioned in the voice note.

**Verification**
An automated adversarial verifier will directly test your `src/validator.c`. It will compile your validator against two corpora:
* A "clean" corpus of valid bytecodes.
* An "evil" corpus of malicious bytecodes.

To succeed, you must commit your final code, ensure `dsp_server` builds via CMake, and your `validate_bytecode` implementation must perfectly filter the adversarial corpus based on the audio instructions.