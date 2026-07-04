I need you to fix a broken data cleaning pipeline. 

We use a pre-trained model to filter out noisy text rows before they hit our database. The previous engineer vendored a custom version of our text classification library at `/app/fastText`. However, it currently fails to build and install when you run `pip install /app/fastText`. There appears to be a misconfiguration in how the compiler flags or environment are set up in the package's build files. 

Your tasks are to:
1. Debug and fix the build configuration for the vendored package in `/app/fastText` so that it compiles. Install it into the current Python environment.
2. Write a reproducible data processing script at `/home/user/filter_script.py` (make sure it has a proper shebang and is executable).
3. The script must process text read from `stdin` line-by-line.
4. For each line, apply this specific feature engineering/preprocessing step: lowercase the string and remove all characters except `a-z` and space (` `). 
5. Pass the preprocessed string to the fastText model located at `/app/cleaner_model.bin` using the python bindings (`import fasttext`).
6. If the model's top predicted label is exactly `__label__keep` AND the confidence probability is `>= 0.60`, print the **original, unmodified** line to `stdout`. Do not print anything else.

The final script will be rigorously tested against a reference implementation using thousands of random strings. Numerical accuracy and exact text matching are critical.