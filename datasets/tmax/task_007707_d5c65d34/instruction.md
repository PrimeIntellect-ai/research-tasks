You are an open-source maintainer reviewing a broken pull request for a Go-based mathematics API. A contributor has submitted a patch file for a new feature, but their PR branch had failing tests and dependency issues, and the contributor has gone unresponsive. Your goal is to apply their patch, fix the dependency and algorithmic issues, make all tests pass, and verify the API endpoint works correctly.

Here is the situation:
- The base repository is located at `/home/user/math-api`. It is a simple Go module.
- The contributor's patch is located at `/home/user/pr-123.patch`.
- The patch adds a new `POST /variance` REST API endpoint that accepts a JSON payload containing an array of floats and returns the **population variance** of those numbers.
- The patch also adds tests and updates `main.go` to use the `github.com/go-chi/chi/v5` router.

Your tasks are:
1. Apply the patch `/home/user/pr-123.patch` to the `/home/user/math-api` repository.
2. The patch introduces a new dependency but the contributor forgot to update `go.mod`. Fix the package dependencies so the project can build.
3. Run the tests. You will notice that `stats_test.go` fails. The contributor made a mistake in the numerical algorithm in `stats.go`. They implemented *sample variance* (dividing by N-1) instead of the required *population variance* (dividing by N). Fix the mathematical bug in `stats.go` so that `go test ./...` passes.
4. Build the API server and start it in the background. It should listen on port `8080`.
5. Write a bash script at `/home/user/verify.sh` that uses `curl` to send a `POST` request to `http://localhost:8080/variance` with the following JSON payload:
   `{"numbers": [10.5, 20.0, 30.5, 40.0]}`
6. The response from the API must be saved to `/home/user/api_output.json` by the bash script.

Requirements:
- Ensure the API response saved in `/home/user/api_output.json` strictly matches the format: `{"variance":<value>}`.
- Make sure `/home/user/verify.sh` is executable and run it at least once to generate the output file.