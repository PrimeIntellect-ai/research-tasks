You are tasked with building the core components of a voice-controlled configuration management system. System administrators dictate configuration changes as audio memos, and your pipeline must transcribe them, extract the intended updates, apply them to a base configuration file, mask sensitive data, and calculate a "configuration drift" score.

The system state is as follows:
- An audio memo dictating configuration updates is located at `/app/config_update.wav`.
- The current system configuration is located at `/home/user/base_config.json`. It is a simple flat JSON object.

Your task consists of the following steps:
1. **Transcription**: Extract the spoken text from `/app/config_update.wav` into `/home/user/transcript.txt`. You will need to install and configure an appropriate open-source offline speech-to-text tool (e.g., `whisper.cpp` with a tiny/base model). 
2. **C Implementation**: Write a C program located at `/home/user/config_updater.c` that does the following:
   - Reads `/home/user/base_config.json` and `/home/user/transcript.txt`.
   - Extracts the requested configuration updates from the transcribed text. The audio mentions changing three specific configuration keys.
   - Updates the corresponding keys in the JSON structure.
   - **Masking**: If any updated key name contains the substring `password` or `secret`, its new value must be replaced entirely with the literal string `***` in the final output.
   - **Distance Computation**: Computes the Levenshtein distance between the original unformatted JSON string and the newly updated unformatted JSON string.
   - Writes the new configuration to `/home/user/updated_config.json` (as a valid JSON string).
   - Writes the integer Levenshtein distance to `/home/user/drift.txt`.
3. Compile and execute your C program to process the files and generate the required outputs.

You may use standard C libraries. If you need a JSON library for C, you may download and compile a lightweight one (like `cJSON`), or write a simple string manipulation routine since the base JSON is flat and predictably formatted.

Deliverables expected for automated verification:
- `/home/user/updated_config.json` (Must accurately reflect the changes and masked secrets).
- `/home/user/drift.txt`