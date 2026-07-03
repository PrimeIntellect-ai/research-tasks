You are a mobile build engineer maintaining our automated UI testing pipelines. We have a custom video analysis tool that extracts frames from UI test recordings and calculates visual metrics using a custom expression parser written in C++. This tool is orchestrated via a Python script. 

Currently, the pipeline is broken:
1. The C++ library (`/home/user/pipeline_tool/src/evaluator.cpp`) has memory safety issues and undefined behavior (UB). It frequently crashes with segmentation faults or produces garbage outputs due to uninitialized memory and buffer overflows.
2. The build script (`/home/user/pipeline_tool/build.sh`) is incomplete and fails to properly orchestrate the polyglot build (compiling the C++ code into a shared library that Python can load via `ctypes`).
3. The custom expression parser inside the C++ code is evaluating basic arithmetic incorrectly due to operator precedence bugs and integer division truncation.

Your task:
1. Fix the C++ source code in `/home/user/pipeline_tool/src/evaluator.cpp` to eliminate all memory leaks, undefined behavior, and arithmetic parsing bugs. The evaluator computes a per-pixel score based on a provided string expression (e.g., `R*0.299 + G*0.587 + B*0.114`) and returns the average score for the frame.
2. Fix `/home/user/pipeline_tool/build.sh` so that it successfully compiles the C++ code into a shared library named `libevaluator.so` in the `pipeline_tool/lib` directory.
3. Use the provided Python script `/home/user/pipeline_tool/process.py` to analyze the test recording located at `/app/test_recording.mp4`.
4. The Python script will output the frame-by-frame analysis to `/home/user/output.json`.

Run the pipeline:
`cd /home/user/pipeline_tool`
`bash build.sh`
`python3 process.py /app/test_recording.mp4 "R*0.299+G*0.587+B*0.114" /home/user/output.json`

Ensure your fixed C++ code runs efficiently and correctly. We will verify the correctness of your `output.json` by calculating the Mean Squared Error (MSE) against our ground truth. Your output must achieve an MSE of less than 0.01.