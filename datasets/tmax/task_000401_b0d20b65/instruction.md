You are tasked with building an automated project file organization service for our legacy codebases. A previous engineer left an image containing the architectural specifications for this service at `/app/spec.png`.

Your objectives are as follows:

1. **Extract Specifications**: Read the image `/app/spec.png` to understand the REST API endpoint requirements and the mathematical formula for the "Modularity Score".
2. **Implement the API**: Create a Python script at `/home/user/organizer_api.py` that runs a REST API on port `8000`. It must expose the endpoints and accept the payload described in the specification image.
3. **Implement the Organization Algorithm**: The API must analyze a target directory containing Python files. Dependencies are defined by simple `import <filename_without_extension>` statements found inside the files. Your algorithm must partition the files into modules such that the "Modularity Score" is maximized, while respecting the constraint that no module can contain more than 3 files.
4. **Create Test Fixtures**: Write a test script at `/home/user/test_api.py` that sets up a mock directory structure with at least 5 files and specific dependency imports, starts the API (or mocks the app), makes a request to the endpoint, and asserts that the response format is correct and the Modularity Score is calculated correctly.

The primary codebase to test your live API on is located at `/home/user/legacy_project/`. However, your API should be generic enough to accept any directory path provided in the REST payload. 

Leave the API running in the background on port `8000` when you are finished, or ensure it can be started simply by running `python3 /home/user/organizer_api.py`.