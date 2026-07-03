You are a release manager preparing a critical deployment toolset. We have lost the source code for our legacy data obfuscator, and we need to deploy it to a new architecture. We only have two artifacts left:
1. A compiled reference binary (`/app/oracle_bin`).
2. An audio recording (`/app/spec.wav`) left by the original engineer detailing the exact transformation parameters.

Your task:
1. Extract the transformation rules from the audio file `/app/spec.wav`.
2. Re-implement the obfuscation logic in C. Create a shared library `/home/user/libobfuscate.so` with a function `void obfuscate(const unsigned char* in, unsigned char* out, int len)`.
3. To ensure your re-implementation is robust, create a Python test suite at `/home/user/test.py` using `ctypes` to interface with your shared library and `hypothesis` for property-based testing. Generate random byte arrays and assert that your library processes them correctly according to the rules you extracted. 
4. Finally, create a CLI executable `/home/user/deploy_tool` (compiled from your C code) that reads binary data from `stdin`, processes it using the obfuscate function, and writes the output to `stdout`.

The automated verification system will run hundreds of random binary payloads through both your `/home/user/deploy_tool` and the reference `/app/oracle_bin` to guarantee bit-exact behavioral equivalence. 

Make sure your C tool compiles flawlessly and is placed exactly at `/home/user/deploy_tool`.