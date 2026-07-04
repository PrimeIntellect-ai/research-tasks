You are an ML engineer tasked with migrating our training data preprocessing pipeline from a legacy compiled C++ tool to a pure Python implementation for easier integration into our modern PyTorch stack.

Your objective is to create a Python script, `/home/user/py_feature_extractor.py`, that behaves EXACTLY like the legacy preprocessor located at `/app/legacy_feature_extractor` (a stripped binary).

To accomplish this, follow this workflow:
1. **Scientific Software Compilation**: The source code for our raw signal generator is located in `/app/signal_gen_src/`. Compile it using `make` to produce an executable named `signal_gen` in that directory.
2. **Dataset Generation**: Run `/app/signal_gen_src/signal_gen` to output 10,000 raw signal data points (floats, one per line) and redirect the output to `/home/user/raw_signals.txt`.
3. **Reference Dataset Creation**: Pass `/home/user/raw_signals.txt` through the legacy binary via standard input (`cat /home/user/raw_signals.txt | /app/legacy_feature_extractor > /home/user/legacy_features.txt`).
4. **Notebook Orchestration**: We have provided a Jupyter notebook template at `/home/user/analyze_transform.ipynb` to help you reverse-engineer the legacy transformation parameters. Update the notebook to load the two text files, fit a model to find the smoothing factor (alpha) and the activation scale (beta), and run it headlessly (e.g., using `jupyter nbconvert --to notebook --execute`).
5. **Implementation**: Write `/home/user/py_feature_extractor.py`. It must read a sequence of floats from standard input (one per line) and print the transformed features to standard output (one per line, formatted to exactly 6 decimal places). 

The legacy binary applies a standard Exponential Moving Average (EMA) followed by a non-linear activation function. Ensure your Python implementation matches the legacy binary's output bit-for-bit for any sequence of valid floating-point inputs.