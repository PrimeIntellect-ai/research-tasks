apt-get update && apt-get install -y python3 python3-pip gcc
    pip3 install pytest

    mkdir -p /home/user/configs/subdir
    printf "aaaaabbbbbbbbb" > /home/user/configs/file1.txt
    printf "xxxxyyzzzzzz\n\n" > /home/user/configs/subdir/file2.txt

    ln -s link_b /home/user/configs/link_a
    ln -s link_a /home/user/configs/subdir/link_b

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user