from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class Goal(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    target_date: Optional[str] = None

    tasks: List['Task'] = Relationship(back_populates='goal')

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    description: str
    completed: bool = False
    goal_id: int = Field(foreign_key='goal.id')

    goal: Optional[Goal] = Relationship(back_populates='tasks')
