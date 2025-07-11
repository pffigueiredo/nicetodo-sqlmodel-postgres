from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List


# Persistent models (stored in database)
class User(SQLModel, table=True):
    __tablename__ = "users"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    email: str = Field(unique=True, max_length=255)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    tasks: List["Task"] = Relationship(back_populates="user")


class Task(SQLModel, table=True):
    __tablename__ = "tasks"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=200)
    description: str = Field(default="", max_length=1000)
    completed: bool = Field(default=False)
    user_id: int = Field(foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    user: User = Relationship(back_populates="tasks")


# Non-persistent schemas (for validation, forms, API requests/responses)
class TaskCreate(SQLModel, table=False):
    title: str = Field(max_length=200)
    description: str = Field(default="", max_length=1000)
    user_id: int


class TaskUpdate(SQLModel, table=False):
    title: Optional[str] = Field(default=None, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: Optional[bool] = Field(default=None)


class UserCreate(SQLModel, table=False):
    name: str = Field(max_length=100)
    email: str = Field(max_length=255)


class UserResponse(SQLModel, table=False):
    id: int
    name: str
    email: str
    is_active: bool
    created_at: str
    task_count: int = Field(default=0)


class TaskResponse(SQLModel, table=False):
    id: int
    title: str
    description: str
    completed: bool
    created_at: str
    updated_at: str
    user_name: str
