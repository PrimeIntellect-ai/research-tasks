As a script developer, we are dealing with a Python project whose test suite passes locally but fails in CI due to unpredictable import ordering. To fix this, we are routing module imports through a custom CI proxy emulator. 

Unfortunately, the original documentation for the proxy router is lost, but we managed to find a screenshot of the routing rules at `/app/import_router.png`. 

Your task is to:
1. Extract the text/rules from the image `/app/import_router.png` (using OCR tools like `tesseract` which are available).
2. Implement the exact URL routing and custom checksum logic described in the image.
3. Write an executable Python script at `/home/user/route.py` that accepts a single command-line argument representing the input URL path.
4. The script must output ONLY the correctly calculated reverse proxy URL to `stdout`.
5. If the input does not perfectly match the expected input format (described in the image), the script must output exactly the word `INVALID`.

Ensure your script is executable (`chmod +x /home/user/route.py`) and perfectly matches the logic in the image so it can flawlessly emulate the legacy router.