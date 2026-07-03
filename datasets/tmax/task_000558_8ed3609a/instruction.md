Hello IT Support,

We have an urgent ticket escalated from the audio engineering team. They are using a legacy C-based audio effects processor (`/app/audio_filter.c`), but it has a severe numerical instability bug. Sometimes, processing certain WAV files causes the internal floating-point values to explode into NaNs (Not-a-Number), completely corrupting the output pipeline.

The user who reported the issue left a voicemail explaining the exact filter parameters that trigger the bug. We have saved their voicemail at `/app/ticket_1492_voicemail.wav`. 

Here is your workflow to resolve this ticket:

1. **Extract Parameters:** Listen to or transcribe the voicemail at `/app/ticket_1492_voicemail.wav` to obtain the `cutoff` frequency and `resonance` parameters the user mentioned. (You may use tools like `whisper`, `ffmpeg`, or Python libraries available in your environment).
2. **Diagnosis & MRE:** Analyze `/app/audio_filter.c` to understand the numerical instability (it appears to be an IIR filter where certain high-amplitude frequencies combined with the user's parameters push the poles outside the unit circle). 
3. **Build a Classifier:** We need to automatically quarantine files that will crash the pipeline. Write a C program at `/home/user/detector.c` and compile it to `/home/user/detector`. 
   - Your program must take a single command-line argument: the path to a WAV file.
   - It should read the WAV file, simulate the internal state of the filter using the parameters extracted from the voicemail, and detect if a NaN or Infinity would be produced.
   - If the audio file is safe, the program must exit with status code `0`.
   - If the audio file triggers the numerical instability (produces NaN/Infinity), the program must exit with status code `1`.

We have provided a corpus of test files to validate your detector:
- `/app/corpus/clean/` contains WAV files that process safely.
- `/app/corpus/evil/` contains WAV files that trigger the NaN explosion when used with the user's parameters.

Your compiled `/home/user/detector` must correctly classify 100% of the files in both directories. 

Good luck!