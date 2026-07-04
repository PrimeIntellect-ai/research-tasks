You are tasked with building a Bayesian data anomaly detector for our sensor pipeline. 

We have an image artifact at `/app/sensor_priors.png` that contains a table of the baseline distribution parameters (Normal distribution mean `mu` and standard deviation `sigma`) for three critical sensors: `Sensor_A`, `Sensor_B`, and `Sensor_C`. You will need to extract these parameters (using OCR or visual inspection).

Our pipeline processes data in "batches". Each batch is a directory containing two files:
1. `readings.csv` - Contains columns `id`, `Sensor_A`, `Sensor_B`.
2. `metadata.csv` - Contains columns `id`, `Sensor_C`.

**Your objectives:**
1. Write a Python script at `/home/user/detector.py` that takes a single command-line argument: the path to a batch directory.
2. The script must join the two CSV files on `id` to reconstruct the full sensor readings.
3. Using the extracted priors from the image, implement a probabilistic model to evaluate the batch. You should calculate the likelihood of the observed sensor readings assuming they are independent and normally distributed according to the priors.
4. "Clean" batches are drawn directly from the baseline distributions. "Anomalous" (evil) batches contain systematic deviations (e.g., shifted means or altered variances on one or more sensors).
5. The script must exit with status code `0` if it classifies the batch as "clean" (accept).
6. The script must exit with status code `1` if it classifies the batch as "anomalous" (reject).

To help you tune your threshold for anomaly detection, we have provided a small labeled training dataset:
- `/app/training_data/clean/` contains a few examples of clean batch directories.
- `/app/training_data/anomalous/` contains examples of anomalous batch directories.

**Constraints & Notes:**
- You may use any standard Python data science libraries (e.g., `pandas`, `numpy`, `scipy`).
- `pytesseract` and `tesseract-ocr` are preinstalled if you wish to extract the image text programmatically, though you can also read it and hardcode the values if you prefer.
- Your script must be robust and perform well on an unseen test corpus of clean and anomalous batches.

Ensure `/home/user/detector.py` is executable and accurately distinguishes the batches.