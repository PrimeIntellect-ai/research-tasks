I've recently inherited a legacy data-processing service from a former developer. It was originally running inside a container, but the container keeps crashing. I inspected the container logs and saw repeated `RecursionError: maximum recursion depth exceeded` followed by a complete crash of the service. 

I've extracted the application code and the input dataset to my home directory at `/home/user/legacy_app/`.

The application, `app.py`, is supposed to read a series of coordinate updates from `data.txt` and recursively calculate a steady-state equilibrium point for each line. However, it seems like the recursive loop never terminates properly for certain inputs. I suspect there is an issue with how the termination condition is evaluated, likely related to how Python handles floating-point arithmetic.

Your task is to:
1. Debug and fix the `/home/user/legacy_app/app.py` script so that it properly terminates the recursion without crashing. You must resolve the floating-point precision issue that is causing the recursion to miss its target and run endlessly. Use a tolerance of `1e-5` for any floating-point comparisons to determine equality.
2. Run the fixed script against `/home/user/legacy_app/data.txt`.
3. Save the final calculated outputs to `/home/user/legacy_app/output.txt`.

The `output.txt` file should contain exactly one floating-point number per line, corresponding to the final equilibrium value calculated for each line in `data.txt`. Format the output values to one decimal place (e.g., `1.0`).

Do not change the recursive nature of the function, only fix the termination condition.