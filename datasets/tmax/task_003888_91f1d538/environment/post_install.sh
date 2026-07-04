apt-get update && apt-get install -y python3 python3-pip git bc sed
    pip3 install pytest

    mkdir -p /home/user/repo
    cd /home/user/repo
    git init
    git config user.email "dev@example.com"
    git config user.name "Dev"

    cat << 'EOF' > data.txt
1.234
2.345
3.456
4.567
5.678
EOF
    base64 data.txt > data.b64
    rm data.txt

    cat << 'EOF' > process.sh
#!/bin/bash
base64 -d data.b64 > decoded.txt
sum=0
while read -r num; do
  sum=$(echo "scale=7; $sum + 1/$num" | bc -l)
done < decoded.txt
echo "$sum"
EOF
    chmod +x process.sh

    git add data.b64 process.sh
    git commit -m "Initial commit"

    for i in $(seq 1 200); do
      if [ $i -eq 137 ]; then
        sed -i 's/scale=7/scale=2/' process.sh
        git add process.sh
        git commit -m "Update scale for performance (commit $i)"
      else
        echo "# Comment $i" >> process.sh
        git add process.sh
        git commit -m "Add comment $i"
      fi
    done

    git log --grep="Update scale for performance" --format="%H" > /tmp/expected_bad_commit.txt

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user