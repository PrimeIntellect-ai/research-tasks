I need you to fix and complete a C++ data processing utility designed to validate, rate-limit, and route incoming HTTP-like requests. 

I started writing this multi-file C++ project located in `/home/user/router_utility/`, but it crashes with segmentation faults (I suspect some dangling pointers or bad `std::string_view` usage similar to lifetime issues) when parsing URL parameters.

Here is what you need to do:
1. **Extract Routing Rules**: There is an image file at `/app/routing_spec.png` containing the specifications for our API endpoints, expected parameters, and their specific rate limits. Use OCR (like `tesseract`, which is installed) to extract these rules.
2. **Fix the C++ Skeleton**: Inspect the code in `/home/user/router_utility/`. Fix the memory management and string parsing issues in `url_parser.cpp` and `router.cpp`.
3. **Implement Validation & Rate Limiting**: Complete the `validate_request` function. It must:
   - Parse the URL routing and extract parameters.
   - Enforce the rate limits extracted from the image. (Requests are processed chronologically based on their provided timestamp).
   - Reject any request containing path traversal sequences (`../`) or invalid characters in the parameters.
4. **Compile**: Use the provided `CMakeLists.txt` to build the utility. The executable should be output to `/home/user/router_utility/build/request_validator`.
5. **Verify against the Corpus**: There is a dataset of pre-parsed request JSON files provided.
   - `/app/corpus/clean/`: These requests are perfectly valid and within rate limits. Your utility must output `ACCEPT` for all of these.
   - `/app/corpus/evil/`: These requests contain path traversals, malformed parameters, or violate the rate limit specifications in the image. Your utility must output `REJECT` for all of these.

The C++ utility takes a directory of JSON requests as an argument and outputs a CSV log. You must run your fixed utility on both directories and save the results:
```bash
/home/user/router_utility/build/request_validator /app/corpus/clean/ > /home/user/clean_results.csv
/home/user/router_utility/build/request_validator /app/corpus/evil/ > /home/user/evil_results.csv
```

A test suite will run your compiled executable against a hidden evaluation corpus as well, so ensure your logic strictly follows the extracted rules and handles state cleanly.