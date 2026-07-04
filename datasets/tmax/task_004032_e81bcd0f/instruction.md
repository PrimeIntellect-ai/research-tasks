You are a data engineer building an ETL pipeline to filter out noisy and corrupted audio segments from voice recordings before they are ingested into a machine learning model. 

You have been provided with an initial labeled training corpus of 1-second raw audio snippets (16-bit signed little-endian PCM, 8000 Hz, mono) located at:
- `/app/corpus/clean/` (contains valid voice segments)
- `/app/corpus/evil/` (contains corrupted/adversarial noise segments)

You also have a single long, unprocessed WAV recording at `/app/source.wav`.

Your task requires feature engineering, hyperparameter tuning in bash, and building a reproducible C-based pipeline.

Follow these steps:
1. **Feature Engineering in C**: Write a C program `classifier.c` (and compile it to `/home/user/classifier`) that reads raw 16-bit PCM data from `stdin`. It must calculate two features:
   - Mean Absolute Amplitude (MAA): The average of the absolute values of all samples.
   - Zero-Crossing Rate (ZCR): The fraction of adjacent sample pairs that have strictly different signs (i.e., one is positive and the other is negative, ignoring zeroes).
   The program must accept two command-line arguments: `<maa_threshold>` and `<zcr_threshold>`. It should exit with status `0` (clean) if `MAA > maa_threshold` AND `ZCR < zcr_threshold`. Otherwise, it should exit with status `1` (evil).

2. **Hyperparameter Tuning**: Write a bash script `/home/user/tune.sh` that performs a grid search over a reasonable range of MAA and ZCR thresholds. It must evaluate your compiled `classifier` against the provided `/app/corpus/` to find a combination of thresholds that achieves exactly 100% accuracy (accepts all clean, rejects all evil). 

3. **Pipeline Filter**: Create a wrapper script `/home/user/filter.sh <input.pcm>` that invokes your `classifier` with the optimal thresholds you discovered. This script will be used by our automated verifier. It must exit `0` for clean files and `1` for evil files.

4. **Integration**: Create a bash script `/home/user/process_source.sh` that processes the fixture `/app/source.wav`. The script must:
   - Convert the WAV file to raw PCM and split it into discrete 1-second chunks.
   - Pass each chunk through `/home/user/filter.sh`.
   - Concatenate all accepted (clean) chunks in their original order.
   - Convert the combined clean PCM data back into a valid WAV file at `/home/user/processed_output.wav` (8000 Hz, 16-bit mono).

**Verification requirements**:
- We will test `/home/user/filter.sh` against a hidden adversarial corpus of `clean/` and `evil/` PCM files. To pass, it must preserve 100% of the hidden clean corpus and reject 100% of the hidden evil corpus.
- We will inspect `/home/user/processed_output.wav` to ensure it only contains the clean chunks from the fixture.
- Do not hardcode specific filenames from `/app/corpus` into your logic; your filter must generalize based on the features.