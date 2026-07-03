apt-get update && apt-get install -y python3 python3-pip git
pip3 install pytest

useradd -m -s /bin/bash user || true

bash -c '

mkdir -p /home/user/service_repo
cd /home/user/service_repo

git config --global user.email "test@example.com"
git config --global user.name "Test User"
git config --global init.defaultBranch main

git init

cat << "EOF" > processor.py
class Node:
    def __init__(self, val, next_node=None):
        self.val = val
        self.next = next_node

def run_service():
    head = Node(1, Node(2, Node(3, Node(4, Node(5)))))
    curr = head
    cache = []

    # Process nodes
    while curr is not None:
        cache.append(curr.val)
        curr = curr.next

    print("Service finished successfully.")

if __name__ == "__main__":
    run_service()
EOF

echo "requests==2.31.0" > requirements.txt

for i in {1..4}; do
    echo "# Harmless comment $i" >> processor.py
    git add processor.py requirements.txt
    git commit -m "Harmless commit $i"
done

cat << "EOF" > processor.py
class Node:
    def __init__(self, val, next_node=None):
        self.val = val
        self.next = next_node

def run_service():
    head = Node(1, Node(2, Node(3, Node(4, Node(5)))))
    curr = head
    cache = []

    # Process nodes
    while curr is not None:
        cache.append(curr.val)

    print("Service finished successfully.")

if __name__ == "__main__":
    run_service()
EOF
echo "# Harmless comment 1" >> processor.py
echo "# Harmless comment 2" >> processor.py
echo "# Harmless comment 3" >> processor.py
echo "# Harmless comment 4" >> processor.py

git add processor.py
git commit -m "Refactor processing logic"
git rev-parse HEAD > /home/user/.secret_bad_commit

for i in {6..9}; do
    echo "# Harmless comment $i" >> processor.py
    git add processor.py
    git commit -m "Harmless commit $i"
done

echo "nonexistent-fake-package-12345==99.99.99" >> requirements.txt
git add requirements.txt
git commit -m "Update requirements"
'

chown -R user:user /home/user/service_repo
chown user:user /home/user/.secret_bad_commit
chmod -R 777 /home/user