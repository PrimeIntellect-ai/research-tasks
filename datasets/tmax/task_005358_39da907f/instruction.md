As an automation specialist, I need you to build a robust data processing pipeline component. We receive continuous telemetry data in JSON-lines format, but the system generating this data has a bug: it improperly escapes unicode characters in the keys and sometimes breaks JSON formatting by leaving raw unicode escape sequences (like `\u0041`) in string values without proper quoting. 

Additionally, we need to apply a mathematical transformation to the numerical coordinates found in the telemetry. The specific 2x2 transformation matrix you need to apply is documented in an image file located at `/app/transformation_matrix.png`. 

Your task is to write a Python script at `/home/user/process_telemetry.py` that acts as a stream processor (reading from `stdin` and writing to `stdout`).

The script must:
1. Read the image at `/app/transformation_matrix.png` (using OCR/tesseract or similar) to extract the four integer values of the 2x2 matrix: [[a, b], [c, d]].
2. Process `stdin` line by line (JSON-lines).
3. Use regex to clean up broken unicode escape sequences in the raw string before parsing it as JSON. Specifically, find any sequence like `\uXXXX` and ensure it is properly decoded to its corresponding character.
4. Extract the `x` and `y` values from the `coordinates` object in the JSON.
5. Multiply the vector `[x, y]` by the extracted 2x2 matrix to get new `[x', y']` values.
6. Write a valid JSON-line to `stdout` containing `{"original_x": x, "original_y": y, "transformed_x": x', "transformed_y": y'}`.
7. Implement validation checkpoints: if a line cannot be parsed or lacks `coordinates`, silently drop it. 

The script must be executable from the command line and will be rigorously tested against a reference implementation with thousands of randomized inputs.