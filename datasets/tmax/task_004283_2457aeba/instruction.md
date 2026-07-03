You are a performance engineer working on a bioinformatics pipeline. We are experiencing numerical instability and performance spikes when our `seq_profiler` tool processes certain edge-case observational datasets stored in FASTA format. 

Your objective is to build an automated sanitization script that identifies and rejects "bad" FASTA files before they enter the main pipeline. 

Here are your tasks:

1. **Information Extraction**:
   There is an audio log left by the lead researcher at `/app/field_notes.wav`. You must transcribe or listen to this audio file to find the specific numerical stability constraints and threshold values required for the filter. (Standard audio tools like `ffmpeg` or `whisper` are available in the environment).

2. **Compilation**:
   The source code for the profiler is located at `/app/src/seq_profiler.c`. Compile this scientific software from source into an executable named `seq_profiler` and place it in your home directory (`/home/user/seq_profiler`). Use standard GCC with `-O2` optimization and link the math library.

3. **Filter Implementation**:
   Write a pure Bash script at `/home/user/filter.sh`. 
   - The script must take exactly one argument: the absolute path to a FASTA file.
   - It must execute your compiled `/home/user/seq_profiler` on the provided FASTA file.
   - The profiler outputs a single metric to `stdout` (e.g., `Variance: 123.45`, `Variance: NaN`, or `Variance: Inf`).
   - Your script must parse this output and perform numerical stability testing.
   - Based on the constraints mentioned in the audio log, the script must `exit 0` if the file is "clean" (accepted), and `exit 1` if the file is "evil" (rejected due to instability, NaNs, Infs, or exceeding the threshold).

Ensure your script handles standard Bash constructs, arithmetic comparison (you may use tools like `awk` or `bc` for floating-point comparisons), and properly captures exit codes. 

We will test your `/home/user/filter.sh` against two hidden corpora of FASTA files. To pass, your script must accept 100% of the clean files and reject 100% of the evil files.