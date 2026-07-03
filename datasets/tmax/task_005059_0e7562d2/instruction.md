You are an AI assistant helping a researcher organize and process environmental sensor datasets.

We receive daily sensor dumps in a proprietary binary format. We use a provided compiled tool to decode these dumps, but the tool occasionally produces corrupted feature sets due to sensor malfunctions or decoding bugs. We need you to build a robust ETL and modeling pipeline that can filter out these corrupted readings and train a diagnostic classifier.

Here are the components you have to work with:
1. **Decoder Utility**: A stripped binary located at `/app/sensor_decode`. It takes an input binary file and an output CSV path: `/app/sensor_decode <input.bin> <output.csv>`.
2. **Raw Data**: A directory of raw sensor dumps at `/app/data/raw/`.
3. **Metadata**: A CSV file at `/app/data/metadata.csv` containing the `reading_id` and the target label `status` for each dump.

Your objectives:

**Part 1: Anomaly Detection (Filter)**
By exploring the output of `/app/sensor_decode` on the raw data, identify the signatures of corrupted decodings (e.g., physically impossible environmental values).
Create a Python script at `/home/user/filter.py` that takes a decoded CSV file path as its first command-line argument.
- It must exit with code `0` if the CSV contains valid, clean data.
- It must exit with code `1` if the CSV contains corrupted or impossible data (e.g., negative humidity, temperature below absolute zero, or malformed columns).

**Part 2: ETL Pipeline & Classification**
Create a script (e.g., bash or python) to process all `.bin` files in `/app/data/raw/`.
1. Decode each file using `/app/sensor_decode`.
2. Use your `filter.py` to discard corrupted outputs.
3. Join the clean decoded data with `/app/data/metadata.csv` on the `reading_id` field.
4. The classes in `status` are highly imbalanced. Implement bootstrap sampling (up-sampling the minority class) to balance the training set.
5. Train a classification model (e.g., RandomForest) using the joined, balanced data to predict the `status` label based on the sensor features.
6. Evaluate the model and save the standard classification report (e.g., from scikit-learn) to `/home/user/report.txt`.

Ensure your scripts are thoroughly tested. An automated verification suite will test your `/home/user/filter.py` against hidden "clean" and "evil" (corrupted) corpora.