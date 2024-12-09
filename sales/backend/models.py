from typing import Optional
import reflex as rx
from sqlmodel import Field, SQLModel
from enum import Enum


class UserType(str, Enum):
    ADMIN = "admin"
    CUSTOMER = "customer"


class User(SQLModel, table=True):
    """Base user model."""
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    clerk_id: str = Field(unique=True)
    user_type: UserType
    
    # Customer fields - nullable for admin users
    customer_name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    location: Optional[str] = None
    job: Optional[str] = None
    salary: Optional[int] = None
