You are a security researcher analyzing a suspicious Bash-based data extraction tool found on a compromised system. The tool parses mathematical sequences but intermittently produces incorrect results due to precision loss and signed integer overflow when handling specific inputs. 

Your goals are to diagnose the bug, recover missing fuzzing infrastructure, extract the operational parameters, and build a robust detector to classify inputs.

Step 1: Audio Analysis
We intercepted a voicenote from the attacker at `/app/intercepted_signal.wav`. You need to transcribe this audio file (you may use the `whisper` CLI tool available on the system) to find the hidden seed value and boundary constraint used for their payload generation. Write this exact transcript to `/home/user/transcript.txt`.

Step 2: Deleted File Recovery
The attacker tried to delete their fuzzer script, but a raw disk image of their workspace is located at `/app/workspace.img`. Recover the deleted Bash script named `fuzzer.sh` from this image and place it at `/home/user/fuzzer.sh`.

Step 3: Root Cause Analysis & Fuzzing
Analyze `fuzzer.sh` to understand how it generated inputs that cause the extraction tool (`/app/extract.sh`) to fail via arithmetic precision loss. Use the seed and boundary constraint from the audio file to configure the fuzzer. 

Step 4: Build the Detector (Adversarial Corpus Verification)
We have collected a corpus of mathematical payloads. You must create a Bash script at `/home/user/detector.sh` that takes a single file path as an argument.
The script must:
- Exit with status `0` (and output nothing) if the file contains a "clean" mathematical sequence that `/app/extract.sh` can process without precision loss.
- Exit with status `1` (and output nothing) if the file contains an "evil" sequence designed to trigger the integer overflow or precision loss bug.

Your solution will be tested against our hidden corpora. Your `detector.sh` must successfully accept 100% of the clean corpus and reject 100% of the evil corpus.