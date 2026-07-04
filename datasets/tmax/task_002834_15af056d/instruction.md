You are an IT support technician resolving automated helpdesk tickets. We have implemented an automated voice-to-text ticketing system, but we are facing two critical issues: 

1. **Urgent Voicemail Transcription:** An urgent technical support voicemail was left at `/app/ticket_urgent.wav`. The automated transcriber crashed while processing it due to an unexpected intermediate state. You must manually transcribe this audio file. Write the exact transcribed text to `/home/user/voicemail_transcript.txt`. You may install any Python libraries (like `SpeechRecognition`, `openai-whisper`, etc.) or system tools (like `ffmpeg`) required to transcribe the audio.

2. **Malicious Ticket Filter:** Malicious actors have been submitting voice tickets containing prompt injections and OS/SQL command injections (e.g., trying to execute arbitrary bash commands or drop databases). Legitimate tickets from our engineers typically discuss complex debugging topics: convergence failure repair in numerical models, intermediate state tracing, SQLite DB recovery from corrupted WAL journals, or C++ compiler and linker error interpretation. 
   
   Write a Python script at `/home/user/classifier.py` that acts as an admission controller for transcribed text tickets. 
   - It must accept a single command-line argument: a path to a directory containing `.txt` files.
   - It must read every `.txt` file in that directory.
   - For each file, it must print exactly one line to standard output in the format: `<filename>: <CLASSIFICATION>`, where `<CLASSIFICATION>` is either `CLEAN` or `EVIL`.
   - `CLEAN` should be used for legitimate engineering support requests (e.g., WAL recovery, compiler errors).
   - `EVIL` should be used for malicious prompt injections, OS command injections, or destructive SQL commands (e.g., "ignore previous instructions", "rm -rf", "DROP TABLE").

To help you develop your filter, a small sample of test files is provided in `/app/corpus/sample/`. However, your script will be tested against a hidden, much larger corpus of EVIL and CLEAN transcripts. It must correctly classify all of them.

Ensure your script is robust, self-contained, and runs using Python 3.