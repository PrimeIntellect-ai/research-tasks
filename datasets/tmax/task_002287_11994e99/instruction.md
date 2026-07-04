We are currently cleaning a large dataset of environmental audio recordings (bird sounds). Unfortunately, our collection pipeline was compromised, and several recordings have been injected with a synthetic adversarial "drone sweep" signal. 

We need you to build a C++ based data-cleaning tool that can robustly detect and filter out these corrupted recordings. 

You are provided with a small sample corpus in `/app/sample_corpus/` which contains two subdirectories: `clean/` and `evil/`. 
Inside these directories, you will find mono, 16kHz WAV files alongside corresponding JSON metadata files (e.g., `recording_1.wav` and `recording_1.json`).

The JSON metadata contains calibration parameters for the sensor that recorded the audio. It looks like this:
```json
{
  "recording_id": "rec_1",
  "gain_factor": 1.15,
  "offset": -0.02
}
```

You are also provided with `/app/reference_sweep.csv`, which contains a 1D array of floating-point values representing the known amplitude envelope of the adversarial synthetic sweep (sampled at 100 Hz, i.e., one value per 10ms).

Your task is to write a reproducible ETL pipeline in C++ that processes an audio file, joins it with its calibration metadata, and detects the anomaly via similarity search.

Specifically, write a C++ program `/home/user/detector.cpp` and a build script `/home/user/build.sh` (which compiles it to `/home/user/detector`). The compiled binary must accept exactly one argument (the path to a WAV file) and behave as follows:

1. **Multi-source Join:** For the given input `/path/to/audio.wav`, automatically locate and read `/path/to/audio.json`.
2. **Transform (ETL):** Read the WAV file (we recommend installing and using `libsndfile` and `nlohmann-json` via system packages). Convert the 16-bit PCM samples to normalized floats in the range [-1.0, 1.0].
3. **Calibration:** Apply the metadata calibration to every sample `x`: `adjusted_x = (x * gain_factor) + offset`.
4. **Feature Extraction:** Compute the amplitude envelope. Group the adjusted samples into non-overlapping windows of 160 samples (10ms at 16kHz). For each window, compute the average of the absolute values of the adjusted samples. This gives an envelope sequence.
5. **Similarity Search & Numerical Accuracy:** Compute the Pearson correlation coefficient between the extracted envelope sequence and the reference sequence from `/app/reference_sweep.csv`. (Both sequences will have the same length; truncate to the shorter one if there are minor rounding differences).
6. **Classification:** If the Pearson correlation is >= 0.80, the file is corrupted. The program must print "EVIL" to standard output and terminate with exit code `1`. If the correlation is < 0.80, print "CLEAN" and terminate with exit code `0`.

Ensure your `build.sh` installs any necessary dependencies (e.g., `libsndfile1-dev`, `nlohmann-json3-dev`) and compiles the C++ code successfully. We will run your detector against a hidden adversarial corpus using your compiled `/home/user/detector`.