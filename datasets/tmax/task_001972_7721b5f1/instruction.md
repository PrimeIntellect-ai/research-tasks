You are a build engineer managing an artifact ingestion pipeline. The system uses a high-performance C++ parser to validate build artifacts, which is called via Python. However, the current system is broken, suffers from memory safety issues, and is failing to detect malicious artifacts.

Your goal is to repair the pipeline, compile the library, and build a Python classifier.

**Phase 1: Audio Signal Analysis**
The original developer left a diagnostic audio note in `/app/signal.wav`. The audio contains exactly three distinct continuous tones played sequentially. 
Write a Python numerical algorithm (e.g., using `scipy` or `numpy` FFT) to process `/app/signal.wav` and determine the three peak frequencies (in integer Hz).

**Phase 2: C++ Memory Safety & Patching**
In `/app/src/artifact_parser.cpp`, there is a function that parses artifact metadata. It currently suffers from undefined behavior and buffer overflows. 
1. Use the three frequencies discovered in Phase 1 as the correct parameters to patch the C++ code. The highest frequency represents the exact `MAX_BUFFER_SIZE` needed to safely parse the artifacts. The other two frequencies are the `MAGIC_HEADER_1` and `MAGIC_HEADER_2` validation values required by the parser.
2. Fix any explicit memory leaks or undefined behavior in `artifact_parser.cpp`.
3. Create a Makefile and compile `artifact_parser.cpp` into a shared library named `/app/build/libartifact.so`.

**Phase 3: Python Classifier & Adversarial Corpus**
Write a Python script `/home/user/classifier.py` that accepts a single file path as a command-line argument:
`python3 /home/user/classifier.py <filepath>`

The script must:
1. Load `/app/build/libartifact.so` using `ctypes`.
2. Pass the file content to the C++ parser.
3. Print exactly `CLEAN` to standard output if the artifact is safe.
4. Print exactly `EVIL` to standard output if the artifact triggers the buffer size limits, contains invalid magic headers, or contains the string `EXEC_PAYLOAD`.

**Phase 4: Benchmarking**
Create a dummy text file of exactly 10MB. Write a benchmark script to measure the throughput of `classifier.py` when processing this file. Output the result in MB/s to `/home/user/benchmark.log` in the format: `Throughput: <value> MB/s`.

Ensure your classifier perfectly accepts valid artifacts and rejects malicious ones.