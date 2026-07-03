You are a data scientist responsible for cleaning and extracting features from a large-scale audio dataset. Your initial Python scripts for this task have proven too slow for the scale of data you are managing, so you need to reconstruct the extraction pipeline in Rust to benchmark inference and processing performance.

You are provided with a sample audio artefact at `/app/data/recording.wav` (16-bit PCM, 44100 Hz, mono). 

Your objective is to create a Rust project in `/home/user/audio_pipeline` that implements the following feature extraction and cleaning steps:
1. Parse the WAV file (you may use crates like `hound`).
2. Process the audio samples in non-overlapping frames of exactly 1024 samples. (If the last frame has fewer than 1024 samples, discard it).
3. For each frame, calculate the Root Mean Square (RMS) energy.
4. Apply a noise gate: if the RMS energy is strictly less than 0.05, classify the frame as "silence" and drop it.
5. For the remaining "active" frames, calculate the Zero-Crossing Rate (ZCR). We define ZCR here as the fraction of adjacent sample pairs within the frame that have different signs (i.e., `x[i] * x[i+1] < 0`). The ZCR should be a float between 0.0 and 1.0. (Treat a sample value of exactly 0 as having a positive sign).
6. Save the results to a JSON file. The output must be an array of objects, keeping the original temporal order of the frames. Each object must have:
   - `frame_index`: The integer index of the frame (starting at 0 for the first 1024 samples).
   - `rms`: The RMS energy (float).
   - `zcr`: The ZCR (float).

Your Rust program must be compiled in release mode. The resulting binary must be located at `/home/user/audio_pipeline/target/release/audio_pipeline`. 
It must accept exactly two command-line arguments: the input WAV file path, and the output JSON file path.
Example usage: `/home/user/audio_pipeline/target/release/audio_pipeline /app/data/recording.wav /home/user/features.json`

After building your project, run it on `/app/data/recording.wav` and output the results to `/home/user/features.json`.

An automated verifier will evaluate your compiled Rust binary on a much larger hidden dataset to benchmark its inference performance. It will measure the execution time and check the numerical accuracy of your extracted features against the reference implementation. Ensure your implementation is efficient!