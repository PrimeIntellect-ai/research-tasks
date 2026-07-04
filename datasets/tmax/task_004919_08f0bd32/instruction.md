I need you to help me fix and deploy a data science pipeline that simulates PCR amplification kinetics using ODEs based on primer design sequences. The pipeline consists of multiple cooperating services, but it's currently broken and the numerical integrator crashes on certain sequences.

The system is located in `/home/user/app/` and has the following components:
1. A Redis message broker.
2. A Celery worker (`worker.py`) that runs the ODE simulation for PCR kinetics.
3. A Flask API (`api.py`) that receives sequences and dispatches jobs to Celery.
4. An Nginx reverse proxy meant to expose the API.

First, you need to configure and start the multi-service architecture:
- Configure Nginx to listen on port 8080 and forward requests to the Flask API running on port 5000. The nginx config is at `/home/user/app/nginx.conf`. Start Nginx using this config.
- Start Redis (default port 6379).
- Start the Celery worker and the Flask application in the background.

Second, our ODE solver (using `scipy.integrate.solve_ivp` in the worker) diverges and crashes due to wrong step-size adaptation when it encounters "stiff" amplification kinetics caused by sequences with extreme GC content or tandem repeats. 
I have provided two datasets of sequences in FASTA format:
- `/home/user/data/clean_sequences.fasta`: Standard sequences that integrate smoothly.
- `/home/user/data/evil_sequences.fasta`: Pathological sequences that cause the integrator to diverge.

Your main task is to write a Python script `/home/user/app/classifier.py` that acts as an adversarial filter. It must take a path to a FASTA file as a command-line argument and output a JSON file named `classifications.json` in the current working directory. The JSON must map the FASTA sequence IDs to either the string `"accept"` (if it's safe to process) or `"reject"` (if it's an evil sequence that will cause divergence). 

Finally, create a Jupyter notebook `/home/user/app/orchestrate.ipynb` that automates this workflow: it should import your classifier, process a target FASTA file, and for every "accept" sequence, send a POST request to `http://localhost:8080/simulate` with JSON payload `{"sequence": "<ACTUAL_SEQUENCE_DATA>"}`. 

To complete the task:
1. Ensure all 4 services (Nginx, Flask, Redis, Celery) are running and properly communicating.
2. Write `/home/user/app/classifier.py` so that it rejects 100% of the evil corpus and accepts 100% of the clean corpus.
3. Ensure `/home/user/app/orchestrate.ipynb` is ready to be executed via papermill.