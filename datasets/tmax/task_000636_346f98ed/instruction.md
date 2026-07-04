You are acting as a QA Engineer tasked with setting up a robust test environment and verification parser for our legacy OCR pipeline. We have been experiencing issues where our system is fed malicious or malformed OCR outputs, leading to downstream processing failures. 

Your objectives:
1. **Initial Environment & Fixture Setup**: Set up a Python virtual environment at `/home/user/venv`, and install `pytesseract`, `Pillow`, and `pytest`. 
2. **Image Baseline Recovery**: We have provided a baseline system blueprint image at `/app/system_blueprint.png`. Write a script to extract the embedded environment ID from this image using `tesseract`.
3. **Adversarial Log Sanitizer**: Implement a Python module at `/home/user/sanitizer.py` with a state-machine based parser. It must contain the function `def sanitize_log(content: str) -> bool:`. This function should return `True` if the log is clean, and `False` if it contains malformed sequences or injection attempts.
4. **Verification**: I have placed a set of test corpora under `/app/corpus/clean/` and `/app/corpus/evil/`. Every file in the `clean` directory must evaluate to `True`, and every file in the `evil` directory must evaluate to `False`. 
5. **Test Harness**: Write a `pytest` suite at `/home/user/test_sanitizer.py` that iterates through both directories and asserts the correct behavior for `sanitize_log`. Additionally, your test suite must mock the OCR reading step to return the environment ID extracted from `/app/system_blueprint.png`.
6. **Execution**: Run your tests and save the standard output to `/home/user/test_report.log`.

Make sure your code strictly conforms to the function signature requested.