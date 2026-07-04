You are a Machine Learning Engineer preparing training data for a new retrieval model. Your pipeline requires cleaning raw text files, sampling from them, and computing initial embeddings. 

However, your environment has a few broken pieces, and you need to build a robust filtering script.

**Step 1: Fix the Vendored Package**
You have a vendored package located at `/app/text-sampler-0.5.0`. This package provides bootstrap sampling and basic neural network architecture reconstruction for our dummy embeddings. 
Unfortunately, the previous engineer made a mistake in the package configuration. The `setup.py` attempts to link against a numerical library incorrectly (it enforces `numpy==99.9.9`, which is impossible). 
Fix the configuration in `/app/text-sampler-0.5.0` so it can be installed, and install it in your environment (`pip install /app/text-sampler-0.5.0`).

**Step 2: Create a Data Filter (Adversarial Corpus)**
You need to write a Bash script at `/home/user/filter_data.sh` that takes a single file path as an argument.
The script must enforce our data schema and reject adversarial data.
A file is considered **VALID (clean)** if:
1. The first line is exactly `SCHEMA_VERSION=1.0`
2. It contains strictly valid ASCII characters (no binary/control characters other than standard whitespace/newlines).
3. It does NOT contain any line starting with the exact string `[INJECT]`.

A file is considered **INVALID (evil)** if it violates any of the above rules.
Your script `/home/user/filter_data.sh <file_path>` must exit with status `0` if the file is valid, and exit with status `1` if the file is invalid.

You have been provided with two directories for testing:
- `/home/user/corpora/clean/` : Contains examples of valid files.
- `/home/user/corpora/evil/` : Contains examples of invalid files.
*Note: The automated verification system will test your script against a hidden holdout set of clean and evil files. Your script must correctly classify 100% of them.*

**Step 3: Data Processing Pipeline**
Write a Bash script at `/home/user/pipeline.sh` that takes an input directory and an output directory as arguments:
`/home/user/pipeline.sh <input_dir> <output_dir>`

For every file in the `<input_dir>`:
1. Run it through your `/home/user/filter_data.sh`.
2. If it passes (valid), use the `text-sampler` CLI tool (installed in Step 1) to extract a bootstrap sample of exactly 5 lines. The command syntax is `text-sampler --file <file_path> --n 5 > <output_dir>/<filename>.sample`.
3. If it fails (invalid), ignore it.

Ensure your scripts have the correct execution permissions.