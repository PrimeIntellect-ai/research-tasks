You are an on-call engineer responding to a 3 AM page. The legacy audio processing pipeline is producing corrupted output for high-amplitude signals.

A previous engineer left a voicemail about the issue before their shift ended, located at `/app/voicemail.wav`. The original processing script was accidentally deleted from the working directory, but the local git repository at `/app/repo` might still have traces of it in its reflog.

Your task:
1. Recover the deleted script from the git repository in `/app/repo`. 
2. Transcribe or listen to `/app/voicemail.wav` to discover the missing "magic constant" used in the audio scaling formula.
3. The recovered script is written in Python and uses `numpy`. It multiplies 16-bit integer audio samples by the magic constant, then divides by 256. However, it currently suffers from 16-bit signed integer overflow during the multiplication step, causing the corrupted output on x86 architectures.
4. The `/app/repo/requirements.txt` has a dependency conflict preventing it from installing. Fix the conflict and ensure the environment can run your code.
5. Fix the overflow bug and the missing constant. Write the corrected, fully functional script to `/home/user/fix.py`.

Your script `/home/user/fix.py` must:
- Read a single line from standard input containing a comma-separated list of integers (representing 16-bit audio samples).
- Apply the scaling formula: `(sample * magic_constant) // 256` for each sample.
- Print a single line to standard output containing the comma-separated list of processed integers.
- Handle the arithmetic correctly without overflowing intermediary values.

Automated verification will pass random lists of integers to your script and compare its output against a reference oracle.