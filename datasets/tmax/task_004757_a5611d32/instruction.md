I am a dataset researcher organizing my lab's proprietary data. My predecessor created a custom archive format to store thousands of sensor readings, but they left the lab before documenting the exact binary specification. 

However, they did leave a voice memo at `/app/dataset_notes.wav` that supposedly explains how to parse these custom archive files, along with strict security warnings about how they used relative paths (including `../`) for some internal linking, which could lead to accidental overwrites if extracted blindly.

I need you to:
1. Figure out the archive format specification from the audio file.
2. Write a Go program at `/home/user/extractor.go` and compile it to `/home/user/extractor`.
3. The program must accept exactly two command-line arguments: the path to the archive file, and an absolute path to a target extraction directory.
   Usage: `/home/user/extractor <archive_file> <target_dir>`
4. The program should *not* actually extract the files or write any data to disk. Instead, it must strictly parse the archive and print to `stdout` line-by-line the disposition of each file entry as dictated by the rules in the voice memo.
5. Pay very close attention to the specific output prefixes and path sanitization rules mentioned in the audio recording. You will need to carefully resolve paths to detect escapes (often called "zip slip" vulnerabilities).

Ensure your compiled Go binary is executable and strictly adheres to the formatting rules in the voice memo, as it will be rigorously tested against thousands of generated archives. You may use any tools available or installable in the environment to transcribe the audio file.