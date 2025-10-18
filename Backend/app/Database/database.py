#Module for establishing connection with PostgreSQL Database


from sqlmodel import create_engine,Session

DATABASE_URL =  'postgresql://samarth:samarth2410@localhost:5432/ai_db'



engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_table():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

