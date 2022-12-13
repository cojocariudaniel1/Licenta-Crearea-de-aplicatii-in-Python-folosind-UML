from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://admin:1395@localhost:5432/licenta_database')

#Creare noua conexiune la baza de date
Session = sessionmaker(bind=engine)

# In base se stocheaza tot ce tine de clase (metadata)
Base = declarative_base()



