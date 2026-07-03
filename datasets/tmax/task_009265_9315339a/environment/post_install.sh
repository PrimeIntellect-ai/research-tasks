apt-get update && apt-get install -y python3 python3-pip
pip3 install pytest pandas numpy scikit-learn

useradd -m -s /bin/bash user || true

mkdir -p /home/user/data
cat << 'EOF' > /home/user/data/generate_data.py
import pandas as pd
import numpy as np

np.random.seed(42)
n = 500
ids = np.arange(1, n+1)
dates = pd.to_datetime(np.random.choice(pd.date_range('2023-01-01', '2023-12-31'), n))
# Mix date formats
date_strs = [d.strftime('%Y-%m-%d') if i % 2 == 0 else d.strftime('%m/%d/%Y') for i, d in enumerate(dates)]
zip_codes = np.random.choice([10001, 20002, 30003, 40004], n)
prices = np.random.uniform(10, 1000, n)
price_strs = ["${:,.2f}".format(p) for p in prices]
marketing = np.random.uniform(100, 5000, n)

months = dates.month
zip_effects = {10001: 500, 20002: 1000, 30003: 1500, 40004: 2000}
sales = (months * 100) + (prices * 2.5) + (marketing * 1.2) + np.array([zip_effects[z] for z in zip_codes]) + np.random.normal(0, 200, n)

df = pd.DataFrame({
    'id': ids,
    'date': date_strs,
    'zip_code': zip_codes,
    'price': price_strs,
    'marketing_spend': marketing,
    'sales': sales
})

df.to_csv('/home/user/data/raw_data.csv', index=False)
EOF

python3 /home/user/data/generate_data.py

chmod -R 777 /home/user