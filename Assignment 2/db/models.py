from sqlmodel import SQLModel, Field


class Task(SQLModel, table=True):
    id: int = Field(primary_key=True, default=None)
    title: str = Field()
    done: bool = Field(default=False)
    
models = [Task]