You are an automation specialist responsible for modernizing a legacy data processing pipeline. 

We have a legacy text processing binary located at `/app/oracle_processor`. We need to replace this black-box binary with a maintainable Python script. Unfortunately, the original documentation was lost, but a former engineer left a voice memo detailing the exact algorithmic rules, character encodings, tokenization steps, and validation gates the binary uses.

The voice memo is located at `/app/pipeline_specs.wav`.

Your task:
1. Transcribe the audio file `/app/pipeline_specs.wav` to recover the pipeline specifications. You may install and use any transcription tools you need (e.g., `ffmpeg`, `openai-whisper`).
2. Implement the text processing pipeline in a Python script at `/home/user/processor.py`.
3. Your script must read raw binary data from standard input (`sys.stdin.buffer`), apply the exact sequence of transformations, normalizations, and validations described in the audio, and write the final output to standard output (`sys.stdout.buffer`).
4. Ensure your implementation is BIT-EXACT equivalent to the `/app/oracle_processor` binary. You can test your script against the binary by feeding both the same random byte strings.

Your final deliverable must be the script at `/home/user/processor.py`. An automated verifier will randomly generate thousands of inputs and assert that your Python script produces the exact same byte-level output as `/app/oracle_processor`.