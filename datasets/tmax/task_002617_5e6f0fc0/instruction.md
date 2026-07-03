You are a data engineer building a robust ETL pipeline for a fleet of IoT sensors. The raw telemetry data is transmitted in a proprietary binary format (`.bin`). We have a legacy, stripped C binary located at `/app/legacy_parser` that can read these files and output the raw numerical matrices, but we have a problem: malicious actors are injecting poisoned telemetry logs into our ingestion pipeline.

We have managed to isolate a set of known good logs and known poisoned logs:
- Clean corpus: `/home/user/corpus/clean/`
- Poisoned (Evil) corpus: `/home/user/corpus/evil/`

Your task is to write a Python script at `/home/user/filter.py` that acts as a gatekeeper in our ETL pipeline. It must:
1. Accept exactly one command-line argument: the path to a `.bin` file.
2. Use the `/app/legacy_parser` to extract the numerical data. You will need to figure out how to invoke the parser by examining it or experimenting with the provided corpora.
3. Use linear algebra and statistical properties to determine if the data is clean or poisoned. (Hint: The sensors have a specific physical constraint that manifests in the dimensionality/covariance of the clean signals. The poisoned data generators failed to replicate this constraint).
4. Exit with status code `0` if the file is clean, and exit with status code `1` if the file is poisoned.

Your script will be tested against a hidden holdout set of clean and evil `.bin` files. You must achieve 100% accuracy on the holdout set to pass. You may use standard data science libraries like `numpy`, `scipy`, and `pandas`.