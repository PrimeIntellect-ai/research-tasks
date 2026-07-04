You are a mobile build engineer maintaining a continuous integration (CI) pipeline. Our automated UI tests produce a video recording of the device screen during the test run. Recently, a bug has caused the CI dashboard service to crash and report incorrect build stability scores.

Your task has three parts:

1. **Video Analysis**:
   There is a video artifact from a recent failed build located at `/app/ci_test_run.mp4`. During a "crash" event, the mobile app screen flashes entirely RED (where the red channel is near maximum, and green/blue are near zero). 
   Use `ffmpeg` (which is preinstalled) and any scripting language of your choice to analyze the video and count the exact number of completely red frames. Let this count be `N`.

2. **C Server Repair**:
   In your home directory (`/home/user/dashboard/`), there is a C-based HTTP service (`server.c`) that calculates build stability constraints.
   It has several severe issues:
   - **Memory Safety**: The HTTP request parser has a buffer overflow vulnerability that crashes the server when it receives large headers. There is also a memory leak in the request handler.
   - **Numerical Algorithm (Constraint Satisfaction)**: The function `int calculate_optimal_score(int capacity, int weights[], int values[], int n)` is intended to solve the 0/1 Knapsack problem to determine the optimal subset of test modules to run within a time `capacity`. The current implementation is a flawed greedy algorithm. Rewrite this function to correctly compute the maximum possible value using dynamic programming.

3. **API Integration**:
   Modify the C server so that it securely listens on `127.0.0.1:8080`.
   It must implement the following endpoints:
   - `GET /health`: Returns `{"status": "ok"}`
   - `POST /score`: Accepts a request. The request must include the header `Authorization: Bearer mobile_ci_secret`. 
     It should parse a JSON payload `{"crash_count": <count>}` (where `<count>` is the number of red frames you found).
     When invoked, it should compute the optimal score using the hardcoded test modules in `server.c`, multiply that optimal score by the `crash_count`, and return the JSON response: `{"final_score": <calculated_integer>}`.

**Instructions**:
- Fix `server.c` and compile it (a `Makefile` is provided, or you can use `gcc`).
- Start the server as a background process so it is actively listening on `127.0.0.1:8080`.
- Leave the server running when you finish the task.
- Ensure the server does not crash if it receives an HTTP request with an unusually long URL or headers.