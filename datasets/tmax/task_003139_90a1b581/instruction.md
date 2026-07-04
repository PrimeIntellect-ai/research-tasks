You are acting as a FinOps analyst tasked with optimizing cloud transit costs. The infrastructure team has lost the raw text configuration for our cross-region network routing costs, leaving us with only a screenshot of the architecture diagram. 

Your task is to extract this pricing data and expose it via a local API for our automated cost-routing health checks.

Here are your instructions:

1. **Extract Pricing Data:** 
   We have an architecture diagram located at `/app/transit_costs.png`. Use OCR (Tesseract is pre-installed) to read the text from this image. 
   The text contains routing costs formatted roughly like: `Region: <region_name>, Cost: $<value>/GB`.

2. **Process and Store Data:**
   Parse the OCR output to extract the exact region names and their corresponding numeric cost values. Write a robust script or text processing pipeline to handle this data cleanly.

3. **Develop a Cost API:**
   Write and start a web service (using a language of your choice) that serves the parsed data.
   - The service MUST listen on `127.0.0.1:8080`.
   - The service must run continuously in the background.

4. **API Endpoints & Routing Configuration:**
   Implement the following HTTP endpoints:
   - `GET /health`: 
     Returns an HTTP 200 status code and exactly the plaintext response `OK`. This simulates our basic health check and monitoring setup.
   - `GET /cost?region=<region_name>`: 
     Must act as our simulated cost lookup.
     - **Authentication**: This endpoint must require an `Authorization` header with the bearer token `FINOPS_SECRET_99X`. If the header is missing or incorrect, return an HTTP 401 Unauthorized status.
     - **Success**: If the region exists in the extracted data, return an HTTP 200 status and the numeric cost value (e.g., `0.05`) in plaintext.
     - **Not Found**: If the region does not exist, return an HTTP 404 Not Found status.

Ensure your service is fully running and accessible locally before completing the task.