You are a data scientist stepping in to clean a dataset for our next-generation speech-to-text models. Recently, we discovered a severe data leakage issue: test set transcripts and corrupted logs were accidentally mixed into the incoming unverified data batches. Your job is to create a robust, Bash-only data sanitization filter to identify and reject the contaminated files.

You must create an executable bash script at `/home/user/sanitizer.sh`. This script will be run against a large dataset to determine if each file should be preserved or rejected.

Your script must take a single argument: the absolute path to a text file.
It must exit with code `0` if the file is CLEAN (preserve).
It must exit with code `1` if the file is EVIL/CONTAMINATED (reject).

To determine the filtering logic, you must synthesize three rules:

1. **The Audio Directive (Similarity/Extraction):**
   The project manager left a voice memo about a specific leaked identifier that contaminated the test set. The audio file is located at `/app/manager_notes.wav`. You must transcribe or extract the spoken content of this audio file (you may use `whisper` or standard tools available in your environment). The audio contains a specific alphanumeric "Project Codename". Any text file containing this exact codename must be rejected.

2. **The Train-Test Leak (Model Validation):**
   We have a master list of training set document IDs in `/app/train_master_ids.txt` (one ID per line). Each text file in the corpus contains an ID on its first line in the format `DOC_ID: <ID>`. If a file's ID matches ANY ID in the training master list, it is a data leak and must be rejected.

3. **Hypothesis Testing on Line Counts:**
   Corrupted files often have abnormal lengths due to duplication loops. We have a sample of verified clean file line counts in `/app/baseline_line_counts.txt`. 
   Using Bash utilities (`awk`, `bc`, etc.), calculate the mean and the sample standard deviation of these baseline counts. 
   Compute the 95% confidence interval for the population of clean files (use Z = 1.96). 
   Any file whose total line count falls strictly outside this calculated [lower_bound, upper_bound] interval (inclusive) must be rejected as an anomaly.

You can explore the files and test your script using the provided corpora:
- Clean examples (must exit 0): `/app/corpus/clean/`
- Contaminated examples (must exit 1): `/app/corpus/evil/`

Ensure your `/home/user/sanitizer.sh` is thoroughly tested against these directories, as we will use a hidden evaluation set with the same characteristics to grade your script.