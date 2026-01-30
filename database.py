import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 1. Your Aiven URI (Cleaned of the ?ssl-mode=... part)
# Use your actual password and hostname here
AIVEN_URI = "mysql://avnadmin:AVNS_50e-Od90lOam2DJMT6P@mysql-intelliims-123-intelli-ims-prod.k.aivencloud.com:21425/inventory_management"

# 2. Force the correct protocol for PyMySQL
if AIVEN_URI.startswith("mysql://"):
    AIVEN_URI = AIVEN_URI.replace("mysql://", "mysql+pymysql://", 1)

# 3. Create the engine with SSL arguments passed separately
# This bypasses the 'unexpected keyword argument' error entirely
engine = create_engine(
    AIVEN_URI,
    connect_args={
        "ssl": {
            "ssl_mode": "REQUIRED"
        }
    }
)

session = sessionmaker(autocommit=False, autoflush=False, bind=engine)