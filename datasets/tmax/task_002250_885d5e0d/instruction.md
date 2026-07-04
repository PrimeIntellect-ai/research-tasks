You are an open-source maintainer reviewing a pull request for our project's audio event processing pipeline. A contributor has submitted a PR containing a C program (`/home/user/pr_review/event_parser.c`) meant to parse a stream of transcription timestamps and tags, and a Bash orchestration script (`/home/user/pr_review/process_audio.sh`) that extracts data from an audio transcription. 

Unfortunately, the PR is broken in multiple ways:
1. The C program (`event_parser.c`) contains memory safety issues (buffer overflows and use-after-free bugs) when handling deeply nested event tags, causing it to crash on malformed inputs.
2. The Bash script (`process_audio.sh`) fails to correctly sort, merge, and diff the outputs from our legacy transcription engine against the new outputs. It is missing the state machine parser logic required to filter out background noise tags.

Your task:
1. Fix the undefined behavior and memory leaks in `/home/user/pr_review/event_parser.c` without changing its core state-machine logic. Compile it to `/home/user/pr_review/event_parser`.
2. Complete `/home/user/pr_review/process_audio.sh` so that it takes a raw text input (simulated transcription), passes it through `event_parser`, sorts the events by timestamp, and outputs a clean, merged list of events.
3. We have an audio file located at `/app/test_sample.wav`. The Bash script must be able to process the text transcript generated from this audio file (the transcript is provided at `/home/user/pr_review/sample_transcript.txt`).
4. Most importantly, your fixed `process_audio.sh` (which calls your compiled `event_parser`) must behave EXACTLY like our closed-source reference implementation located at `/app/oracle_processor`. 

We will verify your solution by fuzzing your `/home/user/pr_review/process_audio.sh` with thousands of randomly generated transcription strings and asserting that its standard output exactly matches the standard output of `/app/oracle_processor` for every input.

Make sure your final executable Bash script is at `/home/user/pr_review/process_audio.sh`.