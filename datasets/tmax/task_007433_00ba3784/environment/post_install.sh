apt-get update && apt-get install -y python3 python3-pip git
pip3 install pytest

mkdir -p /home/user/service
cd /home/user/service
git init
git config --global user.email "devops@example.com"
git config --global user.name "DevOps"

cat << 'EOF' > requirements.txt
asyncio
EOF

cat << 'EOF' > server.py
import asyncio

async def long_running_job():
    try:
        await asyncio.sleep(10)
    except asyncio.CancelledError:
        pass

async def handle_request(request_data):
    # Simulate processing
    await long_running_job()
    return "OK"
EOF

git add .
git commit -m "Initial commit: basic server"
GOOD_COMMIT=$(git rev-parse HEAD)

# Add a dummy feature
echo "# dummy feature" >> server.py
git commit -am "Add dummy feature"

# Introduce the bug
cat << 'EOF' > server.py
import asyncio

async def long_running_job():
    try:
        await asyncio.sleep(10)
    except asyncio.CancelledError:
        pass

async def handle_request(request_data):
    # Bug: Creating a task but not cancelling it when the handler is cancelled
    task = asyncio.create_task(long_running_job())
    await asyncio.sleep(0.1)
    await task
    return "OK"
EOF
git commit -am "Refactor request handler"
BAD_COMMIT=$(git rev-parse HEAD)

# Add another feature
echo "# another feature" >> server.py
git commit -am "Add another feature"

# Introduce misconfiguration (missing dependency in requirements)
cat << 'EOF' > requirements.txt
asyncio
nonexistent_pkg_12345
EOF
git commit -am "Update dependencies"

# Create the test script
cat << 'EOF' > /home/user/test_leak.py
import asyncio
import sys
import os

# Ensure the service directory is in path to import server
sys.path.insert(0, '/home/user/service')

try:
    import server
except ImportError as e:
    print(f"Import Error: {e}")
    sys.exit(2)

async def test_leak():
    initial_tasks = len(asyncio.all_tasks())

    # Simulate a request that gets cancelled
    task = asyncio.create_task(server.handle_request("data"))
    await asyncio.sleep(0.01) # let it start
    task.cancel()

    try:
        await task
    except asyncio.CancelledError:
        pass

    # Wait a bit for cleanup
    await asyncio.sleep(0.01)

    final_tasks = len(asyncio.all_tasks())
    if final_tasks > initial_tasks:
        print(f"Leak detected! Initial tasks: {initial_tasks}, Final tasks: {final_tasks}")
        sys.exit(1)
    else:
        print("No leak detected.")
        sys.exit(0)

if __name__ == "__main__":
    asyncio.run(test_leak())
EOF

# Save the bad commit hash for verification
echo $BAD_COMMIT > /home/user/.secret_expected_bad_commit

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user