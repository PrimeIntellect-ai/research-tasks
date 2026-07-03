You are an AI assistant helping a researcher organize their legacy dataset metadata. 

The researcher has an undocumented SQLite database located at `/app/datasets.db`. They want you to extract specific analytical insights from this database and serve them via a secure local HTTP API.

Unfortunately, the researcher forgot the API configuration they used to use, but they left a scan of a sticky note at `/app/sticky_note.png`. You will need to extract the required server `PORT` and the `TOKEN` from this image.

Your tasks are:
1. **Analyze the Image**: Use OCR (e.g., `tesseract` which is pre-installed) to read `/app/sticky_note.png`. Extract the port number and the authorization token.
2. **Reverse Engineer the Database**: Inspect `/app/datasets.db`. It contains three tables related to authors, dataset collections, and recorded metrics. You must figure out the schema and how the tables relate.
3. **Data Aggregation**: Write a SQL query using window functions to find the top 2 `metric_value`s (highest values) for each dataset collection. 
4. **Build the API**: Create a Python HTTP API (using Flask, FastAPI, or standard library) that listens on `0.0.0.0` at the port specified in the sticky note.
5. **Serve the Endpoint**: Implement a `GET` endpoint at `/api/v1/datasets/stats`.
   - The endpoint MUST require an `Authorization: Bearer <TOKEN>` header using the token found in the image. Return HTTP 401 if the token is missing or invalid.
   - The endpoint must return a JSON response with the following schema:
     ```json
     {
       "results": [
         {
           "dataset_name": "string",
           "author_name": "string",
           "top_metrics": [float, float] 
         }
       ]
     }
     ```
   - Sort the `results` array alphabetically by `dataset_name` ascending. If a dataset has fewer than 2 metrics, include however many exist. If it has no metrics, omit it or return an empty array for `top_metrics`.

Keep your API running in the background or foreground so it can be tested. You can install any necessary Python packages (e.g., `flask`, `fastapi`, `uvicorn`, `pytesseract`, `Pillow`) via `pip`.