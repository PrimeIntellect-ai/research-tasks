You are a build engineer managing the CI/CD pipeline for a Python web application. 

The security team has added a test suite to ensure our URL routing logic securely parses parameters and prioritizes protected endpoints over wildcards. The tests pass on local developer machines but are failing in the CI environment. 

The problem has been traced to `/home/user/app/mock_loader.py`. This file loads URL routing test fixtures from `/home/user/app/fixtures/`. Because `os.listdir()` returns files in an arbitrary, filesystem-dependent order, the catch-all routing configurations (e.g., `99_catchall.json`) are sometimes loaded before the secure routing configurations (e.g., `10_secure.json`) in the CI runner. This causes the test fixtures to be injected in the wrong order, causing the security test to fail.

Your task:
1. Modify `/home/user/app/mock_loader.py` to ensure that the files retrieved from the fixtures directory are always processed in alphabetical order.
2. Run the CI pipeline script at `/home/user/app/ci_pipeline.sh`.
3. If your fix is correct, the tests will pass and the CI script will automatically generate a success log at `/home/user/build_success.log`.

Do not modify the test assertions or the fixture files themselves. You only need to fix the import ordering bug in the mock loader.