You are acting as a Support Diagnostics Engineer. A client has reported that their custom C++ diagnostic agent is crashing when trying to retrieve system information, but only after they authenticate. 

The client left a voicemail detailing the administrative PIN needed to access the system, which has been saved to `/app/voicemail.wav`. 

You have the source code for the diagnostic server at `/home/user/diagnostic_server.cpp`.

Your tasks are to:
1. Extract the administrative PIN spoken in `/app/voicemail.wav`. You may install and use any transcription tools (like `ffmpeg`, `whisper`, etc.) or simply listen to it if you have a way to pipe the audio locally, but transcribing it programmatically or via CLI is expected.
2. Compile `/home/user/diagnostic_server.cpp` into an executable named `/home/user/diag_server`.
3. The server is designed to listen on `0.0.0.0:9090`. Run it.
4. Interact with the server over HTTP to reproduce the crash. The client mentioned the crash occurs on the `GET /diagnostics` endpoint, but you must first hit the `POST /auth` endpoint using the PIN from the voicemail to activate the diagnostic module.
5. Use a debugger (`gdb`) or system call tracer (`strace`) to analyze why the C++ server crashes when `GET /diagnostics` is requested.
6. Fix the bug in `/home/user/diagnostic_server.cpp`. Do not remove the endpoints; just fix the memory corruption or logic error causing the crash.
7. Recompile the server and leave it running in the background listening on `0.0.0.0:9090`.

An automated verifier will issue HTTP requests to `0.0.0.0:9090` to ensure:
- The server responds correctly to `/auth` with the PIN from the audio.
- The server successfully returns data on `/diagnostics` without crashing.

Please leave the fixed server running as a background process.