You are tasked with building a data processing pipeline that normalizes Unicode mathematical datasets, incorporates a transformation extracted from an audio file, and serves the results via a local API.

You have been provided with two input files:
1. `/app/instruction.wav`: An audio file containing a spoken instruction in English. This instruction specifies a final mathematical operation (e.g., "multiply by five" or "add one hundred") that must be applied to all your computed results.
2. `/app/math_data.csv`: A CSV file with two columns: `id` and `expression`. The `expression` column contains simple mathematical operations (`+`, `-`, `*`, `/`), but the numbers are represented using various Unicode characters (e.g., full-width digits like `５`, fractions like `½`, circled numbers like `⑧`, or Roman numerals like `Ⅳ`).

Your objective is to:
1. **Transcribe the Audio**: Programmatically transcribe `/app/instruction.wav` to extract the hidden mathematical operation.
2. **Process the Text**: Read `/app/math_data.csv`. For each row, parse the Unicode characters into standard numeric values (you can use Python's `unicodedata` module) and evaluate the mathematical expression.
3. **Apply the Transformation**: Apply the mathematical operation extracted from the audio file to the result of each evaluated expression.
4. **Log the Pipeline**: Create a log file at `/app/pipeline.log` that logs the progression of your pipeline. It must include the transcribed audio text, the number of records processed, and any errors encountered during parsing. Use a standard logging format (e.g., `YYYY-MM-DD HH:MM:SS - LEVEL - Message`).
5. **Serve the Data**: Start an HTTP server listening on `0.0.0.0:8000`. 
   - It must have an endpoint `GET /result/{id}`.
   - The endpoint must return a JSON response in the exact format: `{"id": <id_as_int>, "result": <final_computed_value_as_float>}`.
   - Return a 404 status code if the `id` does not exist.

You must write a Python script (or multiple scripts) to execute this entire pipeline and launch the API server. You may install any necessary open-source libraries (e.g., `openai-whisper`, `fastapi`, `uvicorn`, `pandas`) using `pip`. Leave the server running in the foreground or background so it can be tested.