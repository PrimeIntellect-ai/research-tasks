You are a build engineer managing artifact telemetry. The lead developer left a voice memo in an audio file located at `/app/equation.wav`. This memo contains a spoken mathematical expression that calculates the new cache retention threshold.

Your task is to:
1. Transcribe the audio file to text to recover the spoken mathematical expression. You may write a Python script using standard transcription libraries (assume `openai-whisper` or similar is available in your environment, or you can use an external API if you have the keys, or simply mock the transcription if you can understand it by other means, though programmatic transcription is expected).
2. Write a C++ program (`/home/user/evaluator.cpp`) that reads this mathematical expression.
3. The C++ program **must** implement a custom Abstract Syntax Tree (AST) data structure and a parser (e.g., recursive descent) to parse the expression. 
4. The C++ program should evaluate the AST and output the final numerical result to `/home/user/result.txt`.
5. Compile your C++ program using `g++` and run it to produce the final `result.txt`.

Ensure your C++ program can handle basic arithmetic operations (addition, subtraction, multiplication, division) and parentheses, as well as floating-point numbers. Write the final computed number to `/home/user/result.txt` as a standard floating-point string.