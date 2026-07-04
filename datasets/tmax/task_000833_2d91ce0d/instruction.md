You are an Machine Learning Engineer tasked with preparing a training data pipeline for an IoT predictive maintenance model. We need a robust data filtration script that can automatically reject corrupted or adversarial data points before they poison our training set.

Our senior data scientist left a screenshot of the exact numerical constraints and rules required for valid data. This image is located at `/app/specs/validation_rules.png`. You must extract the validation rules from this image (you may use `tesseract` or any other tool you prefer).

We have provided a small sample of representative data:
- `/app/corpus/clean/`: Contains valid CSV files that perfectly adhere to the rules.
- `/app/corpus/evil/`: Contains adversarial or corrupted CSV files that violate one or more rules.

Your task:
1. Extract the data validation thresholds from `/app/specs/validation_rules.png`.
2. Write a standalone validation script at `/home/user/filter_data.py` (or `.sh` if you prefer).
3. The script must accept exactly one argument: the absolute path to a CSV file.
   Usage: `python3 /home/user/filter_data.py /path/to/data.csv`
4. The script must parse the CSV (which contains headers: `timestamp`, `temperature`, `pressure`, `status`) and evaluate it against the rules from the image.
5. If the CSV strictly follows ALL rules, the script must exit with status code `0`.
6. If the CSV violates ANY rule, contains missing values (NaN/null) in numerical columns, or is malformed, the script must exit with status code `1`.

Your script will be tested against a hidden evaluation suite containing hundreds of clean and evil CSV files. Ensure your logic is numerically accurate and reproducible. You can test your script against the provided `/app/corpus/` directories to benchmark its performance before concluding.