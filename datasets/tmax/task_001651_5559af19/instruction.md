You are a data scientist building an automated anomaly detection pipeline to filter out adversarial sensor telemetry before it reaches our main database.

We have a multi-service architecture located in `/app/` that is currently broken. It consists of:
1. **Nginx** (Reverse Proxy)
2. **Flask API** (Job Ingestion)
3. **Redis** (Message Broker)
4. **JupyterLab** (Workflow Orchestration)

Your task has two main phases:

### Phase 1: Pipeline Configuration (Multi-Service Compose)
The services are not talking to each other. You need to configure and start them:
1. Configure Nginx (`/etc/nginx/sites-available/default`) to listen on port `8080` and proxy requests for the `/api` location to the Flask app running on `127.0.0.1:5000`.
2. Ensure Redis is running on default port `6379`.
3. Start the Flask application (`/app/api.py`) so it listens on port `5000`.
4. Ensure the end-to-end flow works: `curl -X POST http://localhost:8080/api/enqueue -H "Content-Type: application/json" -d '{"filepath": "/app/corpus/clean/sample1.csv"}'` should successfully push a job to the Redis `sensor_jobs` queue.

### Phase 2: Implement the Statistical Detector in C
You must implement the core analytical worker, a C program that will be executed against individual CSV files. 

Write a C program at `/app/detector.c` and compile it to `/app/detector`. 
The program must take a single command-line argument (the path to a CSV file).
The CSV files contain observational data with two columns: `X` and `Y` (floats, with a header row).

Your C program must:
1. Parse the CSV file and reshape the observational data into memory arrays.
2. Perform an optimization routine (Gradient Descent) to fit a simple linear regression model: $Y = mX + c$. 
   - Initialize $m = 0, c = 0$. 
   - Use a learning rate of `0.01` for `1000` iterations.
3. Calculate the Mean Squared Error (MSE) of the fitted model against the data points.
4. **Classification Rule**: We are filtering out data injected by malicious actors that breaks our assumed statistical distributions.
   - If the MSE is **greater than 5.0**, the data is anomalous. The program must print "REJECT" and exit with status code `1`.
   - If the MSE is **less than or equal to 5.0**, the data is clean. The program must print "ACCEPT" and exit with status code `0`.

You can test your compiled `/app/detector` against the corpora provided:
- **Clean Corpus**: `/app/corpus/clean/` (Contains 50 normal CSV files)
- **Evil Corpus**: `/app/corpus/evil/` (Contains 50 anomalous CSV files with heavy-tailed structural breaks)

Compile with: `gcc -O2 /app/detector.c -o /app/detector -lm`

To complete the task, ensure the services are running and your `/app/detector` binary perfectly separates the clean files from the evil files.