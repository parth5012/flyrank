from fastapi import Depends
from typing_extensions import Annotated
from sqlmodel import  Session, SQLModel,select
from db.engine import engine
from db.models import Task,models

def get_session():
    """Dependency provider for database sessions."""
    with Session(engine) as session:
        yield session

APISession = Annotated[Session, Depends(get_session)]


def generate_fake_tasks(session: Session):
    for i in range(3):
        task = Task(id=i, title=f"Task {i}", done=False)
        session.add(task)
    session.commit()

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        all_tables_empty = all(
                session.exec(select(model)).first() is None 
                for model in models)
        if all_tables_empty:
            generate_fake_tasks(session)
    

