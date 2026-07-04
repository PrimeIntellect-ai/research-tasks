You are an operations engineer triaging a critical incident. Our legacy C++ Pricing Service recently started timing out and failing to converge on certain inputs. The previous engineer left a screenshot of the last known good configuration on the server before their access was revoked. 

Your task is to restore the service, fix the underlying mathematical bugs, and deploy the fixed server locally.

**Step 1: Recover Configuration**
There is an image file located at `/app/error_snapshot.png`. It contains a screenshot of a terminal showing the required `EPSILON` and `MAX_ITERATIONS` parameters for the iterative pricing algorithm. You must use OCR (e.g., `tesseract`) to extract these values.

**Step 2: Fix the Pricing Algorithm**
Create a directory `/home/user/pricing_service/`. Write the following buggy C++ HTTP server code to `/home/user/pricing_service/server.cpp`. 

```cpp
#include "httplib.h"
#include <iostream>
#include <cmath>
#include <string>

// TODO: Update these with values from the image
const float EPSILON = 0.001f; 
const int MAX_ITERATIONS = 50;

// Buggy Newton-Raphson square root calculation (simulating our pricing model)
float calculate_pricing_model(float S) {
    if (S <= 0.0f) return 0.0f;
    float x = S;
    float prev_x = 0.0f;
    int iter = 0;
    
    // Fails to converge due to precision issues for certain inputs!
    while (std::abs(x - prev_x) >= EPSILON && iter < MAX_ITERATIONS) {
        prev_x = x;
        x = 0.5f * (x + S / x);
        iter++;
    }
    return x;
}

int main() {
    httplib::Server svr;

    svr.Get("/price", [](const httplib::Request& req, httplib::Response& res) {
        if (req.has_param("s")) {
            float s = std::stof(req.get_param_value("s"));
            float result = calculate_pricing_model(s);
            res.set_content(std::to_string(result), "text/plain");
        } else {
            res.status = 400;
            res.set_content("Missing parameter 's'", "text/plain");
        }
    });

    std::cout << "Starting server on port 8080" << std::endl;
    svr.listen("127.0.0.1", 8080);
    return 0;
}
```

**Requirements:**
1. Download `cpp-httplib` (header-only) to the project directory: `wget https://raw.githubusercontent.com/yhirose/cpp-httplib/master/httplib.h`
2. Analyze the floating-point precision and convergence failure repair. The current code uses `float`, which lacks the precision to satisfy the `EPSILON` value from the image, leading to early termination or incorrect diffs in our data transformation pipeline. Upgrade the logic to use double-precision floating-point types (`double`).
3. Update the `EPSILON` and `MAX_ITERATIONS` constants with the exact values you extracted from the image.
4. Compile the server (e.g., `g++ -O2 server.cpp -o server -lpthread`).
5. Run the server in the background so it listens on `127.0.0.1:8080`. The server must remain running for the verification step.

Ensure the server returns high-precision double string representations when the `/price` endpoint is hit.