apt-get update && apt-get install -y python3 python3-pip tesseract-ocr imagemagick fonts-dejavu-core zip unzip tar xz-utils
    pip3 install pytest

    mkdir -p /app
    convert -background white -fill black -font DejaVu-Sans -pointsize 24 label:"STORAGE POLICY 2024\nTarget Size: <= 1250000 bytes\nArchive Password: AdminStoragePass_99!" /app/policy.png

    mkdir -p /home/user/storage_pool/raw_data
    mkdir -p /home/user/storage_pool/dupes

    for i in $(seq 1 10); do
        head -c 100000 /dev/urandom > /home/user/storage_pool/raw_data/random_base_$i.dat
    done
    head -c 500000 /dev/zero > /home/user/storage_pool/raw_data/compressible.log

    for i in $(seq 1 200); do
        cp /home/user/storage_pool/raw_data/random_base_1.dat /home/user/storage_pool/dupes/copy_$i.dat
        cp /home/user/storage_pool/raw_data/compressible.log /home/user/storage_pool/dupes/log_copy_$i.log
    done

    cd /home/user/storage_pool
    zip -r -P "AdminStoragePass_99!" encrypted_logs.zip raw_data/ dupes/
    tar -czf nested.tar.gz encrypted_logs.zip
    zip wrapper.zip nested.tar.gz

    cp encrypted_logs.zip copy2.zip
    cp encrypted_logs.zip copy3.zip

    rm -rf raw_data dupes nested.tar.gz

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app