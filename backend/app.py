from fastapi import FastAPI, HTTPException
from typing import List, Optional
from sqlmodel import Session, select

from .database import create_db_and_tables, engine
from .models import Goal, Task

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Goal endpoints
@app.post('/goals', response_model=Goal)
def create_goal(goal: Goal):
    with Session(engine) as session:
        session.add(goal)
        session.commit()
        session.refresh(goal)
        return goal

@app.get('/goals', response_model=List[Goal])
def read_goals():
    with Session(engine) as session:
        goals = session.exec(select(Goal)).all()
        return goals

@app.get('/goals/{goal_id}', response_model=Goal)
def read_goal(goal_id: int):
    with Session(engine) as session:
        goal = session.get(Goal, goal_id)
        if not goal:
            raise HTTPException(status_code=404, detail='Goal not found')
        return goal

@app.put('/goals/{goal_id}', response_model=Goal)
def update_goal(goal_id: int, data: Goal):
    with Session(engine) as session:
        goal = session.get(Goal, goal_id)
        if not goal:
            raise HTTPException(status_code=404, detail='Goal not found')
        for key, value in data.dict(exclude_unset=True).items():
            setattr(goal, key, value)
        session.add(goal)
        session.commit()
        session.refresh(goal)
        return goal

@app.delete('/goals/{goal_id}')
def delete_goal(goal_id: int):
    with Session(engine) as session:
        goal = session.get(Goal, goal_id)
        if not goal:
            raise HTTPException(status_code=404, detail='Goal not found')
        session.delete(goal)
        session.commit()
        return {'ok': True}

# Task endpoints
@app.post('/tasks', response_model=Task)
def create_task(task: Task):
    with Session(engine) as session:
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

@app.get('/tasks', response_model=List[Task])
def read_tasks(goal_id: Optional[int] = None):
    with Session(engine) as session:
        statement = select(Task)
        if goal_id is not None:
            statement = statement.where(Task.goal_id == goal_id)
        tasks = session.exec(statement).all()
        return tasks

@app.get('/tasks/{task_id}', response_model=Task)
def read_task(task_id: int):
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail='Task not found')
        return task

@app.put('/tasks/{task_id}', response_model=Task)
def update_task(task_id: int, data: Task):
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail='Task not found')
        for key, value in data.dict(exclude_unset=True).items():
            setattr(task, key, value)
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

@app.delete('/tasks/{task_id}')
def delete_task(task_id: int):
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail='Task not found')
        session.delete(task)
        session.commit()
        return {'ok': True}
