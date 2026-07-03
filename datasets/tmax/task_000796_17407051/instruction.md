You are an open-source maintainer reviewing a pull request for `WaveMath`, a Python CLI tool that applies mathematical expressions to audio file waveforms. The PR contributor has submitted a script `wave_math.py` that currently has severe security and performance issues.

Your task is to fix the script located at `/home/user/wave_math.py` to meet the following requirements:

1. **Security (Expression Parsing)**: The current PR uses Python's raw `eval()` to evaluate the math expression provided by the user. This is a massive security vulnerability. You must replace this with a safe expression parser and evaluator. Your script must successfully process valid mathematical expressions (e.g., `sin(x) * 0.5`, `x**2 + cos(x)`) and completely reject any malicious payloads (e.g., `__import__('os').system('id')`, `open('file.txt').read()`). The script must exit with status code 1 if an unsafe expression is detected. Only standard mathematical functions from the `math` or `numpy` module and the variable `x` (representing the audio sample array) should be allowed.

2. **Performance (Numerical Algorithm)**: The contributor processed the audio samples using a pure Python `for` loop, which is extremely slow. You must refactor the audio sample processing to use vectorized `numpy` operations. The tool should be able to process a 5-minute audio file in under 2 seconds on standard hardware.

3. **Audio Fixture Processing**: There is an audio file located at `/app/reference_audio.wav`. Once you have secured and optimized `wave_math.py`, use it to process `/app/reference_audio.wav` with the mathematical expression `x * 2.0`. Save the output to `/home/user/processed_audio.wav`.

4. **Integration**: The tool must maintain its original CLI interface: 
   `python wave_math.py <input_wav> <output_wav> "<expression>"`

Refactor the code to ensure it is secure, performant, and correctly processes the audio files.