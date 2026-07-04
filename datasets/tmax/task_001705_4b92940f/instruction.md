You are a performance engineer at a high-frequency trading firm. Our core pricing engine is a proprietary, highly-optimized C++ executable located at `/app/engine`. Unfortunately, the source code was lost, and the binary is stripped.

Recently, the engine has been sporadically crashing in production, bringing down the pipeline. We believe the crashes are due to numerical instability caused by certain edge-case input parameters, but we cannot modify the binary. 

Your task is to write a Python pre-filter (a sanitizer) that can inspect incoming parameter payloads and reject ones that will cause the engine to crash, while accepting all valid payloads.

We have gathered a dataset of historical parameter payloads (in JSON format) to help you:
- `/app/data/clean/`: Contains 50 payloads that process successfully.
- `/app/data/evil/`: Contains 50 payloads that cause the engine to crash, hang, or emit fatal numerical errors.

Additionally, the engine requires a secret authorization token passed as the first command-line argument to run, followed by the path to the JSON file. (e.g., `/app/engine <TOKEN> <input.json>`). The current team doesn't know the token, but we believe an old deployment script containing the token was accidentally committed to the git repository at `/home/user/legacy_wrapper` before being deleted.

Your objectives:
1. Perform git forensics on `/home/user/legacy_wrapper` to recover the engine's secret authorization token.
2. Analyze the stripped binary (`/app/engine`) and its behavior on the `clean` and `evil` datasets to deduce the exact numerical conditions that cause a crash. (You may use tools like `strings`, `gdb`, or simply treat it as an oracle).
3. Create a Python script at `/home/user/sanitizer.py` that implements your filtering logic.

The script MUST have the following interface:
- It must accept a single command line argument: the path to a JSON file.
- It must print exactly `SAFE` to standard output (with a newline) and exit with code 0 if the payload is safe.
- It must print exactly `UNSAFE` to standard output (with a newline) and exit with code 1 if the payload would crash the engine.

Your solution will be tested against the provided clean and evil corpora, as well as a hidden holdout set. You must achieve 100% accuracy (all clean preserved, all evil rejected).