You are a support engineer investigating an urgent customer escalation. We received a bug report from a major client regarding our C-based timezone conversion microservice. The customer sent us a screenshot of their internal ticketing system containing the specific failing datetime string and the port configuration they expect for the fixed service. This screenshot is located at `/app/bug_ticket.png`.

Here is your workflow:
1. Extract the text from `/app/bug_ticket.png` using OCR (e.g., `tesseract`) to determine the exact failing datetime string, the expected UTC output, and the port number the service must run on.
2. Navigate to the local Git repository of the microservice at `/app/timeserver_repo`. 
3. The service compiles to an executable named `timeserver`. We know the service worked perfectly in the `v1.0` tag, but the current `master` branch is failing or crashing on the input specified in the image.
4. Use `git bisect` to identify the exact commit that introduced the regression. 
5. You may notice that one of the intermediate commits has a build failure (e.g., a missing header or syntax error). Diagnose and fix the build or skip the commit to continue your bisection.
6. Once the root cause is identified, fix the C code. The bug involves improper bounds checking or timezone offset calculation when handling the specific string from the bug ticket. Use system call tracing (`strace`) or write a quick assertion-based test/fuzzer if you need to isolate the crash locally.
7. Compile the fixed `timeserver` using the provided `Makefile`.
8. Start the microservice and bind it to `127.0.0.1` on the port specified in the `bug_ticket.png`. It must stay running in the background.

The server operates over HTTP. The endpoint is `GET /convert?datetime=<url_encoded_datetime>`. It should return a `200 OK` response with a plain text body of the converted Unix epoch timestamp. 

Fix the code, launch the fixed server on the correct port, and ensure it correctly handles the edge case from the image ticket.