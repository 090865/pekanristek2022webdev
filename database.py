from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine=create_engine("postgresql://test:1@localhost/project1", 
    echo=True
)

Base=declarative_base()

SessionLocal=sessionmaker(bind=engine)