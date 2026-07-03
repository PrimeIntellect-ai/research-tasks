You have been assigned to fix and complete a multi-file C project located at `/app/audio_math_server`. This project is a mathematical Digital Signal Processing (DSP) WebSocket server. It receives audio processing commands via URL routing over WebSockets, parses custom mathematical filter expressions using a state machine, applies them to an input audio file, and writes the result.

Currently, the project is in a broken state:
1. **Compilation Failures**: Running `make` fails due to conflicting definitions and circular dependencies between `router.h`, `state_machine.h`, and `audio_buffer.h`. This is similar to a conflicting peer dependency issue, but in C header inclusion.
2. **Incomplete Interpreter**: The state machine parser in `state_machine.c` that evaluates the mathematical string expressions for the filters is missing the logic for the "moving_average" command.

Your tasks are:
1. **Fix the Build**: Refactor the C headers and Makefile in `/app/audio_math_server` so that the project compiles cleanly with `make` without warnings.
2. **Implement the Filter Interpreter**: Complete the state machine in `state_machine.c` to parse and apply a simple moving average filter. The parser should recognize the command format `MA(W)` where `W` is an integer window size.
3. **Process the Audio**: Start the compiled server (`./dsp_server 8080`). Write a client script to connect via WebSocket to `ws://localhost:8080/process?filter=MA(5)&input=/app/noisy_speech.wav&output=/app/output.wav`.
4. **Verification**: The server should generate `/app/output.wav`. The processed audio must significantly reduce the high-frequency noise from the original `/app/noisy_speech.wav` file. 

The final output must be located exactly at `/app/output.wav`. Our automated test will evaluate the Mean Squared Error (MSE) between your `/app/output.wav` and a pristine reference waveform. The MSE must be strictly lower than the specified threshold.