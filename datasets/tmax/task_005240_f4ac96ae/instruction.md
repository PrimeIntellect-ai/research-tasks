You are tasked with diagnosing and fixing a regression in a custom network packet parser used for audio streams.

A critical git repository containing our Python-based network pipeline has been encrypted. The password to decrypt it was left in a voicemail. 

Stage 1: Transcription
1. You will find an audio file at `/app/voicemail.wav`.
2. Transcribe the spoken content of this audio file. It contains the decryption password.
3. Use the password (all lowercase, no spaces) to decrypt and extract the repository:
   `openssl enc -aes-256-cbc -d -in /app/pipeline_repo.tar.gz.enc -out /home/user/repo.tar.gz -pass pass:<YOUR_PASSWORD>`
4. Extract `/home/user/repo.tar.gz` to `/home/user/repo/`.

Stage 2: Bisection & Diagnosis
1. Inside `/home/user/repo/`, there are 200 commits. The `main` branch contains a regression.
2. The repository contains `parser.py` and `test_pipeline.py`. `test_pipeline.py` currently fails on `main`.
3. Use `git bisect` to find the commit that introduced the regression. 
4. The regression is related to format parsing edge-cases: specifically, how the parser handles corrupted network packets where the declared `header_length` byte indicates a length larger than the actual payload. The buggy commit causes a crash (IndexError/ValueError) instead of gracefully rejecting the packet.

Stage 3: Repair
1. Checkout the `main` branch.
2. Fix the bug in `parser.py`. When a packet's `header_length` exceeds the total packet byte size, the parser should catch this corrupted input edge-case and gracefully output `{"error": "corrupted length"}`.
3. Ensure your fixed code passes `python3 test_pipeline.py`.

Stage 4: Integration
1. Save your fully repaired script as `/home/user/final_parser.py`.
2. The script must be executable from the command line and take exactly one argument: a Base64-encoded packet string.
   Example: `python3 /home/user/final_parser.py "AQIDBA=="`
3. It must print exactly a JSON string to `stdout` containing the parsed fields or the error message, matching the legacy system's behavior.

Automated verification will random-fuzz your `/home/user/final_parser.py` against our reference oracle with thousands of malformed packets to guarantee bit-exact behavioral equivalence.