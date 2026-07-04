You are tasked with fixing and completing a polyglot data-processing pipeline that validates, rate-limits, and processes a stream of numerical inputs. 

Currently, the project in `/home/user/pipeline/` is in an incomplete state. A previous engineer left behind a broken test suite and an audio specification, but didn't finish the core logic.

Here is what you need to do:

1. **Extract Parameters from Audio Specification**:
   Listen to (or transcribe) the audio file located at `/app/spec_memo.wav`. You can use the transcription tool provided at `/usr/local/bin/whisper-cli` (or any ffmpeg-based approach you prefer). The audio dictates three quadratic coefficients (A, B, and C) and a specific rate-limit capacity (requests per second).

2. **Fix the Test Orchestration and Import Ordering**:
   The test suite in `/home/user/pipeline/tests/test_processor.py` is failing. It was designed to mock the system clock to test the rate-limiting logic. However, due to an import ordering issue, the module caches the real `time.time` before the mock is applied, causing the tests to behave non-deterministically or fail entirely. Fix the import order or the mocking strategy so that the test suite passes consistently.

3. **Implement the Processing Tool**:
   Write the main entry point at `/home/user/pipeline/process.py`. 
   - It must read line-by-line from standard input (`stdin`).
   - Each line will contain two space-separated integers: `timestamp_ms` (strictly monotonically increasing) and `x` (the input value).
   - **Rate Limiting**: Apply a rolling-window rate limit. The maximum allowed requests per 1000-millisecond window is dictated by the audio file. If a request arrives and the quota is exhausted for the preceding 1000ms (strictly `> timestamp_ms - 1000`), the tool must output `REJECTED` and not process the value.
   - **Numerical Algorithm**: If the request is accepted, compute the quadratic value $Ax^2 + Bx + C$ using the coefficients (A, B, C) dictated in the audio file. Output this computed integer.
   - Output exactly one line per input line.

4. **Integration**:
   Ensure that `/home/user/pipeline/process.py` is executable (`chmod +x`). 
   Your script must run standalone and will be rigorously tested against an automated fuzzer with thousands of inputs to ensure precise numerical and rate-limiting equivalence with the reference implementation.