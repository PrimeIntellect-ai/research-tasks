You are acting as a QA engineer. We have a broken C project at `/home/user/project` that implements a log sanitization utility. The previous engineer left an audio bug report at `/app/qa_report.wav` detailing the required business logic for the sanitizer, but left the implementation incomplete and the build system broken.

Your tasks are:

1. **Analyze the Audio:** Use available tools (e.g., `ffmpeg`, `whisper`, or Python speech recognition libraries you can install in your user environment) to transcribe the audio bug report at `/app/qa_report.wav`. It contains the exact rules for what constitutes a "clean" vs "evil" log file.
2. **Fix the Build System:** The `Makefile` in `/home/user/project` is broken. It fails to correctly link the mock library `libmocklog.a` (located in `/home/user/project/lib`) and fails to generate the executable in `/home/user/project/bin/`. Fix the `Makefile` so that running `make` successfully builds the project.
3. **Implement the Sanitizer:** Write the core logic in `/home/user/project/src/sanitizer.c`. You must implement a custom data structure (e.g., a Trie or efficient state machine) to process file streams efficiently.
4. **Create a Test Fixture:** Write a C program `/home/user/project/src/main.c` that compiles into `/home/user/project/bin/log_sanitizer`. The CLI invocation must be exactly:
   `/home/user/project/bin/log_sanitizer <filepath>`
   - It should exit with code `0` if the file is perfectly CLEAN.
   - It should exit with code `1` if the file is EVIL (violates any rule from the audio).
5. **Self-Test:** We have provided two local training corpora at `/app/corpus/clean/` and `/app/corpus/evil/`. Ensure your tool correctly accepts all files in the clean directory and rejects all files in the evil directory.

Once you are done, leave the compiled binary at `/home/user/project/bin/log_sanitizer`. The automated grading system will run your binary against a hidden evaluation corpus to determine success.