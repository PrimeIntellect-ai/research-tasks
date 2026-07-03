You are a Build Engineer responsible for managing artifacts and build pipelines for a mathematical signal processing project. 

In `/home/user/signal_project/`, there is a small C project consisting of `main.c`, `poly_filter.c`, `poly_filter.h`, and a `Makefile`. The project currently fails to build due to linking errors. 

Your tasks are to:
1. Identify and fix the linking errors in the `Makefile`.
2. Enhance the `Makefile` to support conditional cross-compilation. If `ARCH=aarch64` is passed to `make`, it should use `aarch64-linux-gnu-gcc`. If `ARCH=x86_64` (or no `ARCH`) is passed, it should use standard `gcc`. The output executable should be named `poly_tool_aarch64` or `poly_tool_x86_64` respectively.
3. The core mathematical algorithm in `poly_filter.c` is missing its initialization coefficients (labeled as `TODO` in the code). The required coefficients have been provided to us in an audio memo located at `/app/memo.wav`. You must process this audio file (you may install Python libraries like `SpeechRecognition` or use system tools like `ffmpeg` or `whisper`) to extract the three integer coefficients spoken in the recording.
4. Inject these extracted coefficients into `poly_filter.c` to complete the `apply_filter(int x)` function. The function should calculate `(C1 * x^3 + C2 * x^2 + C3 * x) % 1000000007` where C1, C2, C3 are the transcribed coefficients in order.
5. Successfully compile the `poly_tool_x86_64` executable.
6. Write a small CI/CD bash script at `/home/user/signal_project/ci_build.sh` that installs the `gcc-aarch64-linux-gnu` cross-compiler via `apt-get` (assuming sudo-less or appropriately permissioned environment, you can use `sudo apt-get`), then builds both architectures.

To successfully complete the task, your compiled `/home/user/signal_project/poly_tool_x86_64` must mathematically match the expected behavior perfectly when given random integer inputs.