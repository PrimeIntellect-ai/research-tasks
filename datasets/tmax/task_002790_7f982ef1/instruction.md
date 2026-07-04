You are a security researcher analyzing a suspicious binary's telemetry exfiltration system. We have recovered the source code for the malware's internal payload classifier, but it is currently broken and we need to use it to filter our own network logs.

The codebase is located at `/home/user/telemetry_classifier/`. It contains a `build.sh` script and several C++ source files in the `src/` directory, including one with spaces in its filename. 

You need to accomplish the following:

1. **Fix the Build System:** The `build.sh` script currently fails to compile the C++ project. Diagnose and fix the shell script so that it correctly handles all files in the `src/` directory. The compiled output must be written to `/home/user/telemetry_classifier/bin/classifier`.
2. **Extract the Seed:** We recovered an image from the malware author's server at `/app/malware_seed.png`. It contains a handwritten threshold value (e.g., "THRESHOLD=XX.XX"). You must extract this numerical value and update the `THRESHOLD` macro in `/home/user/telemetry_classifier/src/classifier.cpp` with it.
3. **Fix Intermittent Failures:** Even when compiled, the classifier suffers from intermittent failures, producing different classification scores for the exact same input file across multiple runs. Diagnose and fix this memory/state issue in the C++ code.
4. **Classify the Corpora:** Once fixed, the classifier must accurately distinguish between benign and malicious payloads. We have provided two directories of payloads:
   - `/app/corpora/evil/`: Contains malicious payloads.
   - `/app/corpora/clean/`: Contains benign payloads.

The final compiled binary at `/home/user/telemetry_classifier/bin/classifier` must accept a single file path as a command-line argument. It must print exactly `EVIL` to standard output if the file is malicious, and `CLEAN` if the file is benign. You must achieve a 100% success rate on both corpora.