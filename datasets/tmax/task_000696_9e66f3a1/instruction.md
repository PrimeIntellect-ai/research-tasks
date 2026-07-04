You are a security researcher analyzing an intercepted communications and a partially recovered piece of malware source code. Your goal is to reverse-engineer the malware's activation sequence, patch the broken source code to run it safely, extract a hidden token using intercepted audio, and finally emulate the malware's Command and Control (C2) server.

You have been provided with the following in your environment:
1. `/app/intercepted.wav`: An audio recording intercepted from the threat actor. It contains spoken English text with an activation sequence.
2. `/home/user/c2_decoder/`: A directory containing the source code of the malware's payload decoder (written in C) and a `Makefile`.

**Phase 1: Source Code Debugging**
The threat actor's source code in `/home/user/c2_decoder/decoder.c` is buggy and currently fails to compile and run. You must debug and fix it. The code suffers from several issues:
- A build failure preventing compilation.
- An off-by-one error leading to memory corruption/segfaults when processing input buffers.
- A numerical instability bug causing a `NaN` (Not a Number) output during the signal variance calculation.
- An infinite recursion / missing base case in the recursive key-derivation function, causing a stack overflow.

Identify and fix these issues so the program compiles cleanly using `make` and runs without crashing.

**Phase 2: Audio Analysis**
Analyze the audio file at `/app/intercepted.wav`. Transcribe the spoken words. The recording contains a spoken phrase ending in a sequence of numbers (e.g., "nine five two"). Convert these numbers into digits (e.g., "952").

**Phase 3: Token Generation**
Run the compiled `decoder` binary, passing the transcribed digit sequence as the only command-line argument:
`./decoder <digits>`
If fixed correctly, the decoder will output an alphanumeric activation token.

**Phase 4: Emulate the C2 Server**
Write and run a script in a language of your choice to start a C2 emulation server listening on exactly `127.0.0.1:8080`.
The server must implement the following HTTP endpoints:
- `GET /ping`: Must return a `200 OK` response with the plaintext body `pong`.
- `POST /register`: The verifier will send an HTTP POST request to this endpoint with a JSON body: `{"agent": "test_bot"}`. The request will include an `Authorization` header in the format: `Authorization: Bearer <TOKEN>`, where `<TOKEN>` is the exact token you generated in Phase 3. 
If the token matches, the server must return a `200 OK` response with the JSON body `{"status": "registered", "transcript": "<FULL_AUDIO_TRANSCRIPT>"}`.

Leave the server running in the background or foreground so that the automated test suite can verify its behavior.