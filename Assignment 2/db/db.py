from fastapi import Depends
from typing_extensions import Annotated
from sqlmodel import create_engine, Session, SQLModel


sqlite_file_name ="tasks.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# check_same_thread=False is unique and required for SQLite
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def get_session():
    """Dependency provider for database sessions."""
    with Session(engine) as session:
        yield session

Session = Annotated[Session, Depends(get_session)]

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

