You have been tasked with building a custom binary archiving tool to help organize our project files. Our team lead left an audio memo detailing the exact binary format specifications for this custom archive. 

Here is what you need to do:

1. **Extract the Specification:**
   Listen to or transcribe the audio memo located at `/app/format_spec.wav`. The memo dictates the precise magic bytes, header structure, endianness, and field types required for the archive format.

2. **Implement the Archiver:**
   Write a Python 3 script at `/home/user/pack_project.py` that implements this custom format. 
   - The script must be invokable as: `python3 /home/user/pack_project.py <input_dir> <output_archive>`
   - It must recursively traverse the given `<input_dir>` and find all files.
   - Files must be packed into the archive in strict case-sensitive alphabetical order based on their *relative path* to `<input_dir>`.
   - The script must use atomic file writes: write the archive to a temporary file (e.g., `<output_archive>.tmp`) and only rename it to `<output_archive>` once the entire packing process is successfully completed.

3. **Validation:**
   Your implementation must be BIT-EXACT equivalent to our internal reference implementation. An automated fuzzer will run your script against dozens of randomly generated directory structures containing binary and text files. If your output deviates by even a single byte, or if the headers/data are misaligned, the test will fail. 

You may install any required Python libraries (e.g., `openai-whisper`, `SpeechRecognition`, etc.) using `pip` to process the audio file.