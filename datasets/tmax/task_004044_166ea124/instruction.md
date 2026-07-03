You are the release manager for a distributed calculation service. You are preparing the v3 deployment pipeline, which involves extracting verification codes from legacy E2E test runs, configuring conditional builds for a multi-language (Python + C++) engine, and implementing a rigorous security filter to prevent injection attacks and Denial of Service (DoS) payloads.

Your task consists of three main phases:

### Phase 1: E2E Test Orchestration & Video Extraction
The previous automated UI test pipeline recorded its execution to an MP4 video file located at `/app/e2e_test_run.mp4`. Embedded within this video is a flashing terminal sequence. For exactly 15 frames during the video, a successful build prints a deployment authorization token in the format `AUTH_TOKEN: XXXX-XXXX-XXXX-XXXX`. 
1. You must extract frames from `/app/e2e_test_run.mp4` (ffmpeg is available).
2. Analyze the frames to locate the authorization token (you may use `tesseract-ocr` or similar tools).
3. Write the exact token string (e.g., `AUTH_TOKEN: 1A2B-3C4D-5E6F-7G8H`) to `/home/user/auth_token.txt`.

### Phase 2: Conditional Build System
The core mathematical expression evaluator is written in C++. The source code will be located at `/home/user/calc_engine.cpp` (assume you write a dummy version of this file just to satisfy the build system, as the real source is pulled during deployment, but your build script must be ready).
You need to write a build script at `/home/user/build.sh` that compiles `/home/user/calc_engine.cpp` into two distinct shared libraries:
1. `/home/user/libcalc_debug.so`: Compiled with debugging symbols (`-g`), optimizations disabled (`-O0`), and the preprocessor macro `DEBUG_TRACE=1`.
2. `/home/user/libcalc_release.so`: Compiled with high optimization (`-O3`), stripped of symbols, and the preprocessor macro `PRODUCTION_MODE=1`.

The script must be executable and handle the compilation using `g++`. Create a minimal dummy `/home/user/calc_engine.cpp` with a simple exported function `extern "C" double evaluate() { return 0.0; }` so your build script successfully runs and generates the `.so` files.

### Phase 3: Adversarial Corpus & Expression Parsing
The Python API gateway passes mathematical expressions to the C++ engine. Historically, attackers have crashed the engine using excessively nested function calls or malformed operators. You must implement a pre-evaluation sanitizer in Python.

Create a module at `/home/user/sanitizer.py` with the following entry point:
```python
def is_safe_expression(expr: str) -> bool:
    # Return True if the expression is safe to evaluate
    # Return False if the expression is malicious or malformed
    pass
```

We have mounted a verification corpus in the environment:
- `/app/corpus/clean/`: Contains text files, each with one valid, safe mathematical expression.
- `/app/corpus/evil/`: Contains text files, each with one malicious payload designed to cause DoS or execute arbitrary code.

Your `is_safe_expression` function will be tested against both corpora. To pass this phase, your function must achieve **100% acceptance** of the `clean` corpus (returning `True`) AND **100% rejection** of the `evil` corpus (returning `False`).
The criteria for an "evil" expression are:
- Contains more than 5 levels of nested parentheses (e.g., `((((((1))))))`).
- Contains the word "eval", "exec", "import", or "system" (case-insensitive).
- Attempts to use an exponentiation operation with a base or exponent larger than 4 digits (e.g., `99999^2` is blocked, `100^100` is safe).
- Exceeds 255 characters in total length.

Ensure all components are in their designated locations and your Python filter is perfectly tuned against the adversarial corpus.