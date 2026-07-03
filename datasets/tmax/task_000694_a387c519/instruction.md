You are acting as a localization engineer. We are analyzing the daily view counts for a specific UI string in our application, but the exact string identifier has been lost in our tracking system. The only reference we have is a mockup image of the UI element.

Your task:
1. Extract the UI string identifier from the image located at `/app/reference_ui.png`. You may use `tesseract` which is pre-installed. Note that OCR might include trailing whitespace or newlines; you must clean the extracted text to get the exact string identifier (it will be an uppercase string with underscores).
2. We have a time-series log of localization events in `/app/loc_events.csv`. The format is `timestamp,ui_string,locale,views`. The timestamp is in Unix epoch seconds.
3. Write a C++ program that reads `/app/loc_events.csv`. The program should filter the dataset for the UI string identifier you extracted.
4. For this specific UI string, aggregate the total `views` grouped by the UTC Date in `YYYY-MM-DD` format.
5. Bring up an HTTP service listening on `127.0.0.1:8080`. You can write the server in C++ (using basic sockets) or process the data in C++, save it to a file, and serve it using another tool (e.g., Python or a simple web server).
6. When your server receives an HTTP GET request to `/metrics`, it must respond with a JSON object where the keys are the dates (e.g., `"2023-10-01"`) and the values are the aggregated integer view counts. No other endpoints need to be supported.

Requirements:
- The core data transformation (parsing, filtering, date conversion, and aggregation) MUST be implemented in C++.
- Ensure your service stays running in the background so the automated verifier can query it.