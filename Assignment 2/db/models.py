from sqlmodel import SQLModel, Field


class Task(SQLModel):
    id: int = Field(primary_key=True)
    title: str = Field()
    done: bool = Field(default=False)
    
