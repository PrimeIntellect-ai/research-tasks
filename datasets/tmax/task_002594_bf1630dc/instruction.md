You are tasked with developing a robust configuration parsing script for our new Configuration Management Database (CMDB) tracking system. 

We are migrating away from a legacy system. The previous systems administrator left a voicemail explaining the exact encoding and quirky formatting rules of the legacy configuration files, which is saved at `/app/sysadmin_voicemail.wav`.

Your task:
1. Extract the instructions from the audio file `/app/sysadmin_voicemail.wav`. You may install tools like `openai-whisper` or `ffmpeg` to transcribe or listen to the file.
2. Based on the rules specified in the voicemail, write a Python 3 script at `/home/user/parse_config.py`.
3. The script must read the raw binary legacy configuration from `stdin`, parse it according to the audio's instructions, apply the required encoding and text transformations, and print a tightly-formatted JSON object (with no extra whitespace, e.g., `json.dumps(data, separators=(',', ':'))`) to `stdout`.

Your script will be tested against a rigorous automated fuzzing suite. The test will generate thousands of randomized legacy configuration files and compare your script's JSON output against a reference implementation. Your script's output must be **bit-exact** equivalent to the reference implementation.

Requirements for `/home/user/parse_config.py`:
- Read from `sys.stdin.buffer`.
- Output valid JSON to `sys.stdout`.
- Handle arbitrary key-value pairs that follow the legacy format structure.
- Execute quickly and cleanly without extraneous print statements.