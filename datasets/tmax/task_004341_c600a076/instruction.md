You are a support engineer tasked with recovering diagnostic logs from a crashed embedded system. The system's only output during the crash was a diagnostic LED, which a field technician recorded on video. You have access to this video, a local Git repository with our diagnostic tools, and standard Linux utilities.

Your task consists of three parts:

1. **Extract the Signal:**
   Analyze the video at `/app/diagnostic_blink.mp4`. The video is recorded at exactly 10 frames per second. Each frame is either purely black (representing binary `0`) or purely white (representing binary `1`). Extract the full sequence of bits from the video and save it as a continuous string of `0`s and `1`s (no spaces or newlines) in `/app/extracted_bits.txt`.

2. **Recover the Secret Key:**
   Navigate to the local repository at `/app/diag_tools`. The tool requires a specific secret system key to decrypt the logs. The key was accidentally removed from the current branch, but it was committed somewhere in the Git history. Perform repository forensics to recover this key.

3. **Fix the Decoder:**
   The decoding script at `/app/diag_tools/decode.py` contains a critical bug. It is supposed to take a binary string as a command-line argument, internally use the recovered secret key, and output the decoded diagnostic text to standard output. However, it currently crashes with an error or produces malformed output due to a logic flaw in how it chunks and processes the binary data. Use a debugger or manual inspection to identify and fix the bug. Update the script so that the secret key is hardcoded correctly as the `SECRET_KEY` variable inside the file.

Your final `/app/diag_tools/decode.py` script must be completely robust. To verify your fix, our automated test suite will run your script against thousands of randomly generated binary sequences and compare its standard output to a verified oracle implementation. 

Ensure your fixed script can be invoked exactly like this:
`python3 /app/diag_tools/decode.py <binary_string>`

Do not change the command-line interface of the script. Only output the final decoded string to `stdout`.