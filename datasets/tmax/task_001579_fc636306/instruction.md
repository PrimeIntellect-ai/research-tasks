You are acting as an automated compliance officer auditing internal trading systems.

A senior auditor has dictated the logic for our new real-time compliance query engine, but the transcription team hasn't processed the audio file yet. 

You have access to the dictated audio file at:
`/app/compliance_dictation.wav`

Your task is to:
1. Transcribe the audio file to understand the specific data querying logic and schema required. You may use any transcription tools available in the environment (e.g., Python, ffmpeg, or whisper if installed).
2. Write a C program at `/home/user/audit_query.c` that implements the query engine described in the audio. 
3. The C program must read from standard input (stdin) and write to standard output (stdout).
4. Compile the program to `/home/user/audit_query`. 

The program should act as a stream processor (effectively implementing the requested SQL window function / analytical aggregation logic manually in C). Ensure your output perfectly matches the schema and conditions dictated in the audio. Handle standard input until EOF.

Do not print any extra text, prompts, or debugging information to stdout. The compiled binary `/home/user/audit_query` will be rigorously tested against a fuzzing verifier with random inputs to ensure absolute equivalence to the auditor's reference implementation.