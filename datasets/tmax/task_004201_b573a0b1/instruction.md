You are a developer tasked with organizing project files by migrating a legacy Go-based file sorting tool to Python, writing proper mock-based tests, and creating a unified build/run wrapper.

Currently, we have a Go program located at `/home/user/legacy/sorter.go`. This program uses a concurrency pattern (a worker pool using goroutines and channels) to process files in a directory. It categorizes files by moving `.txt` files to a `text/` subdirectory, `.log` files to a `logs/` subdirectory, and deleting `.tmp` files.

Your task has three parts:

1. **Code Translation (Python)**
Create `/home/user/sorter.py`. Translate the Go logic into Python. To maintain the exact same concurrent architecture, you MUST use Python's `threading.Thread` and `queue.Queue` to mimic the goroutines and channels. The Python script should accept a target directory as a command-line argument, spawn 3 worker threads, and feed the file paths within that directory into the queue for the workers to process. The workers should perform the file moves (`shutil.move`) and deletions (`os.remove`).

2. **Test Fixtures and Mocks**
Create a test file at `/home/user/test_sorter.py` using the standard `unittest` framework. Write a test suite that:
- Uses `@patch` to mock `shutil.move`, `os.remove`, and `os.listdir`.
- Sets up a fixture simulating a directory containing `a.txt`, `b.log`, and `c.tmp`.
- Tests that the worker functions process the queue and call the correct mocked file operations with the correct paths, without altering the real filesystem.
- When the tests run and pass, the script must append the exact string `TESTS_PASSED_SUCCESSFULLY` to `/home/user/test_status.log`.

3. **Conditional Build & Execution Wrapper**
Create a bash script at `/home/user/organize.sh`. This script will act as a unified entry point that uses environment variables to decide which implementation to run on the target directory (passed as `$1`).
- Check the environment variable `USE_LANG`.
- If `USE_LANG=go`: The script must cross-compile the Go code for Linux using the architecture specified in the `TARGET_ARCH` environment variable (defaulting to `amd64` if not set). Compile it to `/home/user/bin/sorter_bin` and then execute it against the directory.
- If `USE_LANG=python`: The script must simply execute `/home/user/sorter.py` against the directory.

Make sure `/home/user/organize.sh` is executable. You can test your implementation against the messy files located in `/home/user/data/raw_files`.