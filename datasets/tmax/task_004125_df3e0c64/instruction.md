You are an AI assistant helping a technical writer organize a large, nested set of documentation archives. The writer has left a voice memo detailing exactly how they want incoming documentation streams to be processed. 

Your task:
1. Locate and transcribe the voice memo found at `/app/voice_memo.wav`. You can use `whisper` (which is pre-installed in the environment) or any other transcription tool to understand the instructions.
2. Based on the instructions in the memo, write an executable script at `/home/user/archive_tool` (in any language you prefer, e.g., Bash, Python, etc.).
3. The script must read a stream from `stdin` and write its output to `stdout`.
4. Ensure your script handles temporary files cleanly and efficiently, as the streams can be large.
5. Make sure the script is executable (`chmod +x`).

The automated test suite will run your `/home/user/archive_tool` against hundreds of generated input streams and compare its bit-exact output to a hidden reference implementation. Ensure your script's logic perfectly matches the requirements described in the audio.