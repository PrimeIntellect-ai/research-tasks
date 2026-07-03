You are helping a technical writer organize a new documentation system. The writer has recorded their instructions in an audio file, and provided a set of raw documentation files. 

Your task is to build a C-based tool that processes these documents according to the dictated instructions, and generates a final manifest.

Here are the steps you must follow:
1. **Transcribe the Audio**: Listen to (or transcribe) the audio file located at `/app/instructions.wav`. It contains the specific rules for how to organize, split, and merge the documentation files located in `/home/user/docs/`.
2. **Create a Configuration File**: Based on the transcription, create a configuration file named `/home/user/config.ini`. The format of this file is up to you, but it must be machine-readable by your C program.
3. **Write the C Program**: Create a C program at `/home/user/doc_manager.c`. This program must:
   - Read and interpret `/home/user/config.ini`.
   - Perform the required file splitting, merging, and chunking on the files in `/home/user/docs/`.
   - Calculate the SHA-256 checksums of all the **final** output files (the chunks and merged files). You may use external commands via `popen` or `system` to compute the hashes if you prefer, or implement/link a crypto library.
   - Generate a JSON manifest file at `/home/user/manifest.json` containing the filenames and their corresponding SHA-256 checksums. The JSON should be an array of objects, e.g., `[{"filename": "chunk_1.txt", "hash": "..."}]`.
4. **Execute**: Compile your C program to `/home/user/doc_manager` and run it to produce the processed files and `/home/user/manifest.json`.

Ensure your C code correctly handles binary/text file I/O and efficiently manages memory during splits and merges. 

The success of your task will be evaluated based on the accuracy of the checksums in your `manifest.json` compared to our hidden reference manifest.