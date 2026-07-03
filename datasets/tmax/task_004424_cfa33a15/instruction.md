You are an integration developer testing a new "Optical API" that transmits mathematical constraint data via flashing light sequences in video streams. 

Your task consists of three parts:

**Part 1: Fix and Analyze the Legacy C Implementation**
In `/home/user/legacy_source/`, there is a broken C implementation of the API parser. 
1. The `Makefile` is slightly broken and the C code contains a memory leak and a logic bug in how it processes input. 
2. Fix the Makefile so `make` correctly builds the executable `api_parser_c`.
3. Fix the memory leak and bugs in `parser.c`. You may use `valgrind` or `gdb` to debug. Analyzing this source code will reveal the mathematical protocol used by the API (it reads a binary string from `argv[1]`, converts it to a sequence of 8-bit integers, computes a running polynomial hash, and solves a modular inverse constraint, printing the result to stdout).

**Part 2: Create a Bit-Exact Python Equivalent**
The C implementation is being deprecated. You must write a Python script at `/home/user/api_parser.py` that perfectly replicates the intended mathematical logic of the fixed C program. 
- It must accept a single command-line argument containing a binary string (e.g., `python3 /home/user/api_parser.py 1010101000001111`).
- It must print exactly the same integer output to `stdout` as the correctly functioning C program would. 
- An automated fuzzing verifier will randomly generate hundreds of binary strings of varying lengths to ensure your Python script is bit-exact equivalent to a secret reference oracle.

**Part 3: Video Integration Test**
We have captured an integration test video of the optical API at `/app/api_test_capture.mp4`.
1. The video runs at exactly 10 frames per second.
2. The top-left 10x10 pixel region of the video encodes a binary stream over time (1 bit per frame). 
3. A purely black region (average brightness < 128) represents a `0`. A purely white region (average brightness >= 128) represents a `1`.
4. Extract the full binary string encoded in the video's frames.
5. Run your Python script (`/home/user/api_parser.py`) passing this exact extracted binary string as the argument.
6. Save the stdout result of this execution to `/home/user/integration_result.txt`.

Ensure your Python code is robust and handles binary strings of lengths that are not perfect multiples of 8 (pad with trailing zeros up to the next byte boundary, as defined in the C source).