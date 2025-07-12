from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Update the connection string with your MySQL credentials
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:Harshit%40123@localhost/food_delivery"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) 