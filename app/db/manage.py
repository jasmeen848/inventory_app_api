# #!/usr/bin/env python

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_url = 'mysql+pymysql://root:test@localhost/inventorydb'

engine = create_engine(
    db_url, pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
