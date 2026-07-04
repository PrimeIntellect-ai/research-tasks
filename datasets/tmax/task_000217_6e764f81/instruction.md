You are acting as a data scientist responsible for fitting nonlinear models to data streamed from our internal sensor telemetry service. 

We have a multi-service setup in `/app/`. It consists of a Flask API (`sensor_api`) that reads and caches data using Redis. 

Currently, the services are not starting correctly because the configuration is broken. 
1. Fix the configuration in `/app/start_services.sh` so that the Flask API can successfully connect to the Redis service. The Flask API runs on port 8080 and expects a specific environment variable for the Redis connection string.
2. Start the services.
3. Once running, fetch the observation data from `http://127.0.0.1:8080/data`. The endpoint returns a JSON object with two arrays: `x` and `y`.
4. The data represents a nonlinear physical process modeled by the equation:
   `y = a * exp(b * x) + c * sin(d * x)`
   Write a Python script `/home/user/fit_model.py` to fit this equation to the data and determine the optimal parameters `a`, `b`, `c`, and `d`. You should use techniques like nonlinear least squares to ensure numerical stability.
5. Save the final fitted parameters in a JSON file at `/home/user/model_params.json` with the keys `"a"`, `"b"`, `"c"`, and `"d"`.

Ensure your model accurately captures the underlying signal, as your parameters will be tested against a high-resolution refined mesh validation set.