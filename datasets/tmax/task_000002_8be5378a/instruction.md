You are tasked with debugging a failing step in our automated audio processing pipeline. 

We have an audio recording at `/app/voicemail.wav`. Our pipeline transcribes audio to text and then processes the transcript through a custom Python script: `/home/user/aligner.py`. 

Currently, the pipeline crashes with an `IndexError` when `aligner.py` processes the transcript of `/app/voicemail.wav`.

Your objectives are:
1. **Transcribe the Audio:** Listen to or programmatically transcribe `/app/voicemail.wav` to discover the exact text. You may install tools like `whisper`, `pocketsphinx`, or use any Python speech recognition libraries available.
2. **Reproduce the Bug:** Pipe the transcribed text (all uppercase, no punctuation, words separated by spaces) into `/home/user/aligner.py`. Observe the `IndexError` traceback.
3. **Analyze and Fix:** The `aligner.py` script is supposed to read space-separated words from standard input and group them into triplets (chunks of 3). If the final chunk has fewer than 3 words, it should pad the chunk with the string `"SILENCE"` until it has exactly 3 words. It should then print the chunks, one per line, with words separated by hyphens.
    * Example input: `ONE TWO THREE FOUR`
    * Expected output:
      `ONE-TWO-THREE`
      `FOUR-SILENCE-SILENCE`
4. **Correct the Boundary Condition:** Use delta debugging to isolate the exact boundary condition causing the off-by-one `IndexError` in the script. Modify `/home/user/aligner.py` so it accurately implements the padding logic without crashing, regardless of the input word count. 
5. **Verify:** Ensure `/home/user/aligner.py` reads from `stdin`, writes to `stdout`, and behaves identically to the specification for any arbitrary sequence of words. Automated fuzzing will be used to test your script against a hidden oracle.

Do not change the script's input/output interface (stdin to stdout). Fix the algorithmic logic inside `/home/user/aligner.py`.