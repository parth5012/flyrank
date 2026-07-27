from db.models import Task
from sqlmodel import Session,select
from db.engine import engine

def get_all_tasks(session: Session) -> list[Task]:
    statement = select(Task)
    results = session.exec(statement)
    return list(results.all())

if __name__ == "__main__":
    with Session(engine) as session:
        tasks = get_all_tasks(session)
        print(tasks)