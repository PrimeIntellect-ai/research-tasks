I am a researcher trying to organize a multi-source dataset for an NLP model training pipeline, but I'm running into frustrating data type inconsistencies that are corrupting my tokenized sequences.

I have a custom data preparation package that I've vendored into my environment, located at `/app/text_feature_toolkit`. It handles tokenization and dataset preparation by joining textual data with external metadata before converting them to feature vectors. However, there is a bug in the package: when it joins the main dataset with the metadata, it's silently introducing `NaN` values for missing entries, which causes Pandas to upcast my crucial integer token IDs into floats. Because of this, the downstream vocabulary mapping fails or produces invalid floating-point tokens that my PyTorch model rejects.

Your task is to fix this pipeline and write a processing script. Here are the requirements:

1. **Fix the Vendored Package:**
   - Investigate the source code in `/app/text_feature_toolkit`. Identify where the multi-source data joining is occurring.
   - Fix the silent float conversion issue. The join operation should strictly maintain the integer types for all ID columns, filtering out any rows that lack corresponding metadata rather than padding them with `NaN`s (i.e., ensure it performs a strict inner join, not a left join).
   - Reinstall/update the package in the environment as needed.

2. **Implement the Processing Pipeline:**
   - Create a Python script at `/home/user/process_stream.py`.
   - This script must read exactly one line of JSON from `stdin`. The JSON will have two keys: `"text"` (a string) and `"meta_id"` (an integer).
   - Using the fixed `text_feature_toolkit.processor` module, process the input. The package expects to look up the `"meta_id"` in a local reference CSV located at `/app/reference_meta.csv`.
   - Print the final processed feature vector (a list of integers representing the combined text and metadata tokens) to `stdout` as a comma-separated string, with no brackets (e.g., `12,45,102,8,99`). If the `meta_id` is not found in the reference CSV, the script should output `INVALID`.

Ensure your script handles standard input correctly, as it will be continuously tested against an oracle with thousands of random inputs.