You are an AI assistant helping a technical writer organize and format legacy documentation.

We are standardizing our documentation processing pipeline. You need to write a Bash script at `/home/user/process_doc.sh` that reads arbitrary text from standard input (`stdin`), applies a series of transformations, and writes the exact result to standard output (`stdout`).

The lead editor has left an audio memo at `/app/memo.wav` detailing a custom, legacy "compression" step that must be applied to the text. You must transcribe or listen to this audio file to understand the exact custom text transformation rule.

Additionally, you have a CSV dictionary at `/home/user/dict.csv`. 

Your script `/home/user/process_doc.sh` must perform the following operations in order on the incoming text:
1. **Dictionary Substitution:** Replace all exact string matches of the first column in `/home/user/dict.csv` with the second column.
2. **Custom Compression:** Apply the legacy inline text compression algorithm exactly as described in the `/app/memo.wav` audio recording.
3. **Line Numbering:** Prefix every resulting line with a 3-digit zero-padded line number (starting from 001), followed by a colon and a space (e.g., `001: `, `002: `).

Requirements:
- Your script must be written entirely in Bash (using standard coreutils like `sed`, `awk`, `tr`, etc.).
- Your script must handle arbitrary printable ASCII input accurately.
- Ensure the script is marked as executable. 
- You can use external tools like `ffmpeg` or `whisper` to transcribe the audio if needed.