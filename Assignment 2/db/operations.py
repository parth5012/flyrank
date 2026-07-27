from db.models import Task
from sqlmodel import Session,select
from db.engine import engine

def get_all_tasks(session: Session) -> list[Task]:
    statement = select(Task)
    results = session.exec(statement)
    return list(results.all())

def get_task_by_id(session: Session, task_id: int) -> Task | None:
    statement = select(Task).where(Task.id == task_id)
    result = session.exec(statement).first()
    return result

if __name__ == "__main__":
    with Session(engine) as session:
        tasks = get_all_tasks(session)
        print(tasks)