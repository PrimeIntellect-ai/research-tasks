I'm a researcher running orbital mechanics simulations. We have a multi-service simulation backend that calculates the trajectory of a spacecraft using an adaptive step-size Runge-Kutta-Fehlberg (RKF45) integrator. Unfortunately, our Python implementation of the integrator is diverging from the analytical solution due to incorrect step-size adaptation logic, causing downstream analysis in our Jupyter notebooks to fail.

We have a reference C implementation of the integrator that is known to be correct and matches analytical solutions perfectly. 

Your task is to:
1. Compile the reference C oracle located at `/app/oracle/integrator.c` into a binary at `/app/oracle/integrator`.
2. Fix the Python integration service located at `/app/flask_service/integrator.py`. The logic for the step-size error calculation and adaptation (the `calculate_error` and `adapt_step` functions) is flawed. You must correct it so that its outputs match the C oracle exactly (bit-exact float comparisons up to 6 decimal places formatted as strings in the JSON response).
3. Configure and start our multi-service stack:
   - A Redis server for caching simulation results (port 6379).
   - A Flask API running the Python integrator (port 5000).
   - An Nginx reverse proxy serving the Flask API (port 8080).
   You will find the configuration files and a startup script `start_services.sh` in `/app/services/`. You need to ensure Nginx correctly routes `/simulate` to the Flask app, and Flask correctly connects to Redis.
4. Once the services are running, execute the validation notebook `/home/user/validation/check_analytical.ipynb` and ensure all assertions pass. The notebook queries the Nginx endpoint on port 8080. Save the executed notebook to `/home/user/validation/check_analytical_executed.ipynb`.

The Flask API endpoint `/simulate` accepts a POST request with JSON payload: `{"t0": float, "tf": float, "y0": [float, float], "tol": float}` and returns `{"t": [float, ...], "y": [[float, float], ...]}`.

Please make the necessary fixes, configure the services, and leave the services running.