You are assisting a data researcher in organizing and scoring datasets using a probabilistic Bayesian model. 

The researcher has an existing Go service used to score datasets and run inference performance benchmarks. The source code for this service is vendored at `/app/dataset-catalog`. However, the service currently has a mathematical bug causing its numerical accuracy tests to fail, and the researcher needs you to fix it and bring the service online.

Your tasks:
1. Copy the vendored package from `/app/dataset-catalog` to `/home/user/dataset-catalog` and work from there.
2. In the Go code (specifically in the scoring logic), there is a bug in the calculation of the Bayesian posterior probability. Find and fix the mathematical error so that the posterior is correctly calculated as `(Prior * Likelihood) / Marginal`.
3. Verify your fix by running the unit tests and inference benchmarks included in the package (`go test -bench . ./...`). All tests must pass.
4. Build the Go application and run it as a background service. 
5. The service must listen for HTTP requests on `127.0.0.1:9090`. (You may need to inspect the code to see how to configure the port).

The automated verifier will act as an HTTP client and issue real protocol-level HTTP GET requests to the service on `127.0.0.1:9090`. Specifically, it will call the `/score` endpoint with query parameters `prior`, `likelihood`, and `marginal` to verify the numerical accuracy of the Bayesian inference engine directly over the network.

Do not stop the service once it is running; leave it listening on port 9090 so the verifier can test it.