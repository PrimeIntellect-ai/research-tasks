We have a background service that processes incoming audio recordings. The service uses a C-based utility, `/app/audio_filter`, to apply a custom normalization and filtering algorithm. However, we've noticed two severe issues:
1. The utility has a memory leak that causes the service to crash over long runs.
2. The output exhibits minor floating-point precision degradation compared to our original Python prototype (`/app/ref_filter.py`).

Your task is to:
1. Analyze the C source code located at `/app/src/audio_filter.c`.
2. Trace the memory allocations to identify and fix the memory leak. 
3. Identify where floating-point precision is being lost in the algorithmic loop and correct the math or types so the precision matches the Python prototype exactly.
4. Compile your fixed version to `/home/user/audio_filter_fixed`.

We have provided a sample audio file at `/app/sample_recording.wav` that you can use to test your changes. You can run `./audio_filter /app/sample_recording.wav output.bin` and compare it to `python3 /app/ref_filter.py /app/sample_recording.wav ref_output.bin`. 

Your final compiled executable `/home/user/audio_filter_fixed` must behave identically to `/app/ref_filter.py` for any valid WAV file input, producing byte-for-byte identical binary output files without leaking memory.