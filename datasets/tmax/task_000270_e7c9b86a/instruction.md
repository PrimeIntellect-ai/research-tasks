You are a QA engineer setting up an automated UI test verification pipeline. 

We have a reference test execution recorded in a video file: `/app/reference_run.mp4`. During our test suites, a specialized testing overlay flashes a white 10x10 pixel square in the absolute top-left corner of the screen (coordinates 0,0 to 9,9) to indicate active test events.

Your task is divided into two parts:

1. **Video Extraction (Local Validation)**
Analyze `/app/reference_run.mp4` to extract a list of frame numbers where the top-left 10x10 square is considered "active" (average pixel luminance > 128). This represents the raw, noisy event log from the test. You may use `ffmpeg` and standard shell utilities to perform this extraction. Save the extracted frame numbers (one per line) to `/home/user/extracted_frames.txt`.

2. **Event Processor (Primary Implementation)**
Our test infrastructure generates unsorted, noisy streams of these frame numbers. You must create an executable program at `/home/user/event_processor` (in any language you choose, but ensure it is marked executable `chmod +x` and has an appropriate shebang if it's a script).

This program must:
* Read an arbitrarily long stream of text from `stdin`, where each line contains a single integer representing a frame number.
* Handle empty lines, unsorted inputs, and duplicate frame numbers gracefully.
* Deduplicate and sort the frame numbers numerically.
* Merge contiguous frame numbers into discrete event objects.
* Serialize the result as a strict JSON array of objects, outputted to `stdout`.

**Output Format Constraint:**
The JSON output must exactly match this schema and formatting (single-line JSON or properly formatted, but key order matters):
`[{"start": 12, "end": 15}, {"start": 40, "end": 40}]`
(Note: A solitary frame without contiguous neighbors should have the same `start` and `end` value).

**Verification:**
The automated test suite will rigorously test your `/home/user/event_processor` program. It will bypass your `/home/user/extracted_frames.txt` and directly feed your executable thousands of randomly generated, fuzzed input sets (simulating extreme test noise and edge-case frame overlaps), comparing your `stdout` byte-for-byte against our compiled, perfectly-conforming reference oracle. Ensure your logic for sorting, deduplicating, contiguous-sequence diffing, and JSON serialization is robust.