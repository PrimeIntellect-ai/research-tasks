You are an integration developer building a mock client for a legacy data processing API. The original documentation is lost, but a scan of the transformation specification has been recovered and is available at `/app/legacy_api_formula.png`. 

Your task is to write a C program that implements this specification to accurately replicate the API's payload transformation, and to configure its build process.

Step 1: Specification Recovery
Use optical character recognition (OCR) tools (e.g., `tesseract`, which is pre-installed) to extract the text from `/app/legacy_api_formula.png`. This image contains the specific numerical algorithm used to transform each byte of the incoming payload.

Step 2: Implementation & Compilation
Write a C program in `/app/payload_transform.c` that reads arbitrary binary data from `stdin` until EOF, applies the numerical algorithm extracted from the image to each byte sequentially, and prints the result to `stdout` as a continuous string of lowercase 2-character hexadecimal values (no spaces or newlines).

Step 3: Build System
Create a `Makefile` in `/app/` that satisfies the following:
1. The default target `all` compiles `/app/payload_transform.c` into an executable named `/app/payload_transform`.
2. A target `benchmark` compiles the same file into `/app/payload_benchmark` but passes a `-DBENCHMARK_MODE` macro. If this macro is defined, the C program should bypass `stdin`, generate a dummy array of 10,000,000 random bytes, apply the transformation, and print ONLY the time taken in milliseconds (as an integer) before exiting.
3. Both builds must use `-O3` optimization.

Note: An automated fuzzing verifier will test your standard binary (`/app/payload_transform`) against an oracle with thousands of random byte inputs. Ensure your implementation is bit-exact with the mathematical formula provided in the scanned image.