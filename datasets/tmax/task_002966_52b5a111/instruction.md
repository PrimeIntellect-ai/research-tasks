You are tasked with building an automated curation pipeline for an audio artifact manager. We regularly receive batches of voice recordings (in WAV format) that need to be safely archived. However, some recordings contain sensitive spoken markers—specifically the words "CONFIDENTIAL" or "RESTRICTED"—and must be strictly excluded from the archives.

Your objective is to write a Bash script at `/home/user/curate_audio.sh` that acts as a filter and packager.

The script must accept exactly two arguments:
1. An input directory containing `.wav` files.
2. The path to an output `.tar.gz` archive.

Requirements for `/home/user/curate_audio.sh`:
1. **Transcription & Filtering**: For each `.wav` file in the input directory, the script must transcribe the spoken audio. You may install and use any CLI transcription tool you see fit (e.g., `openai-whisper` via pip, or `whisper.cpp`). If the spoken text contains the word "CONFIDENTIAL" or "RESTRICTED" (case-insensitive), the file must be **rejected**.
2. **Manifest Generation**: For all **accepted** (clean) files, compute their SHA256 checksums and file sizes in bytes. Generate a valid JSON file named `manifest.json` structured as follows:
   ```json
   {
     "files": [
       {
         "filename": "audio1.wav",
         "sha256": "...",
         "size": 12345
       }
     ]
   }
   ```
3. **Archiving**: Create a compressed tar archive (`.tar.gz`) at the specified output path containing ONLY the accepted `.wav` files and the generated `manifest.json` at the root of the archive. Do not include directory structures (the files should be at the root of the archive).

To help you test your solution, a sample dataset is provided under `/app/sample_corpus/` containing a mix of `.wav` files. 

Constraints:
- You must use Bash as the primary language for your script. 
- You must ensure the script gracefully handles inputs and correctly parses the transcription outputs.
- The pipeline will be evaluated against a hidden adversarial corpus to ensure 100% of sensitive files are rejected and 100% of clean files are preserved.