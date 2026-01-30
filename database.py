import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# This pulls the URI from Render's Environment Variables
AIVEN_URI = os.getenv("DATABASE_URL")

# Fallback for local testing if the Environment Variable isn't set
if not AIVEN_URI:
    AIVEN_URI = "mysql+pymysql://avnadmin:AVNS_50e-Od90lOam2DJMT6P@mysql-intelliims-123-intelli-ims-prod.k.aivencloud.com:21425/inventory_management"

# Ensure the protocol is correct for SQLAlchemy
if AIVEN_URI.startswith("mysql://"):
    AIVEN_URI = AIVEN_URI.replace("mysql://", "mysql+pymysql://", 1)

engine = create_engine(
    AIVEN_URI,
    connect_args={
        "ssl": {
            "ssl_mode": "REQUIRED"
        }
    }
)

session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

