You are a machine learning engineer tasked with preparing a synthetic data generation service for our training pipeline. We need a service that generates samples from a specific Gaussian Mixture Model (GMM), tests the generated distribution against a regression baseline, and serves the data over an HTTP API.

Here are the requirements:

1. **Extract Target Distribution:**
   You have been provided with an image file at `/app/distribution_spec.png`. This image contains the parameters of the 2-component Gaussian Mixture Model we need to sample from (Weights, Means, and Standard Deviations). Extract these parameters. 

2. **C-based Sampler and Regression Tester:**
   Write a C program (`/home/user/gmm_sampler.c`) that:
   - Takes the number of samples `n` to generate as a command-line argument.
   - Generates `n` independent samples from the target GMM specified in the image. (You may use standard approaches like the Box-Muller transform).
   - Reads the regression baseline dataset from `/app/baseline_samples.txt` (a plain text file containing one float per line).
   - Calculates the Kolmogorov-Smirnov (KS) distance statistic between your newly generated `n` samples and the baseline dataset. This serves as our statistical regression test.
   - Outputs the KS statistic and the generated samples to standard output so a wrapper can parse it.

3. **API Service:**
   Create an HTTP web service listening on exactly `127.0.0.1:8000`. You may write the server in Python (e.g., using Flask or FastAPI) that compiles and calls your C program.
   - The server must expose a `GET /generate` endpoint.
   - It should accept a query parameter `n` indicating the number of samples to generate.
   - It must require an Authorization header with a Bearer token: `Authorization: Bearer ML-DATA-2024`. If the token is missing or invalid, return a 401 status code.
   - On a valid request, it should invoke your C program, parse the output, and return a JSON response in the following format:
     ```json
     {
       "ks_distance": <float>,
       "samples": [<float>, <float>, ...]
     }
     ```

Leave the server running in the background. The automated verification system will test the server's endpoint, authentication, and the statistical validity of the generated data.