You are a data engineer responsible for fixing and rebuilding an ETL and modeling pipeline. We use a custom C implementation for similarity search and classification to minimize overhead.

You are provided with a training dataset `/app/train.csv` (formatted as 4 floating-point features and 1 integer label per row, separated by commas) and a test dataset `/app/test.csv` (4 features per row, no labels). 

Unfortunately, the pipeline configuration file was corrupted, but we recovered a screenshot of the configuration dashboard located at `/app/config.png`. 

Your tasks are to:
1. Extract the pipeline configuration parameters from the image `/app/config.png` (you can use OCR tools like `tesseract`, which is preinstalled).
2. Write a C program (e.g., `pipeline.c`) that parses the CSV datasets.
3. Implement a K-Nearest Neighbors (KNN) classification algorithm from scratch in C, using the specific distance metric and `K` value extracted from the image. In case of a tie, default to the smaller class label.
4. Perform 5-fold cross-validation on `/app/train.csv` using your C model, and print the average validation accuracy to standard output (this acts as our model output validation step).
5. Finally, train the model using the entire `/app/train.csv` dataset and predict the class labels for `/app/test.csv`.
6. Save the predictions to `/home/user/predictions.csv`. The file should contain exactly one integer label per line, directly corresponding to the rows in `/app/test.csv`.

You must implement the core logic in C, though you can use bash or Python for extracting the text from the image and orchestrating the build/run process. 

Your final predictions in `/home/user/predictions.csv` will be evaluated for accuracy against a hidden ground-truth file.