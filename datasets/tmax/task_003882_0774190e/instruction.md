You are acting as a Localization Engineer. We are migrating our translation pipeline and need to set up an automated validation and serving system. 

You are provided with two inputs:
1. `/app/ui_spec.png`: A screenshot of our UI design specifications. You must extract the text from this image (using OCR, `tesseract` is installed) to find two strict translation constraints. It will contain a maximum length constraint and a required placeholder variable constraint.
2. `/app/raw_locales.bin`: A legacy translation data dump. It contains key-value pairs separated by an equals sign (`=`), one per line. However, this file is encoded in `Windows-1252` (CP1252), NOT UTF-8.

Your task is to write a Rust application that implements the following orchestration pipeline:
1. **Extraction:** Read the constraints from the UI spec image.
2. **Decoding:** Read and decode the legacy translation file into proper UTF-8.
3. **Quality Gate:** Filter the translations. A translation is only valid if its value (the right side of the `=`) meets BOTH constraints extracted from the image (length is less than or equal to the max length, AND it contains the exact required placeholder token).
4. **Serving:** Bring up an HTTP server listening on `127.0.0.1:8080`. 

The HTTP server must behave as follows:
- Listen for `GET` requests on `/api/v1/translations`.
- Require an `Authorization` header with the exact value: `Bearer loc-agent-2024`. If missing or incorrect, return a `401 Unauthorized`.
- On a valid request, return a `200 OK` response with a JSON body representing the validated translations. The JSON must be an object with a `"translations"` key containing an object of valid key-value pairs. For example: `{"translations": {"welcome": "Hello {name}!"}}`.

You may create your Rust project in `/home/user/loc_pipeline`. You can use external crates (like `axum`, `tokio`, `encoding_rs`, etc.) to accomplish this. Keep the server running in the background or foreground once it's ready, so our automated tests can query it.