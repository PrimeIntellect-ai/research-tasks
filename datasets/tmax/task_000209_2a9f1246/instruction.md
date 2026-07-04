You are an MLOps engineer tasked with fixing a critical data leakage issue in our experiment tracking pipeline. A recent scikit-learn pipeline inadvertently leaked evaluation data into the training features via an improper `fit_transform` step. 

A senior engineer investigated the issue and left an audio report detailing the exact nature of the leak, but they didn't implement the fix before going on leave.

Your objectives:
1. **Extract the Leak Signature:** Listen to (transcribe) the audio report located at `/app/audio/leakage_report.wav`. You can use the pre-compiled Whisper tool located at `/opt/whisper/main` along with the model at `/opt/whisper/models/ggml-base.en.bin` to transcribe it. The audio contains a specific 3-word token sequence that represents the leaked data.

2. **Build the Leakage Detector:** Write a C++ program at `/home/user/artifact_filter.cpp` that reads our experiment artifact CSV files. 
   - The CSV files have a header row and three columns: `experiment_id,timestamp,train_features`.
   - The `train_features` column contains space-separated string tokens.
   - Your C++ program must parse the CSV, tokenize the `train_features` column, and check if the exact 3-word token sequence from the audio report appears *consecutively* anywhere in the `train_features` (case-insensitive).
   
3. **Program Interface:** 
   - Compile your program to `/home/user/artifact_filter`.
   - It must take a single command-line argument: the path to a CSV file (e.g., `./artifact_filter /path/to/data.csv`).
   - If **any** row in the CSV contains the leaked sequence, print `STATUS: LEAKED` to standard output and exit with return code `1`.
   - If **no** rows contain the leaked sequence, print `STATUS: CLEAN` to standard output and exit with return code `0`.

4. **Test against Corpora:** We have provided two directories of CSV artifacts to validate your filter:
   - `/app/corpora/clean/` : Contains CSVs with no leakage.
   - `/app/corpora/evil/` : Contains CSVs where data has leaked.
   Ensure your compiled `./artifact_filter` correctly flags 100% of the files in both directories.

Please write, compile, and thoroughly test your C++ program against the provided corpora.