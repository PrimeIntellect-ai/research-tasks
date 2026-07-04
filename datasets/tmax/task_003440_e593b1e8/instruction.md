You are a mobile build engineer responsible for maintaining our CI/CD pipeline infrastructure. Recently, we introduced an audio-driven build validation step and a native C library for expression evaluation to speed up build script parsing. However, the system is currently broken.

Your objectives:

1. **Fix the C Library Linking Error:**
   In `/home/user/mathlib`, there is a small C project with a Makefile. It is supposed to compile to a shared library `libmathparser.so` that evaluates mathematical expressions. Currently, running `make` fails due to a linking error. Identify the problem, fix the Makefile, and successfully compile `libmathparser.so`.

2. **Transcribe the Audio Directive:**
   The build pipeline's threshold parameter is dynamically set via a voice note. There is an audio file at `/app/directive.wav`. Transcribe this audio file (you may install and use any Python library like `openai-whisper` or `SpeechRecognition`) to recover the hidden numeric threshold. The audio will state something like "The maximum allowed path weight is [NUMBER]". 

3. **Build the Pipeline Validator (Adversarial Filter):**
   Write a Python script at `/home/user/validator.py` that processes build dependency graphs (JSON files) and classifies them. The script must be invoked as:
   `python3 /home/user/validator.py check <path_to_json>`
   It must print exactly `CLEAN` or `EVIL` to standard output.

   **Validation Rules:**
   - **Schema Migration:** If the JSON has `"version": 1`, it uses the key `"dependencies"` for edges. You must migrate this in-memory to v2, which uses the key `"deps"`.
   - **Expression Parsing via ABI:** Each node in the JSON graph has an `"expr"` string (e.g., `"3 * 4 + 2"`). Your Python script MUST load the fixed `libmathparser.so` using `ctypes` and call its `double eval_expr(const char* expr)` function to compute the node's numeric weight.
   - **Graph Traversal & Cycle Detection:** The JSON represents a directed graph of build tasks. If the graph contains any cycles (circular dependencies), it is `EVIL`.
   - **Threshold Enforcement:** For valid Directed Acyclic Graphs (DAGs), calculate the maximum weight path through the graph. The weight of a path is the sum of the evaluated weights of its nodes. If the maximum path weight is strictly greater than the numeric threshold transcribed from `/app/directive.wav`, it is `EVIL`.
   - If the graph is a valid DAG and its maximum path weight is less than or equal to the threshold, it is `CLEAN`.

Ensure your `validator.py` accurately identifies all provided clean schemas as `CLEAN` and rejects all malicious/invalid schemas as `EVIL`. Do not hardcode the threshold; your script should extract or define it based on the audio transcription.