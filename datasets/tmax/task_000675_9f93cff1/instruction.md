Hello,

We are upgrading our data cleaning pipeline for our machine learning models. We need a high-performance C filter that applies Bayesian smoothing to incoming dataset streams. 

Currently, our old pipeline suffers from "data leakage" because it calculates smoothing parameters across the entire dataset (train and test combined). We've built a new microservice system to correctly perform cross-validation and hyperparameter tuning strictly on the training set to find the optimal Dirichlet prior parameters (`alpha` and `beta`).

Your task consists of two parts:

**Part 1: Service Configuration & Parameter Extraction**
In `/app/services/`, you will find two services:
1. A Redis server
2. A Python Flask API (`/app/services/api/app.py`)

The Flask API is designed to run cross-validation and store the best hyperparameters in Redis, but its configuration is incomplete. 
- You need to configure the environment variables for the Flask API so it can connect to the local Redis instance (it expects `REDIS_HOST` and `REDIS_PORT`).
- Start both the Redis server and the Flask API.
- Send a `POST` request to `http://127.0.0.1:5000/tune`. This will trigger the Bayesian hyperparameter tuning. The API will save the optimal parameters under the keys `cv_alpha` and `cv_beta` in Redis.
- Extract these two float values from Redis.

**Part 2: C Filter Implementation**
Write a C program at `/home/user/bayes_filter.c` and compile it to an executable named `/home/user/bayes_filter`.
- The program must read a stream of floating-point numbers from standard input (`stdin`), one number per line, until EOF.
- For each input number $x$, compute the smoothed value $y$ using the formula:  
  $y = \frac{x + \alpha}{\beta + 1.0}$
  (where $\alpha$ and $\beta$ are the exact parameters you extracted from Redis).
- Output each computed $y$ to standard output (`stdout`), one per line, formatted to exactly 4 decimal places (e.g., using `%.4f`).
- Compile your program optimally using `gcc`. You may use standard C libraries (`math.h`, `stdio.h`, `stdlib.h`).

Do not hardcode guesses for `alpha` and `beta`—you must retrieve the correctly tuned values from the service setup.