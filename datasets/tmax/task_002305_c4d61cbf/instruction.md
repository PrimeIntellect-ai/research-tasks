You are a data analyst setting up an automated transaction validation pipeline. You need to fix a local multi-service environment and write a Bash script to process incoming CSV data.

System Overview:
We have a local environment with two cooperating services located in `/app/`:
1. A Redis server storing user transaction limits.
2. A Flask API (`/app/api.py`) that serves user risk scores. 

Currently, the services are not working together correctly. A startup script `/app/start.sh` is supposed to launch both. However, the Flask API is failing to start because its configuration file `/app/.env` is missing the correct Redis URL, and it is currently configured to bind to port 5005 instead of the required port 5000. 

Your tasks:
1. Reconfigure the services:
   - Fix `/app/.env` so that `REDIS_URL` points to `redis://127.0.0.1:6379/0` and `PORT` is set to `5000`.
   - Ensure that when you run `/app/start.sh`, both Redis and the Flask API start correctly and the API is accessible at `http://127.0.0.1:5000`.
   
2. Write a data processing script:
   - Create an executable Bash script at `/home/user/process.sh`.
   - The script must read exactly ONE line of CSV data from **standard input**. The format of the input is: `tx_id,user_id,amount,timestamp` (e.g., `tx_1001,user_3,250.50,1633024800`).
   - For the given `user_id`, the script must query the Flask API at `http://127.0.0.1:5000/api/users/<user_id>` which will return a JSON response containing `{"risk_score": <float>}`.
   - For the given `user_id`, the script must query the local Redis server for the key `limit:<user_id>` to get the user's transaction limit (an integer or float).
   - The script must calculate the `risk_adjusted_amount = amount * risk_score`.
   - If the `risk_adjusted_amount` is strictly greater than the user's limit, the script should output `<tx_id>,REJECT` to standard output. Otherwise, it should output `<tx_id>,APPROVE`.
   
Constraints:
- You may use standard command-line tools like `curl`, `jq`, `redis-cli`, `awk`, or `bc`.
- Do not print any extra text, logging, or empty lines to standard output in `/home/user/process.sh` other than the final result.
- Handle floating point arithmetic correctly.

Ensure your script is robust and exactly matches the output format.