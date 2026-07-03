You are a performance engineer working on an experimental bio-acoustics processing pipeline. Our new audio-based sequencing hardware captures signals as short `.wav` files. Valid genetic signals contain stable, distinct pitch patterns, whereas empty pores or misreads produce unstructured wideband noise.

Currently, the pipeline is extremely slow because it runs full downstream sequence alignment on *all* audio clips, including the noise. We need a fast, compiled upstream filter to discard the noise.

Your task:
1. **Compile Audio Analysis Software**: We need you to use the `aubio` library's pitch tracking. Download, configure, and compile `aubio` from source (you can clone `https://git.aubio.org/aubio/aubio` or use its GitHub mirror `https://github.com/aubio/aubio.git`). Ensure the `aubiopitch` binary is successfully built and accessible.
2. **Develop a Profiling Classifier**: Write a Bash script at `/home/user/filter.sh` that takes a single `.wav` file path as its first argument. 
3. **Statistical Thresholding**: Your script must run the compiled `aubiopitch` on the input file, extract the pitch confidence or frequency characteristics, and perform a statistical hypothesis comparison to determine if a stable signal is present. 
4. **Adversarial Verification**: We have provided two corpora of audio samples:
   - `/app/corpus/clean/`: Contains 20 valid signal sequences (these must be ACCEPTED).
   - `/app/corpus/evil/`: Contains 20 noise-only misreads (these must be REJECTED).
   Your script `/home/user/filter.sh` must exit with code `0` if the file is a valid signal (clean) and exit with code `1` if it is noise (evil). You must perform convergence testing on these sets to find the exact threshold that achieves 100% accuracy on both corpora.
5. **Fixture Analysis**: We have also provided a raw, uncut continuous sequence recording at `/app/sample.wav`. Once your filter is perfected, profile it against this file (e.g., by splitting it or analyzing it whole) and log the average pitch frequency of the valid segments to `/home/user/fixture_analysis.log`.

Requirements:
- Your classifier `/home/user/filter.sh` must be written primarily in Bash and be highly optimized.
- You must use `aubiopitch` (compiled from source) as the core matrix/signal feature extractor.
- Ensure all required dependencies for compilation are installed.