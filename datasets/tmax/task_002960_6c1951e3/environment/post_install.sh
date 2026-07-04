apt-get update && apt-get install -y python3 python3-pip libc-bin coreutils findutils
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/dataset_raw/dir1
    mkdir -p /home/user/dataset_raw/dir2
    mkdir -p /home/user/dataset_clean
    mkdir -p /home/user/tmp_processing

    # Create dummy UTF-8 files first
    > /tmp/a_base.txt
    for i in $(seq 1 250); do echo "Data ISO A line $i: naïve résumé" >> /tmp/a_base.txt; done

    > /tmp/b_base.txt
    for i in $(seq 1 250); do echo "Data U16 B line $i: こんにちは" >> /tmp/b_base.txt; done

    > /tmp/c_base.txt
    for i in $(seq 1 250); do echo "Data ISO C line $i: façade" >> /tmp/c_base.txt; done

    # Convert to target encodings
    iconv -f UTF-8 -t ISO-8859-1 /tmp/a_base.txt > /home/user/dataset_raw/a.iso
    iconv -f UTF-8 -t UTF-16LE /tmp/b_base.txt > /home/user/dataset_raw/dir1/b.u16
    iconv -f UTF-8 -t ISO-8859-1 /tmp/c_base.txt > /home/user/dataset_raw/dir2/c.iso

    # Cleanup temps
    rm /tmp/a_base.txt /tmp/b_base.txt /tmp/c_base.txt

    chown -R user:user /home/user/dataset_raw /home/user/dataset_clean /home/user/tmp_processing
    chmod -R 777 /home/user