You have recently inherited a broken data processing pipeline for your team. The pipeline is located in `/home/user/pipeline/` and consists of two parts: a Python script `pipeline.py` and a compiled Linux binary named `processor`. Unfortunately, the original author left the company and the C source code for `processor` has been permanently lost.

The expected workflow is:
1. `python3 /home/user/pipeline/pipeline.py` reads a text string from `/home/user/pipeline/input.txt` and serializes it into a custom binary format at `/home/user/pipeline/data.bin`.
2. `/home/user/pipeline/processor /home/user/pipeline/data.bin /home/user/pipeline/output.txt` reads the binary file, processes the text, and writes the result to `output.txt`.

Currently, `pipeline.py` is broken. It uses the wrong magic numbers, incorrect struct field sizes, and the wrong text encoding. As a result, the `processor` binary either rejects the file, crashes, or produces garbage output.

Your task is to:
1. Reverse engineer or trace the `processor` binary to figure out the exact binary struct layout it expects (including the correct magic number, the size of the length field, and the string encoding).
2. Modify `/home/user/pipeline/pipeline.py` to correctly serialize the data according to the binary's expectations.
3. Successfully run both the Python script and the binary processor to generate the correct `/home/user/pipeline/output.txt`.

The initial `input.txt` contains a secret phrase. Do not change `input.txt`. 
You have successfully completed the task when running the processor finishes with a `0` exit code and produces a valid, human-readable `/home/user/pipeline/output.txt` containing the processed phrase.