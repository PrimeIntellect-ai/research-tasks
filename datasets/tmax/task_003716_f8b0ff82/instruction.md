You are a release manager preparing the deployment of a new internal data processing pipeline. Part of this pipeline involves a Python package `fast_dsp` that wraps a highly optimized C extension for processing arrays of acoustic data.

Unfortunately, the repository you've inherited has several severe issues:
1. The `setup.py` and `Makefile` in `/home/user/release_prep/fast_dsp/` are broken and will not compile.
2. The C extension (`src/processor.c`) contains a memory safety vulnerability (an out-of-bounds array access) and uses an extremely slow sorting implementation that fails performance tests.
3. The integration test suite requires ingesting an actual audio transmission, recovering the data, processing it, and validating the output.

Your tasks are:
1. **Fix the Build**: Repair `setup.py` and the `Makefile` so that the `fast_dsp` Python module compiles and installs successfully (`pip install -e .`).
2. **Fix the C Extension**: Debug and repair `src/processor.c`. Fix the memory safety bug (segfault on arrays larger than 10 elements) and replace the quadratic sorting algorithm with an efficient $O(N \log N)$ algorithm (e.g., standard quicksort).
3. **Data Recovery**: There is an audio file located at `/app/transmission.wav`. This file contains a spoken sequence of numbers (integers). You must use an appropriate tool or Python library (e.g., `whisper` or `SpeechRecognition`) to transcribe the spoken numbers into an array of integers.
4. **Integration**: Write a Python script `/home/user/run_pipeline.py` that:
    - Loads the transcribed integers.
    - Uses the newly compiled `fast_dsp.sort_and_merge` function to process the array.
    - Simulates a WebSocket client that connects to `ws://localhost:8080` (you do not need to build the server, just write the client connection logic to demonstrate it would send) and writes the final processed JSON list of integers to `/home/user/final_output.json`.

Format of `/home/user/final_output.json`:
```json
[2, 5, 8, 12, 45, 99]
```

Ensure your pipeline works efficiently and accurately. Automated grading will compare your `final_output.json` to the true mathematical sequence embedded in the audio file.