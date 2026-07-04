We have an incident regarding our video processing pipeline. A critical Python script, `extract_metadata.py`, is used to parse custom subtitle/metadata tracks from video files and output a precise frame-by-frame event log. However, it's currently failing in production.

First, the script processes an MP4 video file located at `/app/incident_evidence.mp4`. Recently, it started crashing with a segmentation fault (likely deep within a native library called by Python during specific frame extraction), and we have captured a core dump at `/home/user/core.dump`. 

Second, even when it doesn't crash, the output is incorrect. The script is supposed to calculate precise timestamp boundaries for events. However, due to floating-point precision loss and an off-by-one boundary condition in the parsing logic, it misses frames or parses malformed timestamps incorrectly. Furthermore, a wrapper shell script `process.sh` fails entirely if the video's internal title metadata contains spaces.

Your task is to:
1. Analyze the core dump to find the exact frame index that causes the crash in the native extension. (You can write a minimal wrapper to isolate it).
2. Use delta debugging principles to isolate the exact malformed metadata string format that triggers the off-by-one error.
3. Fix `extract_metadata.py` so that it handles format parsing edge cases correctly without precision loss, avoids the crash, and processes filenames/metadata with spaces properly.

The repaired script must be placed at `/home/user/extract_metadata_fixed.py`.
It must take two arguments: the path to the video file, and an integer offset.
Execution format: `python3 /home/user/extract_metadata_fixed.py <path_to_video> <offset>`

It must print a sequence of JSON objects (one per line) representing the parsed and corrected event metadata. 
Our automated testing system will fuzz your script with various inputs and compare its output against a reference implementation to ensure exact bit-for-bit equivalence.