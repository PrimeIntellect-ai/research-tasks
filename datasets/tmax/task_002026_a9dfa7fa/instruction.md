Hello! I'm a data analyst and I've inherited a broken ETL pipeline that processes daily transaction CSV files. We have a multi-service architecture that ingests these CSVs, runs anomaly detection, and plots the results, but right now nothing is working together. 

I need you to fix the pipeline, implement the missing Bayesian anomaly detection logic, and get our services communicating properly.

Here is the setup in `/home/user/app/`:
- **Services:** We have a Redis message broker, a FastAPI ingestion service, and a Python worker process. They are launched via `/home/user/app/start_services.sh`. Currently, the FastAPI service and worker are failing to connect to Redis due to missing or incorrect environment variables in `/home/user/app/.env`. 
- **The Data:** I have two sets of historical CSV records: `/home/user/app/data/clean/` (normal transactions) and `/home/user/app/data/evil/` (synthetic fraudulent transactions designed to bypass basic filters).
- **The Anomaly Detector:** The Python worker uses `/home/user/app/detector.py` to classify records. Right now, this file just returns `True` for everything. You need to implement a Bayesian inference model in `detector.py` using `scipy` or `numpy` that calculates the posterior probability of a transaction being anomalous based on the 'amount' and 'location_frequency' columns. The `classify(csv_row_dict)` function must return `True` if it's a valid transaction (clean), and `False` if it's anomalous (evil).
- **The Plotter:** The script `/home/user/app/plot_results.py` reads the output logs and generates a summary chart `summary.png`. However, when I run it on this server, it completes without errors but `summary.png` is just a completely blank white image. Please fix this script so it actually renders the plot (hint: it might be a display backend issue).

**Your objectives:**
1. Fix the environment configuration so all three services start up and communicate properly.
2. Fix the plotting script so it successfully draws the data instead of a blank image.
3. Write the Bayesian logic in `detector.py`. 
4. Process both the `clean` and `evil` CSV corpora through the pipeline. 

To verify your solution, our automated test will run `/home/user/app/verify.py`. This script will feed the corpora through the API, which passes them via Redis to your worker, which uses your `detector.py`. It requires your classifier to correctly reject 100% of the evil records and preserve 100% of the clean records.