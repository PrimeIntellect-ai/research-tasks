apt-get update && apt-get install -y python3 python3-pip git g++ binutils
pip3 install pytest

mkdir -p /home/user/repo
cd /home/user/repo

git init
git config user.name "Dev"
git config user.email "dev@example.com"

for i in $(seq 1 50); do
    if [ $i -lt 35 ]; then
        cat << 'EOF' > main.cpp
#include <iostream>
int main() {
    return 0;
}
EOF
    else
        cat << 'EOF' > main.cpp
#include <iostream>
#include <cstdio>
int main() {
    FILE* f = fopen("crash.dmp", "wb");
    if (f) {
        const char* dump_data = "\x00\x01\x02\x03\x04DEADLOCK_THREAD_ID=0x8A4F92B\x00\xFF\xEE";
        fwrite(dump_data, 1, 33, f);
        fclose(f);
    }
    return 1;
}
EOF
    fi
    # Append a unique comment so git commit doesn't fail due to empty changes
    echo "// Commit $i" >> main.cpp

    git add main.cpp
    GIT_AUTHOR_DATE="2023-10-01 12:00:00" GIT_COMMITTER_DATE="2023-10-01 12:00:00" git commit -m "Commit $i"
done

cat << 'EOF' > /home/user/test.sh
#!/bin/bash
cd /home/user/repo
g++ main.cpp -o app
./app
EOF
chmod +x /home/user/test.sh

cd /home/user/repo
BAD_COMMIT=$(git log --format="%h" --grep="Commit 35")
echo "COMMIT:${BAD_COMMIT},ID:0x8A4F92B" > /tmp/expected_solution.txt

useradd -m -s /bin/bash user || true
chown -R user:user /home/user
chmod -R 777 /home/user